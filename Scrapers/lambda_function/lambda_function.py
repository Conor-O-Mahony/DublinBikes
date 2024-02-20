import pymysql                   
import os
import sys
import logging
import json
import requests
import datetime

#Obtain from RDS - Make the appropraite environment variables as in https://dev.to/biplov/handling-passwords-and-secret-keys-using-environment-variables-2ei0
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']
apikey = os.environ['BIKES_APIKEY']

url = f'https://api.jcdecaux.com/vls/v3/stations?contract=dublin&apiKey={apikey}' #https://v4ek8y4j0k.execute-api.eu-west-1.amazonaws.com/httpsrequest_lambda_api

#Log details
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Connect to RDS
try:
    conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit(1)

logger.info("SUCCESS: Connection to RDS for MySQL instance succeeded")

def lambda_handler(event, context): #https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-lambda-tutorial.html
    """
    This function GETs bike data from JCDeaux API and commits it to the RDS database
    """
    json_file = requests.get(url)
    stations = json.loads(json_file.text)
    
    item_count = 0
    sql_string = """INSERT INTO Bikes.availability(
                    timestamp, number, last_update, connected, available_bikes, available_bike_stands, mechanical_bikes,
                    electrical_bikes, electric_internal_bikes, electric_removeable_battery, status, overflow_stands) 
                    VALUES """
                    
    current_datetime = datetime.datetime.now()

    for station in stations:
        number = station['number']
        last_update = datetime.datetime.strptime(station['lastUpdate'], "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        connected = station['connected']
        available_bikes = station['totalStands']['availabilities']['bikes']
        available_bike_stands = station['totalStands']['availabilities']['stands']
        mechanical_bikes = station['totalStands']['availabilities']['mechanicalBikes']
        electrical_bikes = station['totalStands']['availabilities']['electricalBikes']
        electric_internal_battery = station['totalStands']['availabilities']['electricalInternalBatteryBikes']
        electric_removeable_battery = station['totalStands']['availabilities']['electricalRemovableBatteryBikes']
        status = station['status']
        overflow_stands = station['overflowStands']
        
        sql_string += f"""('{current_datetime}', {number}, '{last_update}', {connected}, {available_bikes}, {available_bike_stands},
                        {mechanical_bikes},{electrical_bikes},{electric_internal_battery},{electric_removeable_battery},
                        '{status}','{overflow_stands}'), """
        item_count += 1
            
    sql_string = sql_string[:-2]+';'
            
    with conn.cursor() as cur:
        try:
            cur.execute(sql_string)
            conn.commit()
            logger.info(f"Successfully commited {item_count} entries")
        except:
            logger.info("Error, could not commit entries.")
            
    conn.close()

    return {"statusCode": 200} 
