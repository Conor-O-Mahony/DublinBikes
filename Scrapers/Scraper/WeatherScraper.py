import requests
from datetime import datetime
from sqlalchemy import create_engine, insert, text, MetaData, Table, Column, Integer, String, Float, TIMESTAMP
import dbManager




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
    wind = weather_data['wind']['speed']
    if 'rain' in weather_data and '1h' in weather_data['rain']:
        rain = weather_data['rain']['1h']
    else:
        rain = 0
    time = datetime.now()
else:
    print("Weather data retrieval failed.")

def insert_weather():

    metadata = MetaData()

    current_weather = Table(
        'currentweather',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('temperature', Float),
        Column('description', String),
        Column('wind_speed', Float),
        Column('rainfall', Float),
        Column('timestamp', TIMESTAMP, default=text('CURRENT_TIMESTAMP'))
    )
    try:
        with dbManager.engine.connect() as conn:
            trans = conn.begin()
            ins = current_weather.insert().values(
                temperature=temp,
                description=desc,
                wind_speed=wind,
                rainfall=rain,
                timestamp=time
            )
            conn.execute(ins)
            trans.commit()
            print("Weather data inserted successfully.")
    except Exception as e:
        if trans:
            trans.rollback()
        print("Error occurred while inserting data:", e)


        
fetch_weather()
insert_weather()
