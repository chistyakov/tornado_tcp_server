import logging

from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer

from core.marshall import marshall_outbox
from core.primitives import OutboxMessage, InboxMessage, SourceStatistics
from core.unmarshall import unmarshall_inbox
from core.utils import now_in_ms

logger = logging.getLogger(__name__)


class MessageServer(TCPServer):
    def __init__(self, observers, sources_statistics, **kwargs):
        super().__init__(**kwargs)
        self.observers = observers
        self.sources_statistics = sources_statistics

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
            await self.on_valid_message(inbox_message)
        except ValueError:
            logger.exception("Error on unmarshalling")
            outbox_message = OutboxMessage(b"\x12", 0)
        await stream.write(marshall_outbox(outbox_message))

    async def on_valid_message(self, message: InboxMessage):
        self.sources_statistics[message.source_name] = SourceStatistics(
            message.source_name,
            message.source_status,
            message.message_number,
            now_in_ms(),
        )
        for observer in self.observers:
            await observer.notify(message)
