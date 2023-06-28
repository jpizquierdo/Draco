from time import sleep
import RPi.GPIO as GPIO
from enum import IntEnum, unique


@unique
class Channel(IntEnum):
    VALVE1 = 4 #J2
    VALVE2 = 22 #J3
    VALVE3 = 6 #J4
    VALVE4 = 26 #J5

class Times(IntEnum):
    WATER_S = 5 # watering time [s]


# GPIO setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(Channel.VALVE1, GPIO.OUT)
GPIO.setup(Channel.VALVE2, GPIO.OUT)
GPIO.setup(Channel.VALVE3, GPIO.OUT)
GPIO.setup(Channel.VALVE4, GPIO.OUT)
try:

    GPIO.output(Channel.VALVE1,True)
    GPIO.output(Channel.VALVE2,True)
    GPIO.output(Channel.VALVE3,True)
    GPIO.output(Channel.VALVE4,True)
    
    sleep(Times.WATER_S)
    GPIO.output(Channel.VALVE1,False)
    GPIO.output(Channel.VALVE2,False)
    GPIO.output(Channel.VALVE3,False)
    GPIO.output(Channel.VALVE4,False)
finally:
    GPIO.output(Channel.VALVE1,False)
    GPIO.output(Channel.VALVE2,False)
    GPIO.output(Channel.VALVE3,False)
    GPIO.output(Channel.VALVE4,False)
    GPIO.cleanup()