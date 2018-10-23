from typing import Iterable

from core.primitives import (
    OutboxMessage,
    InboxMessage,
    SOURCE_STATUSES,
    OnlineSourceStatistics,
)
from core.utils import xor, ascii_to_bytes, int_to_bytes, now_in_ms


def marshall_outbox(message: OutboxMessage) -> bytes:
    bytes_obj = message.header + marshall_message_number(message)
    bytes_obj = bytes_obj + xor(bytes_obj)
    return bytes_obj


def marshal_inbox(message: InboxMessage):
    if message.raw_payload is None:
        payload = b"".join(
            [
                marshall_header(message),
                marshall_message_number(message),
                marshall_source_name(message),
                marshall_source_status(message),
                marshall_fields(message),
            ]
        )
    else:
        payload = message.raw_payload
    xor_payload = xor(payload) if message.source_xor is None else message.source_xor
    return payload + xor_payload


def marshall_header(message: InboxMessage) -> bytes:
    bytes_obj = message.header
    if bytes_obj != b"\x01":
        raise ValueError(f"Invalid header {bytes_obj}")
    return bytes_obj


def marshall_message_number(message: [InboxMessage, OutboxMessage]) -> bytes:
    return int_to_bytes(message.message_number, 2)


def marshall_source_name(message: InboxMessage) -> bytes:
    return ascii_to_bytes(message.source_name, 8)


def marshall_fields(message: InboxMessage) -> bytes:
    fields_count = (
        int_to_bytes(len(message.fields), 1)
        if message.fields_count is None
        else message.fields_count
    )
    fields_bytes = [
        ascii_to_bytes(name, 8) + int_to_bytes(value, 4)
        for name, value in message.fields
    ]
    return b"".join([fields_count, *fields_bytes])


def marshall_source_status(message: InboxMessage) -> bytes:
    try:
        return next(
            key
            for key, value in SOURCE_STATUSES.items()
            if value == message.source_status
        )
    except StopIteration:
        raise ValueError(f"Invalid status {message.source_status}")


def marshall_message_as_rows(message: InboxMessage) -> Iterable[bytes]:
    for field_name, field_value in message.fields:
        yield f"[{message.source_name}] {field_name} | {field_value}\r\n".encode(
            "ascii", "ignore"
        )


def marshall_online_statistics(stat: OnlineSourceStatistics) -> bytes:
    time_delta_in_ms = now_in_ms() - stat.last_message_timestamp_in_ms
    return (
        f"[{stat.name}] "
        f"{stat.last_message_number} | "
        f"{stat.status} | "
        f"{time_delta_in_ms}"
        "\r\n"
    ).encode("ascii", "ignore")
