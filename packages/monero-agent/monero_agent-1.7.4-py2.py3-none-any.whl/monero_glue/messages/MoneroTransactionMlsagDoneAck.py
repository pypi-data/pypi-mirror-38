# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class MoneroTransactionMlsagDoneAck(p.MessageType):
    MESSAGE_WIRE_TYPE = 516

    def __init__(
        self,
        full_message_hash: bytes = None,
    ) -> None:
        self.full_message_hash = full_message_hash

    @classmethod
    def get_fields(cls):
        return {
            1: ('full_message_hash', p.BytesType, 0),
        }
