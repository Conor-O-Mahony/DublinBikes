from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv('db.env')

DB_PASSWORD = os.getenv("DB_PASSWORD")
URI = 'dublinbikes.clw8uqmac8qf.eu-west-1.rds.amazonaws.com'
PORT = 3306
USER = 'admin'
DB = 'dbikes'

# Connect to the db
connection_string = f"mysql+mysqlconnector://{USER}:{DB_PASSWORD}@{URI}:{PORT}/{DB}"
engine = create_engine(connection_string, echo=True)

# SQL statements
sql_create = text("""
CREATE TABLE IF NOT EXISTS availability (
    number INTEGER,
    available_bikes INTEGER,
    available_bike_stands INTEGER,
    last_update INTEGER
);
""")

sql_drop = text("DROP TABLE IF EXISTS availability;")

# Testing
try:
    connection = engine.connect()
    print("Connection established successfully.")
    
    # Drop existing table (if any)
    result = connection.execute(sql_drop)
    print("Table dropped successfully.")

    # Create table
    result = connection.execute(sql_create)
    print("Table created successfully.")

    connection.close()  # Close the connection after use
except Exception as e:
    print("Failed to establish connection:", e)
