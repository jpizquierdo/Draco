from time import sleep
import RPi.GPIO as GPIO
from enum import IntEnum, unique
import adafruit_dht


@unique
class Channel(IntEnum):
    MOISTURE = 1
    VALVE = 2


class Times(IntEnum):
    WATER_S = 15  # watering time [s]
    INTERVAL_H = 48 * 60 * 60  # water interval [h]


# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Channel.MOISTURE, GPIO.IN)
GPIO.setup(Channel.VALVE, GPIO.OUT)

# dht setup
dhtDevice = adafruit_dht.DHT11(board.D18)


def get_temp():
    try:
        temperature_c = dhtDevice.temperature
        return temperature_c
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        sleep(2.0)
    except Exception as error:
        dhtDevice.exit()
        raise error


def get_humidity():
    try:
        humidity = dhtDevice.humidity
        return humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        sleep(2.0)
    except Exception as error:
        dhtDevice.exit()
        raise error


def main():
    try:
        while True:
            if GPIO.input(Channel.MOISTURE) == True:
                GPIO.output(Channel.VALVE, True)
                sleep(Times.WATER_S)
                GPIO.output(Channel.VALVE, False)
                sleep(Times.INTERVAL_H)
            else:
                sleep(1)
    finally:
        # cleanup the GPIO pins before ending
        GPIO.cleanup()


if __name__ == "__main__":
    main()
