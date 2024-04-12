from flask import Flask, render_template, jsonify
from dbManager import engine
from sqlalchemy import text
import requests
from datetime import datetime, timezone

from zoneinfo import ZoneInfo  

# conversion to Dublin time
utc_time = datetime.now(timezone.utc)
local_time = utc_time.astimezone(ZoneInfo("Europe/Dublin"))

import pickle
import pandas as pd
import numpy as np


# de-serialize model.pkl file into an object called model using pickle
from flask import Flask, jsonify, request
import os
import pickle




app = Flask(__name__)


from flask import Flask, request, jsonify
import pickle


# Load the pre-trained model
model_path = '/Users/okellyeneko/Documents/GitHub/DublinBikes/Models/pickle_files/bikes_1.pkl'  # Update with your actual model path
with open(model_path, 'rb') as handle:
    model = pickle.load(handle)

@app.route("/predict", methods=['GET'])
def predict():
    # Retrieve feature values from the query string
    try:
        temperature = request.args.get('temperature', default=0, type=float)
        wind_speed = request.args.get('wind_speed', default=0, type=float)
        rainfall = request.args.get('rainfall', default=0, type=float)
        day_of_week = request.args.get('day_of_week', default=0, type=int)
        hour = request.args.get('hour', default=0, type=int)
        minute = request.args.get('minute', default=0, type=int)
        broken_clouds = request.args.get('broken_clouds', default=0, type=int)
        clear_sky = request.args.get('clear_sky', default=0, type=int)
        few_clouds = request.args.get('few_clouds', default=0, type=int)
        fog = request.args.get('fog', default=0, type=int)
        haze = request.args.get('haze', default=0, type=int)
        heavy_intensity_rain = request.args.get('heavy_intensity_rain', default=0, type=int)
        light_rain = request.args.get('light_rain', default=0, type=int)
        mist = request.args.get('mist', default=0, type=int)
        moderate_rain = request.args.get('moderate_rain', default=0, type=int)
        overcast_clouds = request.args.get('overcast_clouds', default=0, type=int)
        scattered_clouds = request.args.get('scattered_clouds', default=0, type=int)
        thunderstorm_with_light_rain = request.args.get('thunderstorm_with_light_rain', default=0, type=int)
        
        # Assemble the features in the same order as the training set
        features = np.array([[
            temperature, wind_speed, rainfall, day_of_week, hour, minute,
            broken_clouds, clear_sky, few_clouds, fog, haze, heavy_intensity_rain,
            light_rain, mist, moderate_rain, overcast_clouds, scattered_clouds,thunderstorm_with_light_rain
        ]])
        
        # Predict using the loaded model
        prediction = model.predict(features)
        
        # Return prediction
        return jsonify({"prediction": prediction.tolist()})

    except Exception as e:
        # If an error occurs, return the error message
        return jsonify({"error": str(e)}), 400




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/forecast')
def forecast():
    # Foreacst placeholders and urls
    city = "Dublin,IE"
    api_key = "dd05f29b3c673dec7f4a9df4f8cce8fd"
    units = "metric"
    current_weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
    print(local_time)

    # Fetching the current weather info
    current_response = requests.get(current_weather_url)
    if current_response.status_code == 200:
        current_data = current_response.json()
        temp = current_data['main']['temp']
        desc = current_data['weather'][0]['description']
        wind = current_data['wind']['speed']
        rain = current_data.get('rain', {}).get('1h', 0)
        time = local_time.strftime("%Y-%m-%d %H:%M:%S")  # UTC now with timezone support
        icon = current_data['weather'][0]['icon']
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
                           icon=icon,
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


