from multiprocessing import Process
from typing import Mapping, Any
from multiprocessing import Queue
from time import sleep
import sys, os
from draco.interfaces.telegram_interface import TelegramInterface

class TelegramBot(Process):
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
        teleti = None
        pid = os.getpid()
        try:
            teleti = TelegramInterface(config=self._config, 
                                       memory_proxy=(self.system_status_proxy, self.system_status_lock), 
                                       telegram_queue=self.telegram_queue, 
                                       name=self._name)
            while not success:
                success = teleti.init()
                sleep(0.1)
            print(f"telegram bot '{self._name}' successfully initialized")
            self.telegram_queue.put(f"telegram bot '{self._name}' successfully initialized")
            while True:
                teleti.step_log()
                sleep(0.2)

        except Exception as error:
            print(f"Process {pid} - " + repr(error))
            success = False
        finally:
            pass # close telegram bot

        exit_code = int(not success)
        sys.exit(exit_code)