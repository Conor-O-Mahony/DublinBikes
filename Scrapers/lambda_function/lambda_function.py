import pymysql                   
import os
import sys
import logging
import json
import requests

#Obtain from RDS - Make the appropraite environment variables as in https://dev.to/biplov/handling-passwords-and-secret-keys-using-environment-variables-2ei0
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']
apikey = os.environ['BIKES_APIKEY']

url = f'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey={apikey}'

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
    This function creates a new RDS database table and writes records to it
    """
    json_file = requests.get(url)
    stations = json.loads(json_file.text)
    
    item_count = 0

    for station in stations:
        number = station['number']
	last_update = station['last_update']
        available_bikes = station['available_bikes']
        available_bike_stands = station['available_bike_stands']
        status = station['status']
        
        sql_string = f"""INSERT INTO availability(
                        number, last_update, available_bikes, available_bikes_stands, status
                        ) values ({number}, {last_update}, {available_bikes}, {available_bike_stands}, '{status}')"""
    
        with conn.cursor() as cur:
            cur.execute(sql_string)
            try:
                conn.commit()
                item_count += 1
            except:
                logger.info("Error: couldn't commit row.")
            
    try:
        conn.commit()
    except:
        logger.info("Couldn't execute final commit.")

    return "Added %d rows to RDS for MySQL table" %(item_count)
