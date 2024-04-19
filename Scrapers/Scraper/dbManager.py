from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv('../../.env')

DB_PASSWORD = os.getenv("DB_PASSWORD")
URI = 'dublinbikes.clw8uqmac8qf.eu-west-1.rds.amazonaws.com'
PORT = 3306
USER = 'admin'
DB = 'dbikes'

# Connect to the db
connection_string = f"mysql+mysqlconnector://{USER}:{DB_PASSWORD}@{URI}:{PORT}/{DB}"
engine = create_engine(connection_string, echo=True)


# Testing
try:
    connection = engine.connect()
    print("Connection established successfully.")

except Exception as e:
    print("Failed to establish connection:", e)
