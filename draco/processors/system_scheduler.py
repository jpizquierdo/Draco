from multiprocessing import Process, Queue
from typing import Mapping, Any
from time import sleep
import sys, os
from draco.interfaces.scheduler_interface import SchedulerInterface


class SystemScheduler(Process):
    def __init__(
        self,
        config: Mapping[str, Any],
        memory_proxy: tuple,
        telegram_queue: Queue,
        name: str,
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
        telegram_queue : Queue
            telegram queue to send logging to main user
        name: str
            name in json file
        ----------
        """

        super().__init__()
        self._config = config.copy()
        self.system_status_proxy = memory_proxy[0]
        self.system_status_lock = memory_proxy[1]
        self.telegram_queue = telegram_queue
        self._name = name

    def run(self) -> None:
        success = False
        schedit = None
        pid = os.getpid()
        try:
            schedit = SchedulerInterface(
                config=self._config,
                memory_proxy=(self.system_status_proxy, self.system_status_lock),
                telegram_queue=self.telegram_queue,
                name=self._name,
            )
            while not success:
                success = schedit.init()
                sleep(0.2)
            print(f"'{self._name}' - {pid} successfully initialized")
            self.telegram_queue.put(
                f"Process {pid} \- '{self._name}' successfully initialized"
            )
            while True:
                # Update scheduler
                schedit.step()
                sleep(1)

        except Exception as error:
            print(f"Process {pid} - " + repr(error))
            success = False
        finally:
            pass

        exit_code = int(not success)
        sys.exit(exit_code)
