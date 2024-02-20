import requests
from datetime import datetime

def fetch_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=dublin&appid=63b3042347926a25ee5ba9062aa724c0&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch weather data:", response.status_code)
        return None

weather_data = fetch_weather()
if weather_data:
    temp = weather_data['main']['temp']
    desc = weather_data['weather'][0]['description']
    main = weather_data['weather']['main']
    wind = weather_data['wind']['speed']
    rain = weather_data['rain']['1h']
    time = datetime.now()
else:
    print("Weather data retrieval failed.")

fetch_weather()
