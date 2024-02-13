from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
URI = 'dublinbikes.clw8uqmac8qf.eu-west-1.rds.amazonaws.com'
PORT = 3306
USER = 'admin'
DB = 'dbikes'

# Connect to the db
connection_string = f"mysql+mysqlconnector://{USER}:{DB_PASSWORD}@{URI}:{PORT}"
engine = create_engine(connection_string, echo=True)

# Testing
if engine.connect():
    print("Connection established successfully.")
else:
    print("Failed to establish connection.")


