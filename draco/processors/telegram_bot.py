from multiprocessing import Process, Queue
from typing import Mapping, Type, Any
from time import sleep
import sys, os
from draco.interfaces.telegram_interface import TelegramInterface

class TelegramBot(Process):
    def __init__(
        self,
        config: Mapping[str, Any],
        #log_queue: Type[Queue],
        #error_queue: Type[Queue]
    ) -> None:
        """
        Data consumer constructor.

        Parameters
        ----------
        config : Mapping[str, Any]
            Consumer static configuration.
        log_queue : Type[Queue]
            Logging queue. Queue where logging messages go.
        error_queue : Type[Queue]
            Error queue. Queue used to control whether error has been produced
            in process.
        ----------
        """

        super().__init__()
        self._config = config.copy()
        #self._log_queue = log_queue
        #self._error_queue = error_queue

    def run(
        self
    ) -> None:
        success = False
        teleti = None
        pid = os.getpid()
        try:
            teleti = TelegramInterface(config=self._config)
            while not success:
                success = teleti.init()
                sleep(0.1)
            print("telegram bot successfully initialized")
            while True:
                sleep(10)

        except Exception as error:
            pid = os.getpid()
            print(f"Process {pid} - " + repr(error))
            success = False
        finally:
            pass # close telegram bot

        exit_code = int(not success)
        sys.exit(exit_code)