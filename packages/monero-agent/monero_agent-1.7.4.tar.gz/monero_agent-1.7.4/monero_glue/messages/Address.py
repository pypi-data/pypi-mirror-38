# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class Address(p.MessageType):
    MESSAGE_WIRE_TYPE = 30

    def __init__(
        self,
        address: str = None,
    ) -> None:
        self.address = address

    @classmethod
    def get_fields(cls):
        return {
            1: ('address', p.UnicodeType, 0),  # required
        }
