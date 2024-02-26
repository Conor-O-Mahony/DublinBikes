from flask import Flask, render_template
from dbManager import engine
from sqlalchemy import text

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/map')
def stations():
    try:
        # Connect to the database using the engine from dbManager
        with engine.connect() as connection:
            # Execute a query to fetch data from the table
            query = text("SELECT * FROM station")
            result = connection.execute(query)
            # Fetch all rows
            rows = result.fetchall()

            # Render the specific page template with the fetched data
            return render_template('map.html', rows=rows)

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)


