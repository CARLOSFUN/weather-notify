# Weather Notify ☁️

Fetches live weather data (°F) via [WeatherAPI](https://www.weatherapi.com) and sends simple outfit advice to your phone through [Telegram Bot API](https://core.telegram.org/bots/api).

---

## 🚀 Quick Start

```bash
git clone https://github.com/CARLOSFUN/weather-notify.git
cd weather-notify
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
set -a; source .env; set +a
python3 weather_live.py

