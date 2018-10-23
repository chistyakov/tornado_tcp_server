from functools import reduce


def bytes_to_int(bytes_obj: bytes) -> int:
    """
    >>> bytes_to_int(bytes([0x10]))
    16
    >>> bytes_to_int(bytes([0x10, 0x10]))
    4112
    """
    return int.from_bytes(bytes_obj, byteorder="big", signed=False)


def int_to_bytes(int_obj: int, length: int) -> bytes:
    """
    >>> int_to_bytes(16, 1)
    b'\\x10'
    >>> int_to_bytes(4112, 2)
    b'\\x10\\x10'
    """
    return int.to_bytes(int_obj, length, byteorder="big", signed=False)


def bytes_to_ascii(bytes_obj: bytes) -> str:
    """
    >>> bytes_to_ascii(b'\\x00' + b'spamfoo')
    'spamfoo'
    """
    return bytes_obj.lstrip(b"\x00").decode("ascii", "ignore")


def ascii_to_bytes(str_obj: str, length: int) -> bytes:
    """
    >>> ascii_to_bytes('spamfoo', 8)
    b'\\x00spamfoo'
    >>> ascii_to_bytes('pamfoo', 8)
    b'\\x00\\x00pamfoo'
    >>> ascii_to_bytes('baspamfoo', 8)
    Traceback (most recent call last):
    ...
    ValueError: ascii string baspamfoo greater then length limit 8
    """
    if len(str_obj) > length:
        raise ValueError(f"ascii string {str_obj} greater then length limit {length}")
    return str_obj.encode("ascii", "ignore").rjust(length, b"\x00")


def xor(bytes_obj: bytes) -> bytes:
    """
    >>> xor(bytes([0x01, 0x04, 0x03]))
    b'\\x06'
    """
    if len(bytes_obj) < 2:
        raise ValueError
    head, *tail = bytes_obj
    return bytes([reduce(lambda x, y: x ^ y, tail, head)])
