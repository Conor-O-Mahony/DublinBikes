from dotenv import load_dotenv
import os

load_dotenv("../../.env")

apiKey = os.getenv("BIKE_API_KEY")
contract = 'dublin'
STATIONS_URI = f"https://api.jcdecaux.com/vls/v3/stations"