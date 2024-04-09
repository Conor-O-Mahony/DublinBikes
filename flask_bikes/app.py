from flask import Flask, render_template, jsonify
from dbManager import engine
from sqlalchemy import text
import requests
from datetime import datetime, timezone

from zoneinfo import ZoneInfo  

# conversion to Dublin time
utc_time = datetime.now(timezone.utc)
local_time = utc_time.astimezone(ZoneInfo("Europe/Dublin"))





app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/forecast')
def forecast():
    # Foreacst placeholders and urls
    city = "Dublin"
    api_key = "dd05f29b3c673dec7f4a9df4f8cce8fd"
    units = "metric"
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"

    # Fetching the current weather info
    current_response = requests.get(current_weather_url)
    if current_response.status_code == 200:
        current_data = current_response.json()
        temp = current_data['main']['temp']
        desc = current_data['weather'][0]['description']
        wind = current_data['wind']['speed']
        rain = current_data.get('rain', {}).get('1h', 0)
        time = local_time.strftime("%Y-%m-%d %H:%M:%S")  # UTC now with timezone support
    else:
        return render_template('forecast.html', error="Failed to fetch current weather data.")

    # Fetching the forecast
    forecast_response = requests.get(forecast_url)
    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
        forecasts = forecast_data['list']

        # Daily forecasts
        daily_forecasts = []
        seen_dates = set()
        for entry in forecasts:
            forecast_date = datetime.fromtimestamp(entry['dt'], tz=timezone.utc).date()
            if forecast_date not in seen_dates:
                seen_dates.add(forecast_date)
                entry['display_date'] = forecast_date.strftime("%A, %B %d")
                daily_forecasts.append(entry)

    else:
        return render_template('forecast.html', error="Failed to fetch forecast data.")

    # template with all data
    return render_template('forecast.html', 
                           temp=temp, 
                           desc=desc, 
                           wind=wind, 
                           rain=rain, 
                           time=time, 
                           hourly_forecasts=forecasts[:8], # Number of rows to show
                           daily_forecasts=daily_forecasts)

@app.route('/map')
def stations():
    try:
        with engine.connect() as connection:
        
            query = text("""SELECT station.number, status, bikes, stands, mechanicalBikes, electricalBikes, electricalInternalBatteryBikes, electricalRemovableBatteryBikes, address, banking, capacity, bonus, name, position_lat, position_lng, lastUpdate
                             FROM
                                availability, station
                             WHERE
                                timestamp = (SELECT MAX(timestamp) FROM dbikes.availability) AND availability.number = station.number
                             ORDER BY number;""")
            
            result = connection.execute(query)
            rows = result.fetchall()
            
            # Convert rows to a list of dictionaries
            stations = [{"number": row.number,
                        "lat": row.position_lat,
                        "lng": row.position_lng,
                        "name": row.name,
                        "address": row.address,
                        "card": row.banking,
                        "status": row.status, 
                        "bikes": row.bikes, 
                        "stands": row.stands, 
                        "mechbikes": row.mechanicalBikes, 
                        "elecbikes": row.electricalBikes, 
                        "elecinternal": row.electricalInternalBatteryBikes, 
                        "elecremoveable": row.electricalRemovableBatteryBikes, 
                        "lastupdate": row.lastUpdate} 
                        for row in rows]

            # Pass the stations data to the template
            return render_template('map.html', data=stations)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True)


