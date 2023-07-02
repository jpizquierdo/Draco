from multiprocessing import Process, Queue
from typing import Mapping, Any
from time import sleep
import sys, os
from draco.interfaces.relay_shield_interface import KS0212Interface

class GPIOHandler(Process):
    def __init__(
        self,
        config: Mapping[str, Any],
        memory_proxy: tuple,
        telegram_queue: Queue,
        name: str
        #log_queue: Type[Queue],
        #error_queue: Type[Queue]
    ) -> None:
        """
        Data consumer constructor.

        Parameters
        ----------
        config : Mapping[str, Any]
            Consumer static configuration.
        memory_proxy: tuple
            system_status_proxy
            system_status_lock
        name: str
        ----------
        """

        super().__init__()
        self._config = config.copy()
        self.system_status_proxy = memory_proxy[0]
        self.system_status_lock = memory_proxy[1]
        self.telegram_queue = telegram_queue
        self._name = name
        #self._log_queue = log_queue
        #self._error_queue = error_queue

    def run(
        self
    ) -> None:
        success = False
        relayit = None
        pid = os.getpid()
        try:
            relayit = KS0212Interface(config=self._config, 
                                   memory_proxy=(self.system_status_proxy, self.system_status_lock), 
                                   telegram_queue=self.telegram_queue,
                                   name=self._name)
            while not success:
                success = relayit.init()
                sleep(0.1)
            print(f"'{self._name}' successfully initialized")
            self.telegram_queue.put(f"'{self._name}' successfully initialized")
            while True:
                relayit.step() #Update GPIO values
                sleep(1)

        except Exception as error:
            print(f"Process {pid} - " + repr(error))
            success = False
        finally:
            pass

        exit_code = int(not success)
        sys.exit(exit_code)
