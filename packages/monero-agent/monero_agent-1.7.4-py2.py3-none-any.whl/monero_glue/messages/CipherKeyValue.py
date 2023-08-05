# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore


class CipherKeyValue(p.MessageType):
    MESSAGE_WIRE_TYPE = 23

    def __init__(
        self,
        address_n: List[int] = None,
        key: str = None,
        value: bytes = None,
        encrypt: bool = None,
        ask_on_encrypt: bool = None,
        ask_on_decrypt: bool = None,
        iv: bytes = None,
    ) -> None:
        self.address_n = address_n if address_n is not None else []
        self.key = key
        self.value = value
        self.encrypt = encrypt
        self.ask_on_encrypt = ask_on_encrypt
        self.ask_on_decrypt = ask_on_decrypt
        self.iv = iv

    @classmethod
    def get_fields(cls):
        return {
            1: ('address_n', p.UVarintType, p.FLAG_REPEATED),
            2: ('key', p.UnicodeType, 0),
            3: ('value', p.BytesType, 0),
            4: ('encrypt', p.BoolType, 0),
            5: ('ask_on_encrypt', p.BoolType, 0),
            6: ('ask_on_decrypt', p.BoolType, 0),
            7: ('iv', p.BytesType, 0),
        }
