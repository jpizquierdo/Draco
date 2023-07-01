from typing import NamedTuple

class Status(NamedTuple):
    """
    Status object to be shared in multiprocessing manager.
    """
    waterpump: int = -1
    valve1: int = -1
    valve2: int = -1
    valve3: int = -1

