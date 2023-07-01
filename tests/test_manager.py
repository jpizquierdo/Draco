from time import sleep
from multiprocessing import Manager, Process
from typing import NamedTuple

class Status(NamedTuple):
    """
    Status object to be shared in multiprocessing manager.
    """
    waterpump: int = -1
    valve1: int = -1
    valve1: int = -1
    valve3: int = -1

def print_values(my_lock, status_proxy):
    while True:
        my_lock.acquire()
        info = status_proxy._getvalue()
        my_lock.release()
        for key in info:
            print(f"{key}:      {status_proxy[key]}")
        sleep(0.1)
  
def modify_waterpump(my_lock, status_proxy):
    while True:
        my_lock.acquire()
        if status_proxy["waterpump"] == 0:
            status_proxy["waterpump"] = 1
        else:
            status_proxy["waterpump"] = 0
        my_lock.release()

        sleep(0.3)


if __name__ == '__main__':
    my_dict = Status()
    my_dict = my_dict._asdict()


    manager = Manager() # create a manager
    status_proxy = manager.dict(my_dict) # create a proxy dict
    my_lock = manager.Lock() #create lock object to be able to operate with the status proxy in multiprocess (read and write in multiple process without memory breaking)

    # creating new processes
    p1 = Process(target=modify_waterpump, args=(my_lock, status_proxy))
    p2 = Process(target=print_values, args=(my_lock, status_proxy))

    p1.start()
    p2.start()
    p1.join()
    p2.join()
