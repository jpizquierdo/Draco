from typing import Mapping, Any
from multiprocessing import Queue
import os
import schedule
from time import sleep


class SchedulerInterface(object):
    def __init__(
        self,
        config: Mapping[str, Any] = {},
        memory_proxy: tuple = (),
        telegram_queue: Queue = None,
        name: str = "scheduler",
    ) -> None:
        """
        Telegram interface constructor.

         Parameters
         ----------
         config : Mapping[str, Any]
             Class configuration map.
         memory_proxy: tuple
             system_status_proxy
             system_status_lock
         telegram_queue : Queue
             telegram queue to send logging to main user
         name: str
             name in json file
        """
        config_draco = config.copy()
        if name in config:
            config_draco = config_draco[name]

        self._config = config_draco
        self.system_status_proxy = memory_proxy[0]
        self.system_status_lock = memory_proxy[1]
        self.telegram_queue = telegram_queue
        self._pid = os.getpid()
        self.current_holidays_state = None

    def init(
        self,
    ) -> bool:
        """
        This public function initialises the scheduler.

        Returns
        -------
        success : bool
            True if successful initialisation, False otherwise.
        """
        success = True
        try:
            self.current_holidays_state = self._check_status()["holidays"]
        except Exception as error:
            print(f"Process {self._pid} - " + repr(error))
            success = False
        return success

    def step(self) -> None:
        """
        This methods will check status and stop / run schedulers
        """
        # print(schedule.get_jobs())
        info = self._check_status()
        # Only setup the scheduler if value change
        if self.current_holidays_state != info["holidays"]:
            self.current_holidays_state = info["holidays"]
            self.setup_scheduler(info)
        schedule.run_pending()

    def setup_scheduler(self, info) -> None:
        """
        Function that is called in step, it setup the schedulers or remove them
        """
        if info["holidays"]:
            self._log(f"Setting the holidays schedulers:")
            # Alive logging to send messages to telegram
            if self._config["enable_alive_logging"]:
                self._log(f"- Alive logging at 09:00 and 22:00")
                schedule.every().day.at("22:00").do(self._alive_logging).tag(
                    "all", "holidays", "watchdog"
                )
                schedule.every().day.at("09:00").do(self._alive_logging).tag(
                    "all", "holidays", "watchdog"
                )
            self._log(
                f"- Summer watering each {self._config['holidays_frequency_days']} days starting at {self._config['water_start_time_HH']}:{self._config['water_start_time_MM']} and stoping at {self._config['water_stop_time_HH']}:{self._config['water_stop_time_MM']}"
            )
            schedule.every(self._config["holidays_frequency_days"]).days.at(
                f"{self._config['water_start_time_HH']}:{self._config['water_start_time_MM']}"
            ).do(self._summer_watering).tag("all", "holidays", "watchdog")
        else:
            self._log(f"Clearing the holidays schedulers")
            schedule.clear("holidays")

    def _check_status(self):
        """
        This method check the system status proxy
        """
        self.system_status_lock.acquire()
        info = self.system_status_proxy._getvalue()
        self.system_status_lock.release()
        return info

    def _alive_logging(self):
        self._log(f"Ey, I am alive.")
        # TODO send a webcam photo through telegram

    def _summer_watering(self):
        """
        Job that is triggered for watering during the summer
        """
        self._log(f"Summer watering scheduler")
        self._command_waterPump(value=1)
        self._command_valve(valve_number=2, value=1)
        # 15 minutes of watering TODO: put inside configuration
        schedule.every().day.at(
            f"{self._config['water_stop_time_HH']}:{self._config['water_stop_time_MM']}"
        ).do(self._command_waterPump, value=0)
        schedule.every().day.at(
            f"{self._config['water_stop_time_HH']}:{self._config['water_stop_time_MM']}"
        ).do(self._command_valve, valve_number=2, value=0)

    def _command_waterPump(self, value):
        """
        This method request the value of the pump to 'value'
        """
        self.system_status_lock.acquire()
        self.system_status_proxy["waterpump"] = value
        self.system_status_lock.release()
        self._log(f"Request Pump Status to {value}")
        if value == 0:
            return schedule.CancelJob

    def _command_valve(self, valve_number, value):
        """
        This method request the value of the valves 1, 2, 3 to 'value'
        """
        self.system_status_lock.acquire()
        self.system_status_proxy[f"valve{valve_number}"] = value
        self.system_status_lock.release()
        self._log(f"Request Valve {valve_number} Status to {value}")
        if value == 0:
            return schedule.CancelJob

    def _log(self, msg):
        """
        Logging function that queues message for telegram
        #TODO: will implement a python logger
        """
        self.telegram_queue.put(f"{__name__.split('.')[-1]}: {msg}")
