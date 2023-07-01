from typing import Mapping, Any
import os
import RPi.GPIO as GPIO
from enum import IntEnum, unique

@unique
class GPIO_Mode(IntEnum):
    NOT_SET = -1
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
        name: str = "relayshield"
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
        name : str
            json field name
        """
        config_draco = config.copy()
        if name in config:
            config_draco = config_draco[name]

        self._config = config_draco
        self.system_status_proxy = memory_proxy[0]
        self.system_status_lock = memory_proxy[1]
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
            if GPIO.getmode() == GPIO_Mode.NOT_SET:
                GPIO.setmode(GPIO.BCM)
            self._gpio_setup(**self._config)
            self.Channel = IntEnum('Channel', {"WATERPUMP" : self._config["WaterPump"],
                                               "VALVE1" : self._config["Valve1"],
                                               "VALVE2" : self._config["Valve2"],
                                               "VALVE3" : self._config["Valve3"],
                                               })

        except Exception as error:
            print(f"Process {self._pid} - " + repr(error))
            success = False

        return success
    
    def step(
        self,
    ) -> bool:
        success = True
        try:
            self.system_status_lock.acquire()
            info = self.system_status_proxy._getvalue()
            self.system_status_lock.release()
            print(info) #TODO: debug only
        except:
            success = False
        return success
    
    def _gpio_setup(self, **kwargs):
        for key in kwargs:
            GPIO.setup(kwargs[key], GPIO.OUT)
    
    def handle_relay(self, channel, value):
        GPIO.output(channel, value)
    
    def start_waterPump(self):
        GPIO.output(self.Channel.WATERPUMP, 1)

    def stop_waterPump(self):
        GPIO.output(self.Channel.WATERPUMP, 0)
    
    def start_valve1(self):
        GPIO.output(self.Channel.VALVE1, 1)

    def stop_valve1(self):
        GPIO.output(self.Channel.VALVE1, 0)
    
    def start_valve2(self):
        GPIO.output(self.Channel.VALVE2, 1)

    def stop_valve2(self):
        GPIO.output(self.Channel.VALVE2, 0)
    
    def start_valve3(self):
        GPIO.output(self.Channel.VALVE3, 1)

    def stop_valve3(self):
        GPIO.output(self.Channel.VALVE3, 0)
    
  