# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore


class MoneroTransactionRsigData(p.MessageType):

    def __init__(
        self,
        rsig_type: int = None,
        offload_type: int = None,
        grouping: List[int] = None,
        mask: bytes = None,
        rsig: bytes = None,
        rsig_parts: List[bytes] = None,
    ) -> None:
        self.rsig_type = rsig_type
        self.offload_type = offload_type
        self.grouping = grouping if grouping is not None else []
        self.mask = mask
        self.rsig = rsig
        self.rsig_parts = rsig_parts if rsig_parts is not None else []

    @classmethod
    def get_fields(cls):
        return {
            1: ('rsig_type', p.UVarintType, 0),
            2: ('offload_type', p.UVarintType, 0),
            3: ('grouping', p.UVarintType, p.FLAG_REPEATED),
            4: ('mask', p.BytesType, 0),
            5: ('rsig', p.BytesType, 0),
            6: ('rsig_parts', p.BytesType, p.FLAG_REPEATED),
        }
