from typing import List

from core.primitives import InputMessage
from core.utils import bytes_to_int, bytes_to_ascii, xor

import logging

logger = logging.getLogger(__name__)


async def unmarshall_message(stream) -> InputMessage:
    header = await stream.read_bytes(1)
    message_number = await stream.read_bytes(2)
    source_name = await stream.read_bytes(8)
    source_status = await stream.read_bytes(1)
    fields_count = await stream.read_bytes(1)
    fields_count_int = bytes_to_int(fields_count)
    fields = await stream.read_bytes(fields_count_int * 12)
    source_xor = await stream.read_bytes(1)

    message = InputMessage(
        header=unmarshall_header(header),
        message_number=unmarshall_message_number(message_number),
        source_name=source_name,
        source_status=unmarshall_source_status(source_status),
        fields_count=fields_count_int,
        fields=unmarshall_fields(fields_count_int, fields),
        source_xor=source_xor,
        raw=(
            header
            + message_number
            + source_name
            + source_status
            + fields_count
            + fields
        ),
    )

    validate_xor(message)
    return message


def unmarshall_header(bytes_obj: bytes) -> bytes:
    if bytes_obj != b"\x01":
        raise ValueError(f"Invalid header {bytes_obj}")
    return bytes_obj


def unmarshall_message_number(bytes_obj: bytes) -> int:
    return bytes_to_int(bytes_obj)


def unmarshall_source_status(bytes_obj: bytes) -> str:
    try:
        return {b"\x01": "IDLE", b"\x02": "ACTIVE", b"\x03": "RECHARGE"}[bytes_obj]
    except KeyError:
        raise ValueError(f"Invalid status {bytes_obj}")


def unmarshall_fields(fields_count: int, bytes_obj: bytes) -> List[tuple]:
    """
    >>> unmarshall_fields(0, b'')
    []
    >>> unmarshall_fields(1, b'\\x00' + b'spamfoo' + b'\\x00\\x00\\x00\\x01')
    [('spamfoo', 1)]
    >>> unmarshall_fields(2, b'\\x00' + b'spamfoo' + b'\\x00\\x00\\x00\\x01' + b'abcdefgh' + b'\\x00\\x00\\x00\\x10')
    [('spamfoo', 1), ('abcdefgh', 16)]
    """
    result = []
    for i in range(fields_count):
        start_byte_index = i * 12
        field_name = bytes_obj[start_byte_index : start_byte_index + 8]
        field_value = bytes_obj[start_byte_index + 8 : start_byte_index + 12]

        result.append((bytes_to_ascii(field_name), bytes_to_int(field_value)))
    return result


def validate_xor(message: InputMessage) -> None:
    expected_xor = message.source_xor
    actual_xor = xor(message.raw)
    if actual_xor != expected_xor:
        raise ValueError(f"Invalid xor {actual_xor} expected: {expected_xor}")
