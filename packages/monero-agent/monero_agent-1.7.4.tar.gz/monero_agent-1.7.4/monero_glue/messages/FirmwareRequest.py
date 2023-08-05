# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class FirmwareRequest(p.MessageType):
    MESSAGE_WIRE_TYPE = 8

    def __init__(
        self,
        offset: int = None,
        length: int = None,
    ) -> None:
        self.offset = offset
        self.length = length

    @classmethod
    def get_fields(cls):
        return {
            1: ('offset', p.UVarintType, 0),
            2: ('length', p.UVarintType, 0),
        }
