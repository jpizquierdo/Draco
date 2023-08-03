.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Introduction
============

Draco provides a python interface with your raspberry Pi in order to have an automated plant watering system for your holidays or daily.
It's compatible with Python versions **3.9+**.


Core functionality
============
- Telegram interface: Logging and commands
- Scheduler interface: Task scheduling
- MQTT interface: to be able to control it from homeassistant or any other MQTT device/service.
- GPIO interface: Control the relay shield interface

Only GPIO interface is mandatory.
MQTT and telegram interfaces are optional to be able to control and monitor the system, but not mandatory.
Scheduler interface is not mandatory if MQTT or telegram interface is selected. If not, the scheduler will be activated by default and no need to activate the holidays option. It will be working at the interval of ``config.json``. It means that when draco app starts, it will activate water_pump and valve1 at ``water_start_time_HH:water_start_time_MM`` till ``water_stop_time_HH:water_stop_time_MM with an interval`` of ``holidays_frequency_days`` (first execution in ``holidays_frequency_days`` days)

Combinations:
GPIO + scheduler
GPIO + Telegram
GPIO + MQTT
GPIO + Telegram + MQTT
GPIO + scheduler + Telegram + MQTT

Future functionality
============
- Webcam interface to be able to capture whatever you want and have it send to your telegram account or group.
- Watering plants by moisture sensors.
- Include a temperature and relative humidity sensor.

Installing
============
.. code:: shell

    $ git clone https://github.com/jpizquierdo/Draco.git
    $ cd Draco
    $ python -m venv .venv
    $ .venv/bin/pip install -r requirements.txt

Usage
============
.. code:: shell

    $ ~/Draco/.venv/bin/python ~/Draco/draco.py -c ~/Draco/config/config.json

Getting help or sharing your idea
============
Ask questions by opening `a discussion <https://github.com/jpizquierdo/Draco/discussions/new>`_. Or simply share your idea or your implementation in Show and tell.

License
============
`MIT <https://github.com/jpizquierdo/Draco/blob/main/LICENSE>`_