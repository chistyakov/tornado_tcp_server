from core.marshall import marshall_message_as_rows
from core.primitives import InboxMessage


class Observer:
    def __init__(self, stream):
        self.stream = stream

    async def notify(self, message: InboxMessage):
        return await self.on_message(message)

    async def on_message(self, message: InboxMessage):
        for row in marshall_message_as_rows(message):
            await self.stream.write(row)
