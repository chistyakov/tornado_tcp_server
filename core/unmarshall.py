from typing import List

from core.primitives import InboxMessage, SOURCE_STATUSES
from core.utils import bytes_to_int, bytes_to_ascii, xor

import logging

logger = logging.getLogger(__name__)


async def unmarshall_inbox(stream) -> InboxMessage:
    header_bytes = await stream.read_bytes(1)
    message_number_bytes = await stream.read_bytes(2)
    source_name_bytes = await stream.read_bytes(8)
    source_status_bytes = await stream.read_bytes(1)
    fields_count = await stream.read_bytes(1)
    fields_count_int = bytes_to_int(fields_count)
    fields_bytes = await stream.read_bytes(fields_count_int * 12)
    source_xor_bytes = await stream.read_bytes(1)

    message = InboxMessage(
        header=unmarshall_header(header_bytes),
        message_number=unmarshall_message_number(message_number_bytes),
        source_name=unmarshall_source_name(source_name_bytes),
        source_status=unmarshall_source_status(source_status_bytes),
        fields_count=fields_count_int,
        fields=unmarshall_fields(fields_count_int, fields_bytes),
        source_xor=source_xor_bytes,
        raw_payload=(
            header_bytes
            + message_number_bytes
            + source_name_bytes
            + source_status_bytes
            + fields_count
            + fields_bytes
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


def unmarshall_source_name(bytes_obj: bytes) -> str:
    return bytes_to_ascii(bytes_obj)


def unmarshall_source_status(bytes_obj: bytes) -> str:
    try:
        return SOURCE_STATUSES[bytes_obj]
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


def validate_xor(message: InboxMessage) -> None:
    expected_xor = message.source_xor
    actual_xor = xor(message.raw_payload)
    if actual_xor != expected_xor:
        raise ValueError(f"Invalid xor {actual_xor} expected: {expected_xor}")
