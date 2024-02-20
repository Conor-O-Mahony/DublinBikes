
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
        Column('bikes', Integer),
        Column('stands', Integer),
        Column('mechanicalBikes', Integer),
        Column('electricalBikes', Integer),
        Column('electricalInternalBatteryBikes', Integer),
        Column('electricalRemovableBatteryBikes', Integer),
        Column('lastUpdate', TIMESTAMP),
        Column('timestamp', TIMESTAMP, default=text('CURRENT_TIMESTAMP')), 
    )
    
    with dbManager.engine.connect() as conn:
        
        trans = conn.begin()
        
        try:
            values_list = []
            for station_data in stations:
                    last_update_timestamp = station_data['lastUpdate']
                    last_update_datetime = datetime.strptime(last_update_timestamp, '%Y-%m-%dT%H:%M:%SZ')
                    status = station_data['status'].upper()  
                    values_list.append({
                        'number': station_data['number'],
                        'status': status,
                        'bikes': station_data ['totalStands']['availabilities']['bikes'],
                        'stands': station_data['totalStands']['availabilities']['stands'],
                        'mechanicalBikes': station_data['totalStands']['availabilities']['mechanicalBikes'],
                        'electricalBikes': station_data['totalStands']['availabilities']['electricalBikes'],
                        'electricalInternalBatteryBikes': station_data['totalStands']['availabilities']['electricalInternalBatteryBikes'],
                        'electricalRemovableBatteryBikes': station_data['totalStands']['availabilities']['electricalRemovableBatteryBikes'],
                        'lastUpdate': last_update_datetime,
                })
        
            try:
                conn.execute(
                    insert(availability),
                    values_list
                )
            except: #This is to catch errors that may occur if new station is added to the API

                with open("scraper.py") as f: #re-scrape the static data
                    exec(f.read())

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





