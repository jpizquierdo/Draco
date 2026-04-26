# Changelog

## 1.0.0 (2023-07-18)

- Home Assistant integration via MQTT (Mosquitto broker)
- MQTT switch configuration: `docs/homeassistant/mqtt_draco_watering.yaml`

## 0.0.7 (2023-07-17)

- Configurable watering start/stop times and frequency (days) via `config.json`
- Alive logging now conditional via `enable_alive_logging` config flag

## 0.0.6 (2023-07-09)

- Migrated from deprecated `telepot` to `python-telegram-bot`
- Added `[job-queue]` extra for asynchronous logging
- `telegram_bot.py` no longer blocks on `telegram_interface.init()`

## 0.0.5 (2023-07-05)

- Initial `python-telegram-bot` migration of `telegram_interface.py`

## 0.0.4 (2023-07-03)

- New `SystemScheduler` process for scheduling watering tasks
- Added `holidays` status tied to scheduler functions
- Documentation comments added across all source files

## 0.0.3 (2023-07-02)

- Multiprocessing `Queue` for Telegram log messages shared across processes
- All processes log to `telegram_queue`
- Added `/valve1`, `/valve2`, `/valve3` commands in `telegram_interface.py`
- Added `docs/telegram_commands.md`
- `HW_handler.py` renamed to `GPIO_handler.py`

## 0.0.2 (2023-07-01)

- Multiprocessing `Manager` (proxy dict + lock) for shared status variables
- `relay_shield_interface.py`: 4-relay shield interface for Raspberry Pi GPIO
- `telegram_interface.py`: `/pump` and `/status` commands

## 0.0.1 (2023-06-30)

- Initial beta release with Telegram bot
