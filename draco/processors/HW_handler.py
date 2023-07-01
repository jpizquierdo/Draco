from multiprocessing import Process, Manager
from typing import Mapping, Type, Any
from time import sleep
import sys, os
import RPi.GPIO as GPIO
from draco.interfaces.relay_shield_interface import KS0212Interface

class HardwareHandler(Process):
    def __init__(
        self,
        config: Mapping[str, Any],
        memory_proxy: tuple,
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
        self._name = name
        #self._log_queue = log_queue
        #self._error_queue = error_queue

    def run(
        self
    ) -> None:
        success = False
        hwti = None
        pid = os.getpid()
        try:
            hwti = KS0212Interface(config=self._config, 
                                   memory_proxy=(self.system_status_proxy, self.system_status_lock), 
                                   name=self._name)
            while not success:
                success = hwti.init()
                sleep(0.1)
            print(f"'{self._name}' successfully initialized")
            while True:
                hwti.step() #Update GPIO values
                sleep(1)

        except Exception as error:
            print(f"Process {pid} - " + repr(error))
            success = False
        finally:
            pass

        exit_code = int(not success)
        sys.exit(exit_code)
