from dataclasses import dataclass
from typing import List, Optional


@dataclass
class InboxMessage:
    header: bytes
    message_number: int
    source_name: str
    source_status: str
    fields_count: Optional[int]
    fields: List[tuple]
    source_xor: bytes = None
    raw_payload: bytes = None


@dataclass
class OutboxMessage:
    header: bytes
    message_number: int


SOURCE_STATUSES = {b"\x01": "IDLE", b"\x02": "ACTIVE", b"\x03": "RECHARGE"}


@dataclass
class OnlineSourceStatistics:
    name: str
    status: str
    last_message_number: int
    last_message_timestamp_in_ms: int
