.. :changelog:

History
-------

0.0.3 (2013-07-02)
++++++++++++++++++

- Telegram logging: Introducing Multiprocessing Queue for messages in shared memory between processes.
- All process log to telegram_queue.
- Add the commands of /valve1, /valve2 and /valve3 in ``telegram_interface.py`` to be able to interact with the rest of the relays.
- added a ``telegram_commands.rst`` in ``/docs`` with the commands to be introduced in GodFather inside telegram.
- ``HW_handler.py`` change name to ``GPIO_handler.py``

0.0.2 (2013-07-01)
++++++++++++++++++

- Shared variables: Introducing Multiprocessing Manager (with proxy dict and its locker) for sharing status variables between processes (not shared memory).
- Created the HW interface with the 4 relay shield, ``relay_shield_interface.py``, and interact with the PI2 GPIO.
- Updated ``telegram_interface.py`` with new method to interact with the relays. By the moment only /pump works. Also /status


0.0.1 (2023-06-30)
++++++++++++++++++

- Initial beta release, only with bot working