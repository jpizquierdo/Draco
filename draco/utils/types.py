from typing import NamedTuple

class Status(NamedTuple):
    """
    Status object to be shared in multiprocessing manager.
    """
    waterpump: int = 0
    valve1: int = 0
    valve2: int = 0
    valve3: int = 0

