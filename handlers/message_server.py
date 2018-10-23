import logging

from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from core.marshall import marshall_outbox
from core.primitives import OutboxMessage, InboxMessage
from core.unmarshall import unmarshall_inbox

logger = logging.getLogger(__name__)


class MessageServer(TCPServer):
    def __init__(self, observers, **kwargs):
        super().__init__(**kwargs)
        self.observers = observers

    async def handle_stream(self, stream, address):
        while True:
            try:
                await self._handle_single_message(stream)
            except StreamClosedError:
                break

    async def _handle_single_message(self, stream):
        try:
            inbox_message = await unmarshall_inbox(stream)
            outbox_message = OutboxMessage(b"\x11", inbox_message.message_number)
            await self.notify_observers(inbox_message)
        except ValueError:
            logger.exception("Error on unmarshalling")
            outbox_message = OutboxMessage(b"\x12", 0)
        bytes_obj = marshall_outbox(outbox_message)
        await stream.write(bytes_obj)

    async def notify_observers(self, message: InboxMessage):
        for observer in self.observers:
            await observer.notify(message)
