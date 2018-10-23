import logging

from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from core.marshall import marshall_online_statistics
from core.observer import Observer

logger = logging.getLogger(__name__)


class ObserveServer(TCPServer):
    def __init__(self, observers, sources_statistics, **kwargs):
        super().__init__(**kwargs)
        self.observers = observers
        self.online_statistics = sources_statistics

    async def handle_stream(self, stream, address):
        await self.on_connect(stream)
        while True:
            try:
                await stream.read_until_close()
            except StreamClosedError:
                await self.on_disconnect(stream)
                break

    async def on_connect(self, stream):
        await self.send_online_statistics(stream)
        self.observers.add(Observer(stream))

    async def send_online_statistics(self, stream):
        for stat in self.online_statistics.values():
            await stream.write(marshall_online_statistics(stat))

    async def on_disconnect(self, stream):
        self.observers.pop(stream)
