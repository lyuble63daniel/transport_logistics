import requests

OPENWEATHER_API_KEY = "84e4e01bf5439e599f67c9a99fdb0d07"  # 🔁 Replace this with your real key

def get_weather(city):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": data["main"]["temp"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"],
                "city": data["name"]
            }
        else:
            return None
    except Exception as e:
        print("🌩️ Weather fetch error:", e)
        return None
