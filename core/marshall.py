from core.primitives import OutputMessage
from core.utils import xor


async def marshall_message(stream, message: OutputMessage):
    bytes_obj = message.header + marshall_message_number(message.message_number)
    bytes_obj = bytes_obj + xor(bytes_obj)
    await stream.write(bytes_obj)


def marshall_message_number(message_number: int) -> bytes:
    return message_number.to_bytes(2, byteorder="big", signed=False)
