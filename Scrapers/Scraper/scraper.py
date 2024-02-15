
import json
import requests
import dbinfo
from sqlalchemy import create_engine, insert, text, MetaData, Table, Column, Integer, String, Boolean, Float
import dbManager

params = {"contract": dbinfo.contract, "apiKey": dbinfo.apiKey}

try:
    r = requests.get(dbinfo.STATIONS_URI, params=params)
    r.raise_for_status()  
    stations = r.json()

except requests.exceptions.RequestException as e:
    print("Error:", e)

def insert_stations(stations):

    metadata = MetaData()

    station = Table(
        'station',
        metadata,
        Column('number', Integer, primary_key=True),
        Column('address', String),
        Column('banking', Boolean),
        Column('capacity', Integer), 
        Column('bonus', Boolean),
        Column('contractName', String), 
        Column('name', String),
        Column('position_lat', Float),
        Column('position_lng', Float),
        Column('connected', Boolean),
        Column('overflow', Boolean)
    )

    with dbManager.engine.connect() as conn:
        
        trans = conn.begin()
        
        try:
            values_list = []
            # for station_data in stations:
            #     print(station_data)
            #     values_list.append({
            #         'number': station_data['number'],
            #         'address': station_data['address'],
            #         'banking': station_data['banking'],
            #         'capacity': station_data['totalStands']['capacity'],
            #         'bonus': station_data['bonus'],
            #         'contractName': station_data['contractName'],
            #         'name': station_data['name'],
            #         'position_lat': station_data['position']['latitude'],
            #         'position_lng': station_data['position']['longitude'],
            #         'connected': station_data['connected'],
            #         'overflow': station_data['overflow']
            #     })
                

# Don't run this again, the table is already populated with the stations
            # conn.execute(
            #     insert(station),
            #     values_list
            # )

            trans.commit()
            print(f"Inserted {len(stations)} stations into the database")

        except Exception as e:
            
            trans.rollback()
            print("Error occurred while inserting stations:", e)

insert_stations(stations)





