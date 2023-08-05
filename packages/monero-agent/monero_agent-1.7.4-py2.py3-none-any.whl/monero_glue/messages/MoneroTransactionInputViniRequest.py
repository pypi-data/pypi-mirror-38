# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

from .MoneroTransactionSourceEntry import MoneroTransactionSourceEntry


class MoneroTransactionInputViniRequest(p.MessageType):
    MESSAGE_WIRE_TYPE = 507

    def __init__(
        self,
        src_entr: MoneroTransactionSourceEntry = None,
        vini: bytes = None,
        vini_hmac: bytes = None,
        pseudo_out: bytes = None,
        pseudo_out_hmac: bytes = None,
    ) -> None:
        self.src_entr = src_entr
        self.vini = vini
        self.vini_hmac = vini_hmac
        self.pseudo_out = pseudo_out
        self.pseudo_out_hmac = pseudo_out_hmac

    @classmethod
    def get_fields(cls):
        return {
            1: ('src_entr', MoneroTransactionSourceEntry, 0),
            2: ('vini', p.BytesType, 0),
            3: ('vini_hmac', p.BytesType, 0),
            4: ('pseudo_out', p.BytesType, 0),
            5: ('pseudo_out_hmac', p.BytesType, 0),
        }
