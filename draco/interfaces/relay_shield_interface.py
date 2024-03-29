from typing import Mapping, Any
from multiprocessing import Queue
import os
import RPi.GPIO as GPIO
from enum import IntEnum, unique


@unique
class GPIO_Mode(IntEnum):
    BCM_MODE = 11
    BOARD_MODE = 10


class KS0212Interface(object):
    """
    KS0212 keyestudio RPI 4-channel Relay Shield interface.

    Specification:
    ----------
    Control Signal: TTL Level
    Rated Load:
        10A 250VAC
        10A 125VAC
        10A 30VDC
        10A 28VDC
    Rated Current: 10A(NO) 5A(NC)
    Max Switching Voltage: 250VAC 30VDC
    Contact Time: under 10ms


    Pinout:
    ----------
    BCM pin mode
    J2 GPIO pin: 4
    J3 GPIO pin: 22
    J4 GPIO pin: 6
    J5 GPIO pin: 26


    https://wiki.keyestudio.com/KS0212_keyestudio_RPI_4-channel_Relay_Shield
    """

    def __init__(
        self,
        config: Mapping[str, Any] = {},
        memory_proxy: tuple = (),
        telegram_queue: Queue = None,
        name: str = "relayshield",
    ) -> None:
        """
        KS0212 keyestudio RPI 4-channel Relay Shield interface constructor.

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
        self.Channel = None

    def init(
        self,
    ) -> bool:
        """
        This public function initialises the configuration of the GPIO.

        Returns
        -------
        success : bool
            True if successful initialisation, False otherwise.
        """

        success = True

        try:
            # GPIO setup
            if GPIO.getmode() == None:
                GPIO.setmode(GPIO.BCM)
            self._gpio_setup(**self._config)
            self.Channel = IntEnum(
                "Channel",
                {
                    "WATERPUMP": self._config["WaterPump"],
                    "VALVE1": self._config["Valve1"],
                    "VALVE2": self._config["Valve2"],
                    "VALVE3": self._config["Valve3"],
                },
            )

        except Exception as error:
            print(f"Process {self._pid} - " + repr(error))
            success = False

        return success

    def step(
        self,
    ) -> bool:
        """
        Step function to update the Relays status.

        Returns
        -------
        success : bool
            True if successful initialisation, False otherwise.
        """
        success = True
        try:
            self.system_status_lock.acquire()
            info = self.system_status_proxy._getvalue()
            self.system_status_lock.release()
            self.handle_relay(self.Channel.WATERPUMP, info["waterpump"])
            self.handle_relay(self.Channel.VALVE1, info["valve1"])
            self.handle_relay(self.Channel.VALVE2, info["valve2"])
            self.handle_relay(self.Channel.VALVE3, info["valve3"])
        except:
            success = False
        return success

    def _gpio_setup(self, **kwargs) -> None:
        """
        This method setup as outputs the GPIOs from the json config file.

        Parameters
        ----------
        **config : Dict
        """
        for key in kwargs:
            GPIO.setup(kwargs[key], GPIO.OUT)

    def handle_relay(self, channel, value):
        """
        Method to handle the relay. It only takes effect if the GPIO HW value has changed.

        Parameters
        ----------
        channel : int
            Channel integer value. Usually from intenum self.Channel
        value : int
            1 means set to high, while 0 means set to low
        """
        # only handles the GPIO HW if the value has changed.
        if GPIO.input(channel) != value:
            GPIO.output(channel, value)
            self._log(f"{channel.name} set to {value}")

    def start_waterPump(self):
        """
        Set to 1 GPIO waterpump
        """
        GPIO.output(self.Channel.WATERPUMP, 1)
        self._log(f"{self.Channel.WATERPUMP.name} set to 1")

    def stop_waterPump(self):
        """
        Set to 0 GPIO waterpump
        """
        GPIO.output(self.Channel.WATERPUMP, 0)
        self._log(f"{self.Channel.WATERPUMP.name} set to 0")

    def start_valve1(self):
        """
        Set to 1 GPIO valve1
        """
        GPIO.output(self.Channel.VALVE1, 1)
        self._log(f"{self.Channel.VALVE1.name} set to 1")

    def stop_valve1(self):
        """
        Set to 0 GPIO valve1
        """
        GPIO.output(self.Channel.VALVE1, 0)
        self._log(f"{self.Channel.VALVE1.name} set to 0")

    def start_valve2(self):
        """
        Set to 1 GPIO valve2
        """
        GPIO.output(self.Channel.VALVE2, 1)
        self._log(f"{self.Channel.VALVE2.name} set to 1")

    def stop_valve2(self):
        """
        Set to 0 GPIO valve2
        """
        GPIO.output(self.Channel.VALVE2, 0)
        self._log(f"{self.Channel.VALVE2.name} set to 0")

    def start_valve3(self):
        """
        Set to 1 GPIO valve3
        """
        GPIO.output(self.Channel.VALVE3, 1)
        self._log(f"{self.Channel.VALVE3.name} set to 1")

    def stop_valve3(self):
        """
        Set to 0 GPIO valve3
        """
        GPIO.output(self.Channel.VALVE3, 0)
        self._log(f"{self.Channel.VALVE3.name} set to 0")

    def _log(self, msg):
        """
        Logging function that queues message for telegram
        #TODO: will implement a python logger
        """
        self.telegram_queue.put(f"{__name__.split('.')[-1]}: {msg}")
