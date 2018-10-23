import logging

from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from core.observer import Observer

logger = logging.getLogger(__name__)


class ObserveServer(TCPServer):
    def __init__(self, observers, **kwargs):
        super().__init__(**kwargs)
        self.observers = observers

    async def handle_stream(self, stream, address):
        # await stream.write(b"fooo\r\n")
        self.observers.add(Observer(stream))
        while True:
            try:
                await stream.read_until_close()
            except StreamClosedError:
                break
