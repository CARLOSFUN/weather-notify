# 🌦️ Weather Notify — Daily Weather Alerts via Telegram

A simple Python app that fetches live weather data from [WeatherAPI.com](https://www.weatherapi.com) and sends personalized outfit or activity advice directly to your Telegram every morning.

Perfect beginner-friendly project for learning **APIs, environment variables, and automation** — all in one small, practical tool.

---

## ✨ Features

* 🌤️ Fetches **real-time weather data** using WeatherAPI
* 📬 Sends weather updates and advice straight to your **Telegram** chat
* 🌡️ Displays temperature, humidity, wind speed, pressure, UV index, and more
* 🧥 Provides **smart outfit suggestions** based on current conditions
* ⚙️ Configurable for any location (defaults to Misawa, Japan)
* 🔒 Keeps all API keys **secure with `.env` environment variables**
* 🧠 Includes a built-in self-test (`--self-test`) for debugging

---

## 🧰 Tech Stack

| Component                          | Description                          |
| ---------------------------------- | ------------------------------------ |
| **Python 3.10+**                   | Main programming language            |
| **Requests**                       | Used for making HTTP API calls       |
| **WeatherAPI**                     | Source of real-time weather data     |
| **Telegram Bot API**               | Sends messages directly to your chat |
| **dotenv / Environment Variables** | Keeps secrets secure and private     |

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<yourusername>/weather-notify.git
cd weather-notify
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Copy the Environment Example File

```bash
cp .env.example .env
```

---

## 🔐 How to Add Your API Keys

To keep your keys secure, this app uses a hidden `.env` file to store sensitive information.

### Step 1: Edit the `.env` file

```bash
open -e .env
```

Paste your real API keys and IDs like this:

```bash
WEATHERAPI_KEY=your_real_weatherapi_key
TELEGRAM_BOT_TOKEN=your_real_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
DEFAULT_CITY=Misawa
```

* 🔑 Get your WeatherAPI key here: [WeatherAPI.com → My Account → API Keys](https://www.weatherapi.com/my/)
* 🤖 Create your Telegram bot with [@BotFather](https://t.me/botfather)
* 🆔 To find your `TELEGRAM_CHAT_ID`, message your bot and visit:
  `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

---

### Step 2: Load the Environment Variables

Every new terminal session, run:

```bash
set -a; source .env; set +a
```

This loads your keys into memory so Python can read them via `os.getenv()`.

---

### Step 3: Run the App

```bash
python3 weather_live.py
```

Then check your Telegram — you’ll receive the weather update instantly!

---

## 🕕 Optional: Schedule Daily Messages

To get your weather update every morning at **06:00**, use **macOS Automator** or **cron**.

### Example: Schedule via `crontab`

1. Open cron editor:

   ```bash
   crontab -e
   ```
2. Add this line:

   ```bash
   0 6 * * * cd /Users/carlosfunez/Desktop/weather-notify && set -a; source .env; set +a; /usr/local/bin/python3 weather_live.py
   ```
3. Save and exit.
   This runs your script every day at 6:00 AM.

---

## 🧾 Example Output

**Terminal:**

```
Current weather in Misawa, Japan
 - Local time: 2025-11-12 06:00
 - Temp: 38.5°F (feels like 33.2°F)
 - Condition: cloudy
 - Humidity: 72%
 - Wind: 9 mph NW, gusts 15 mph
 - Precip: 0.0 in, Pressure: 29.9 inHg
 - Visibility: 8 mi, UV: 1

Advice:
 - It’s cold — wear a warm jacket.
 - Windy — a windbreaker is recommended.
```

**Telegram:**

```
Weather in Misawa, Japan
Local time: 2025-11-12 06:00

Temp: 38.5°F (feels like 33.2°F)
Condition: cloudy
Humidity: 72%
Wind: 9 mph NW, gusts 15 mph
Precip: 0.0 in | Pressure: 29.9 inHg
Visibility: 8 mi | UV: 1

Advice:
- It’s cold — wear a warm jacket.
- Windy — a windbreaker is recommended.
```

---

## 📁 Repository Structure

```
weather-notify/
├── weather_live.py        # Main Python script
├── requirements.txt       # Dependencies list
├── .env.example           # Example environment variables
├── .gitignore             # Ignores .env, venv, etc.
├── LICENSE                # MIT License
└── README.md              # Documentation (this file)
```

---

## ⚙️ requirements.txt

```bash
# Weather Notify dependencies
requests==2.31.0
```

---

## 🧠 How It Works (Concept Overview)

1. **Reads API keys** from `.env` using `os.getenv()`
2. **Calls WeatherAPI** endpoint (`/v1/current.json`) to get current conditions
3. **Parses** temperature, humidity, wind, UV, and precipitation data
4. **Generates outfit advice** based on temperature & condition
5. **Sends formatted message** to your Telegram bot using Telegram’s HTTP API

This project teaches:

* API calls (`requests.get`)
* Error handling with status codes
* Environment variable management
* Secure key storage
* Basic automation via cron jobs
* JSON parsing and conditional logic in Python

---

## 🧩 Self-Test Mode

You can verify your logic without making API calls:

```bash
python3 weather_live.py --self-test
```

If everything passes, you’ll see:

```
Self-test passed.
```

---

## 🛡️ Security Best Practices

* `.env` is listed in `.gitignore` — never upload it to GitHub
* Use `chmod 600 .env` to make it readable only by you
* Rotate your keys if you ever share screenshots or push sensitive info
* Avoid printing your API keys in logs or terminal output

---

## 📄 License

This project is licensed under the **MIT License** — you’re free to use, modify, and share it with credit.

---

## 💬 Author

👤 **Carlos Funezsanchez**
📍 Misawa, Japan
💼 Aspiring Linux & Cloud Engineer
📫 [LinkedIn Profile](https://www.linkedin.com/in/yourusername/)
🌐 Portfolio: *coming soon*

---

Would you like me to add a **polished “Project Overview” image banner** (like a screenshot preview of the Telegram message with weather icons) to make your GitHub page look even more professional? I can help you design and add that next.



