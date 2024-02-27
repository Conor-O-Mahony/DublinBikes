from flask import Flask, render_template, jsonify
from dbManager import engine
from sqlalchemy import text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/map')
def stations():
    try:
        with engine.connect() as connection:
            query = text("SELECT * FROM station")
            result = connection.execute(query)
            rows = result.fetchall()

            # Convert rows to a list of dictionaries
            stations = [{"lat": row.position_lat, "lng": row.position_lng, "title": row.name} for row in rows]

            # Pass the stations data to the template
            return render_template('map.html', stationsData=stations)
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True)


