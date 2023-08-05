# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .IdentityType import IdentityType


class GetECDHSessionKey(p.MessageType):
    MESSAGE_WIRE_TYPE = 61

    def __init__(
        self,
        identity: IdentityType = None,
        peer_public_key: bytes = None,
        ecdsa_curve_name: str = None,
    ) -> None:
        self.identity = identity
        self.peer_public_key = peer_public_key
        self.ecdsa_curve_name = ecdsa_curve_name

    @classmethod
    def get_fields(cls):
        return {
            1: ('identity', IdentityType, 0),
            2: ('peer_public_key', p.BytesType, 0),
            3: ('ecdsa_curve_name', p.UnicodeType, 0),
        }
