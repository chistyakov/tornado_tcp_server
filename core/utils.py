from functools import reduce


def bytes_to_int(bytes_obj: bytes) -> int:
    """
    >>> bytes_to_int(bytes([0x10]))
    16
    >>> bytes_to_int(bytes([0x10, 0x10]))
    4112
    """
    # https://docs.python.org/3.7/library/stdtypes.html#bytes
    return int.from_bytes(bytes_obj, byteorder="big", signed=False)


def bytes_to_ascii(bytes_obj: bytes) -> str:
    """
    >>> bytes_to_ascii(b'\\x00' + b'spamfoo')
    'spamfoo'
    """
    return bytes_obj.lstrip(b"\x00").decode("ascii", "ignore")


def xor(bytes_obj: bytes) -> bytes:
    """
    >>> xor(bytes([0x01, 0x04, 0x03]))
    b'\\x06'
    """
    if len(bytes_obj) < 2:
        raise ValueError
    head, *tail = bytes_obj
    return bytes([reduce(lambda x, y: x ^ y, tail, head)])
