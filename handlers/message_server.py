import logging

from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from core.marshall import marshall_outbox
from core.primitives import OutboxMessage
from core.unmarshall import unmarshall_inbox

logger = logging.getLogger(__name__)


class MessageServer(TCPServer):
    async def handle_stream(self, stream, address):
        while True:
            try:
                await _handle_single_message(stream)
            except StreamClosedError:
                break


async def _handle_single_message(stream):
    try:
        inbox_message = await unmarshall_inbox(stream)
        outbox_message = OutboxMessage(b"\x11", inbox_message.message_number)
    except ValueError:
        logger.exception("Error on unmarshalling")
        outbox_message = OutboxMessage(b"\x12", 0)
    bytes_obj = marshall_outbox(outbox_message)
    await stream.write(bytes_obj)
