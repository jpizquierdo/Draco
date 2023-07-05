from typing import NamedTuple


class Status(NamedTuple):
    """
    Status object to be shared in multiprocessing manager.
    """

    # HW GPIOs status
    waterpump: int = 0
    valve1: int = 0
    valve2: int = 0
    valve3: int = 0
    # mode status
    holidays: int = 0
