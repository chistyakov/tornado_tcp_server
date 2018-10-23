import logging

from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

logger = logging.getLogger(__name__)


class ObserveServer(TCPServer):
    async def handle_stream(self, stream, address):
        await stream.write(b"fooo\r\n")
