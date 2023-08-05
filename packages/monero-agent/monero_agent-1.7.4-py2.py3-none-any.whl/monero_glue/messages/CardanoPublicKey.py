# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .HDNodeType import HDNodeType


class CardanoPublicKey(p.MessageType):
    MESSAGE_WIRE_TYPE = 306

    def __init__(
        self,
        xpub: str = None,
        node: HDNodeType = None,
    ) -> None:
        self.xpub = xpub
        self.node = node

    @classmethod
    def get_fields(cls):
        return {
            1: ('xpub', p.UnicodeType, 0),
            2: ('node', HDNodeType, 0),
        }
