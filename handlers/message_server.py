import logging

from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from core.marshall import marshall_message
from core.primitives import OutputMessage
from core.unmarshall import unmarshall_message

logger = logging.getLogger(__name__)


class MessageServer(TCPServer):
    async def handle_stream(self, stream, address):
        while True:
            try:
                await self._handle_single_message(stream)
            except StreamClosedError:
                break

    async def _handle_single_message(self, stream):
        try:
            input_message = await unmarshall_message(stream)
            output_message = OutputMessage(b"\x11", input_message.message_number)
        except ValueError:
            logger.exception("Error on unmarshalling")
            output_message = OutputMessage(b"\x12", 0)
        await marshall_message(stream, output_message)
