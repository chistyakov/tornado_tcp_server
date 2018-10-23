from dataclasses import dataclass
from typing import List


@dataclass
class InputMessage:
    header: bytes
    message_number: int
    source_name: str
    source_status: str
    fields_count: int
    fields: List[tuple]
    source_xor: bytes
    raw: bytes


@dataclass
class OutputMessage:
    header: bytes
    message_number: int
