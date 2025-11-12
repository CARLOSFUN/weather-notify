# weather_live.py
# Purpose: Fetch current weather (F) for a city and print simple advice, then notify via Telegram.

import os
import sys
import requests  # pip install requests


def send_telegram(text: str) -> None:
    """Send a message to your Telegram chat using env vars."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        # Don’t crash if unset; just warn to stderr and continue.
        sys.stderr.write(
            "Telegram not configured (set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID).\n"
        )
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            try:
                j = resp.json()
                desc = j.get("description", "Unknown error")
            except Exception:
                desc = resp.text[:200]
            sys.stderr.write(f"Telegram send error ({resp.status_code}): {desc}\n")
    except requests.RequestException as e:
        sys.stderr.write(f"Telegram network error: {e}\n")


def get_api_key() -> str:
    """Read API key from environment (WEATHERAPI_KEY)."""
    key = os.getenv("WEATHERAPI_KEY")
    if not key:
        # Use stderr for clarity across environments
        sys.stderr.write("Error: WEATHERAPI_KEY is not set in your environment.\n")
        sys.exit(1)
    return key


def fetch_weather(city: str, api_key: str) -> dict:
    """
    Call WeatherAPI.com current weather endpoint.
    Returns a dict with expanded fields for display + advice.
    """
    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": city, "aqi": "no"}

    resp = requests.get(url, params=params, timeout=10)

    if resp.status_code != 200:
        try:
            j = resp.json()
            msg = j.get("error", {}).get("message", "Unknown error")
        except Exception:
            msg = resp.text[:200]
        sys.stderr.write(f"API error ({resp.status_code}): {msg}\n")
        sys.exit(1)

    data = resp.json()
    cur = data["current"]
    loc = data.get("location", {})

    # Build a friendly, explicit result dict (safe .get where fields may be missing)
    result = {
        "city_display": loc.get("name") or city,
        "country": loc.get("country"),
        "localtime": loc.get("localtime"),
        "temp_f": float(cur["temp_f"]),
        "feelslike_f": float(cur.get("feelslike_f", cur["temp_f"])),
        "condition": str(cur["condition"]["text"]).lower(),
        # Extras for richer output
        "humidity": cur.get("humidity"),
        "wind_mph": cur.get("wind_mph"),
        "wind_dir": cur.get("wind_dir"),
        "gust_mph": cur.get("gust_mph"),
        "precip_in": cur.get("precip_in"),
        "pressure_in": cur.get("pressure_in"),
        "uv": cur.get("uv"),
        "vis_miles": cur.get("vis_miles"),
        "last_updated": cur.get("last_updated"),
    }
    return result


def make_advice(temp_f: float, condition: str) -> list[str]:
    """Return a list of advice strings based on temp + condition."""
    advice: list[str] = []

    # Temperature rules (using feels-like when we call this)
    if temp_f < 25:
        advice.append("Very cold — heavy coat, gloves, and hat.")
    elif temp_f < 40:
        advice.append("It’s cold — wear a warm jacket.")
    elif temp_f < 60:
        advice.append("A bit cool — bring a light jacket or hoodie.")
    elif temp_f > 85:
        advice.append("Hot — hydrate and consider sunscreen.")
    else:
        advice.append("Feels mild — a t-shirt should be fine.")

    # Condition rules (allow multiple)
    if "snow" in condition:
        advice.append("It’s snowing — waterproof jacket and warm shoes.")
    if "rain" in condition:
        advice.append("Rain expected — bring an umbrella or rain jacket.")
    if "wind" in condition or "windy" in condition:
        advice.append("Windy — a windbreaker is recommended.")

    return advice


def _self_test() -> None:
    """Minimal tests (no network)."""
    # Temperature thresholds
    assert "heavy coat" in " ".join(make_advice(20, "clear")).lower()
    assert "warm jacket" in " ".join(make_advice(35, "clear")).lower()
    assert "hoodie" in " ".join(make_advice(55, "clear")).lower()
    assert "t-shirt" in " ".join(make_advice(70, "clear")).lower()
    assert "hydrate" in " ".join(make_advice(90, "clear")).lower()
    # Conditions layering
    adv = " ".join(make_advice(50, "rain and windy"))
    assert "umbrella" in adv and "windbreaker" in adv
    # Snow rule
    assert "snowing" in " ".join(make_advice(28, "snow")).lower()


def main() -> None:
    # Optional quick test runner (no extra deps)
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        _self_test()
        print("Self-test passed.")
        return

    city = input("City (press Enter for 'Misawa'): ").strip() or "Misawa"
    api_key = get_api_key()

    wx = fetch_weather(city, api_key)
    # Use feels-like for advice (closer to what you feel outdoors)
    advice = make_advice(wx["feelslike_f"], wx["condition"])

    # Rich console output
    print(f"\nCurrent weather in {wx['city_display']}, {wx.get('country','')}")
    print(f" - Local time:  {wx.get('localtime', 'N/A')}")
    print(
        f" - Temp:        {wx['temp_f']:.1f}°F (feels like {wx['feelslike_f']:.1f}°F)"
    )
    print(f" - Condition:   {wx['condition']}")
    print(f" - Humidity:    {wx.get('humidity','N/A')}%")
    print(
        f" - Wind:        {wx.get('wind_mph','N/A')} mph {wx.get('wind_dir','')}, gusts {wx.get('gust_mph','N/A')} mph"
    )
    print(
        f" - Precip:      {wx.get('precip_in','N/A')} in, Pressure: {wx.get('pressure_in','N/A')} inHg"
    )
    print(f" - Visibility:  {wx.get('vis_miles','N/A')} mi, UV: {wx.get('uv','N/A')}")
    print("\nAdvice:")
    print(" - " + "\n - ".join(advice))

    # Rich Telegram message
    msg_lines = [
        f"Weather in {wx['city_display']}, {wx.get('country','')}",
        f"Local time: {wx.get('localtime','N/A')}",
        "",
        f"Temp: {wx['temp_f']:.1f}°F (feels like {wx['feelslike_f']:.1f}°F)",
        f"Condition: {wx['condition']}",
        f"Humidity: {wx.get('humidity','N/A')}%",
        f"Wind: {wx.get('wind_mph','N/A')} mph {wx.get('wind_dir','')}, gusts {wx.get('gust_mph','N/A')} mph",
        f"Precip: {wx.get('precip_in','N/A')} in | Pressure: {wx.get('pressure_in','N/A')} inHg",
        f"Visibility: {wx.get('vis_miles','N/A')} mi | UV: {wx.get('uv','N/A')}",
        "",
        "Advice:",
        *[f"- {a}" for a in advice],
    ]
    send_telegram("\n".join(msg_lines))


if __name__ == "__main__":
    main()
