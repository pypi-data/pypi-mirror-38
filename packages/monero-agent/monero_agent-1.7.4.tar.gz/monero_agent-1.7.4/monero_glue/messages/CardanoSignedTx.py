# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class CardanoSignedTx(p.MessageType):
    MESSAGE_WIRE_TYPE = 310

    def __init__(
        self,
        tx_hash: bytes = None,
        tx_body: bytes = None,
    ) -> None:
        self.tx_hash = tx_hash
        self.tx_body = tx_body

    @classmethod
    def get_fields(cls):
        return {
            1: ('tx_hash', p.BytesType, 0),
            2: ('tx_body', p.BytesType, 0),
        }
