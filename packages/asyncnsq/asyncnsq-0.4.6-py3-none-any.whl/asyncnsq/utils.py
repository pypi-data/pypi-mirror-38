import asyncio
import random
import re
import time
from urllib.parse import urlparse


TOPIC_NAME_RE = re.compile(r'^[\.a-zA-Z0-9_-]+$')
CHANNEL_NAME_RE = re.compile(r'^[\.a-zA-Z0-9_-]+(#ephemeral)?$')


def get_host_and_port(host):
    host_parsed = urlparse(host)
    if host_parsed.scheme == 'tcp':
        result = host_parsed.netloc
    elif host_parsed.scheme == '':
        result = host_parsed.path
    else:
        result = host
    result = result.split(':')
    if len(result) == 2:
        return result[0], result[-1]
    else:
        return result[0], None


def valid_topic_name(topic):
    if not 0 < len(topic) < 33:
        return False
    return bool(TOPIC_NAME_RE.match(topic))


def valid_channel_name(channel):
    if not 0 < len(channel) < 33:
        return False
    return bool(CHANNEL_NAME_RE.match(channel))


_converters_to_bytes_map = {
    bytes: lambda val: val,
    bytearray: lambda val: val,
    str: lambda val: val.encode('utf-8'),
    int: lambda val: str(val).encode('utf-8'),
    float: lambda val: str(val).encode('utf-8'),
}


_converters_to_str_map = {
    str: lambda val: val,
    bytearray: lambda val: bytes(val).decode('utf-8'),
    bytes: lambda val: val.decode('utf-8'),
    int: lambda val: str(val),
    float: lambda val: str(val),
}


def _convert_to_bytes(value):
    if type(value) in _converters_to_bytes_map:
        converted_value = _converters_to_bytes_map[type(value)](value)
    else:
        raise TypeError("Argument {!r} expected to be of bytes,"
                        " str, int or float type".format(value))
    return converted_value


def _convert_to_str(value):
    if type(value) in _converters_to_str_map:
        converted_value = _converters_to_str_map[type(value)](value)
    else:
        raise TypeError("Argument {!r} expected to be of bytes,"
                        " str, int or float type".format(value))
    return converted_value


class MaxRetriesExided(Exception):
    pass


def retry_iterator(init_delay=0.1, max_delay=10.0, factor=2.7182818284590451,
                   jitter=0.11962656472, max_retries=None, now=True):
    """Based on twisted reconnection factory.

    :param init_delay:
    :param max_delay:
    :param factor:
    :param jitter:
    :param max_retries:
    :param now:
    :return:
    """
    retries, delay = 0, init_delay
    if now:
        retries += 1
        yield 0.0
    while not max_retries or retries < max_retries:
        retries += 1
        delay *= factor
        delay = random.normalvariate(
            delay, delay * jitter) if jitter else delay
        delay = min(delay, max_delay) if max_delay else delay
        yield delay
    else:
        raise MaxRetriesExided()


REDISTRIBUTE = 0
CHANGE_CONN_RDY = 1


class RdyControl:

    def __init__(self, idle_timeout, max_in_flight, loop=None):
        self._connections = {}
        self._idle_timeout = idle_timeout
        self._total_ready_count = 0
        self._max_in_flight = max_in_flight
        self._loop = loop or asyncio.get_event_loop()

        self._cmd_queue = asyncio.Queue(loop=self._loop)

        self._expected_rdy_state = {}

        self._is_working = True

        self._distributor_task = self._loop.create_task(self._distributor())

    def add_connections(self, connections):
        self._connections = connections
        for conn in self._connections.values():
            conn._on_rdy_changed_cb = self.rdy_changed

    def add_connection(self, connection):
        connection._on_rdy_changed_cb = self.rdy_changed
        self._connections[connection.id] = connection

    def rdy_changed(self, conn_id):
        self._cmd_queue.put_nowait((CHANGE_CONN_RDY, (conn_id,)))

    def redistribute(self):
        self._cmd_queue.put_nowait((REDISTRIBUTE, ()))

    async def _distributor(self):
        while self._is_working:
            cmd, args = await self._cmd_queue.get()
            if cmd == REDISTRIBUTE:
                await self._redistribute_rdy_state()
            elif cmd == CHANGE_CONN_RDY:
                await self._update_rdy(*args)
            else:
                RuntimeError("Should never be here")

    def remove_connection(self, conn):
        self._connections.pop(conn.id)

    def remove_all(self):
        self._connections = {}

    async def _redistribute_rdy_state(self):
        # We redistribute RDY counts in a few cases:
        #
        # 1. our # of connections exceeds our configured max_in_flight
        # 2. we're in backoff mode (but not in a current backoff block)
        # 3. something out-of-band has set the need_rdy_redistributed flag
        # (connection closed
        # that was about to get RDY during backoff)
        #
        # At a high level, we're trying to mitigate stalls related to
        # -volume
        # producers when we're unable (by configuration or backoff) to provide
        # a RDY count
        # of (at least) 1 to all of our connections.

        connections = self._connections.values()

        rdy_coros = [
            conn.rdy(0) for conn in connections
            if not (conn.rdy_state == 0 or \
                (time.time() - conn.last_message) < self._idle_timeout)
        ]

        distributed_rdy = sum(c.rdy_state for c in connections)
        not_distributed_rdy = self._max_in_flight - distributed_rdy

        random_connections = random.sample(list(connections),
                                           min(not_distributed_rdy,
                                               len(connections)))

        rdy_coros += [conn.rdy(1) for conn in random_connections]

        await asyncio.gather(*rdy_coros)

    async def _update_rdy(self, conn_id):
        conn = self._connections[conn_id]

        if conn.rdy_state > int(conn._last_rdy * 0.25):
            return

        rdy_state = max(1, self._max_in_flight /
                        max(1, len(self._connections)))

        await conn.rdy(int(rdy_state))
