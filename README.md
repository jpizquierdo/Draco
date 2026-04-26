[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

# Draco

Draco is an automated plant watering system for Raspberry Pi. It controls a 4-relay shield to drive a water pump and up to three valves, with optional Telegram and MQTT integration for remote monitoring and control.

## Features

| Interface   | Required | Description |
|-------------|----------|-------------|
| **GPIO**    | Yes      | Controls the 4-relay shield (pump + valves) |
| **Scheduler** | Conditional | Time-based automatic watering (activated by default when Telegram/MQTT are disabled) |
| **Telegram** | No      | Remote commands and log streaming |
| **MQTT**    | No       | Integration with Home Assistant or any MQTT broker |

### Supported combinations

- `GPIO + Scheduler`
- `GPIO + Telegram`
- `GPIO + MQTT`
- `GPIO + Telegram + MQTT`
- `GPIO + Scheduler + Telegram + MQTT`

> **Note:** If neither Telegram nor MQTT is enabled, the scheduler activates automatically. Watering runs at the interval defined in `config.json` (first run after `holidays_frequency_days` days from start).

## Requirements

- Raspberry Pi (any model with GPIO)
- Python 3.9+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

### With uv (recommended)

```shell
git clone https://github.com/jpizquierdo/Draco.git
cd Draco
uv sync
```

### With pip

```shell
git clone https://github.com/jpizquierdo/Draco.git
cd Draco
python -m venv .venv
.venv/bin/pip install .
```

## Configuration

Copy and edit the example config:

```shell
cp config/config.json config/my_config.json
```

Key fields in `config.json`:

```json
{
  "telegram_bot": {
    "enable": true,
    "api": "YOUR_TELEGRAM_BOT_TOKEN",
    "allowed_users": { "name": "CHAT_ID" }
  },
  "relayshield": {
    "WaterPump": 4,
    "Valve1": 22,
    "Valve2": 6,
    "Valve3": 26
  },
  "scheduler": {
    "holidays_frequency_days": 3,
    "water_start_time_HH": "10",
    "water_start_time_MM": "00",
    "water_stop_time_HH": "10",
    "water_stop_time_MM": "02",
    "enable_alive_logging": false
  },
  "mqtt": {
    "enable": true,
    "broker_ip": "192.168.1.153",
    "broker_port": 1883
  }
}
```

GPIO pin numbers refer to BCM numbering.

## Usage

```shell
# With uv
uv run python draco.py -c config/config.json

# With activated venv
python draco.py -c config/config.json
```

## Running as a systemd Service

See [docs/systemd/how_to_systemd.md](docs/systemd/how_to_systemd.md).

## Home Assistant Integration

MQTT-based switch configuration and a custom Lovelace card are provided under [`docs/homeassistant/`](docs/homeassistant/).  
See [docs/homeassistant/readme.md](docs/homeassistant/readme.md) for setup instructions.

## Telegram Commands

See [docs/telegram_commands.md](docs/telegram_commands.md) for the full command list to register with @BotFather.

## Roadmap

- Moisture sensor support for demand-based watering
- DHT temperature and humidity sensor integration

## Contributing / Feedback

Open a [discussion](https://github.com/jpizquierdo/Draco/discussions/new) to ask questions, share your setup, or propose ideas.

## License

[MIT](LICENSE)
