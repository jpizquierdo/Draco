.. :changelog:

History
-------

1.0.0 (2023-07-18)
++++++++++++++++++

- Updated version with homeAssistant integration using MQTT
- The broker selected in mosquitto mqtt broker
- Configuration of mqtt switches are inside ``docs/homeassistant/mqtt_draco_watering.yaml``

0.0.7 (2023-07-17)
++++++++++++++++++

- Update with custom starting and stoping time for the watering.
- Also the frequency in days. All from .json file.
- The alive logging has been conditionally with enable_alive_logging json file variable

0.0.6 (2023-07-09)
++++++++++++++++++

- Transition of telepot to python-telegram-bot. Telepot is deprecated and not robust and has to be changed. ``telegram_interface.py`` has been fully updated with new library.
- PTB (python-telegram-bot) has been changed to python-telegram-bot[job-queue] to be able to use the asynchrnous logging.
- ``telegram_bot.py`` process has been updated to not wait for the end of the telegram_interface.init(). This is an infinite loop now.

0.0.5 (2023-07-05)
++++++++++++++++++

- Initial version of the transition of telepot to python-telegram-bot. Telepot is deprecated and not robust and has to be changed. ``telegram_interface.py`` has been fully updated with new library.

0.0.4 (2023-07-03)
++++++++++++++++++

- New scheduler (``system_scheduler``) process to be able to schedule watering (or whatever).
- New status, holidays, associated with the scheduler functions.
- Some documentation comments in all the files.

0.0.3 (2023-07-02)
++++++++++++++++++

- Telegram logging: Introducing Multiprocessing Queue for messages in shared memory between processes.
- All process log to telegram_queue.
- Add the commands of /valve1, /valve2 and /valve3 in ``telegram_interface.py`` to be able to interact with the rest of the relays.
- added a ``telegram_commands.rst`` in ``/docs`` with the commands to be introduced in GodFather inside telegram.
- ``HW_handler.py`` change name to ``GPIO_handler.py``

0.0.2 (2023-07-01)
++++++++++++++++++

- Shared variables: Introducing Multiprocessing Manager (with proxy dict and its locker) for sharing status variables between processes (not shared memory).
- Created the HW interface with the 4 relay shield, ``relay_shield_interface.py``, and interact with the PI2 GPIO.
- Updated ``telegram_interface.py`` with new method to interact with the relays. By the moment only /pump works. Also /status


0.0.1 (2023-06-30)
++++++++++++++++++

- Initial beta release, only with bot working
