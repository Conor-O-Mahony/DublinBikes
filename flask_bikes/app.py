from flask import Flask, render_template, jsonify
from dbManager import engine
from sqlalchemy import text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')


@app.route('/stations')
def station():
    return render_template('stations.html')

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


