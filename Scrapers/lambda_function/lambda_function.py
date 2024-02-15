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
    
    logger.info("SUCCESS: obtained JSON file")
    
    item_count = 0

    for station in stations:
        last_update = station['last_update']
        number = station['number']
        banking = str(station['banking'])
        bonus = str(station['bonus'])
        bike_stands = station['bike_stands']
        available_bike_stands = station['available_bike_stands']
        available_bikes = station['available_bikes']
        status = station['status']
    
        sql_string = f"insert into DynamicData (Time, Number, Card, Bonus, Stands, Available_Stands, Available_Bikes, Status) values({last_update}, {number}, '{banking}', '{bonus}', {bike_stands}, {available_bike_stands}, {available_bikes}, '{status}')"
    
        with conn.cursor() as cur:
            cur.execute("create table if not exists DynamicData (Time bigint NOT NULL, Number int NOT NULL, Card varchar(5) NOT NULL, Bonus varchar(5) NOT NULL, Stands int NOT NULL, Available_Stands int NOT NULL, Available_Bikes int NOT NULL, Status varchar(10) NOT NULL, PRIMARY KEY (Time, Number) )")
            cur.execute(sql_string)
            conn.commit()
            cur.execute("select * from DynamicData")
            logger.info("The following items have been added to the database:")
            for row in cur:
                item_count += 1
                logger.info(row)

                
    conn.commit()

    return "Added %d items to RDS for MySQL table" %(item_count)
