
import json
import requests
import dbinfo
from sqlalchemy import create_engine, insert, text, MetaData, Table, Column, Integer, String, Boolean, Float, Enum, TIMESTAMP
import dbManager
from datetime import datetime

params = {"contract": dbinfo.contract, "apiKey": dbinfo.apiKey}

try:
    r = requests.get(dbinfo.STATIONS_URI, params=params)
    r.raise_for_status()  
    stations = r.json()

except requests.exceptions.RequestException as e:
    print("Error:", e)



def insert_availability(stations):

    metadata = MetaData()

    availability = Table(
        'availability',
        metadata,
        Column('availability_id', Integer, primary_key=True),
        Column('number', Integer),
        Column('status', Enum('OPEN', 'CLOSED')),
        Column('available_bikes', Integer),
        Column('available_bike_stands', Integer),
        Column('last_update', TIMESTAMP),
        Column('timestamp', TIMESTAMP, default=text('CURRENT_TIMESTAMP')), 
    )
    

    with dbManager.engine.connect() as conn:
        
        trans = conn.begin()
        
        try:
            values_list = []
            for station_data in stations:
                    last_update_timestamp = station_data['last_update'] / 1000  
                    last_update_datetime = datetime.fromtimestamp(last_update_timestamp)
                    status = station_data['status'].upper()  
                    values_list.append({
                        'number': station_data['number'],
                        'status': status,
                        'available_bikes': station_data['available_bikes'],
                        'available_bike_stands': station_data['available_bike_stands'],
                        'last_update': last_update_datetime,
                })
        
            conn.execute(
                insert(availability),
                values_list
            )

            trans.commit()
            print(f"Added {len(stations)} availability rows into the database")

        except Exception as e:
            
            trans.rollback()
            print("Error occurred while inserting availability data:", e)

insert_availability(stations)





