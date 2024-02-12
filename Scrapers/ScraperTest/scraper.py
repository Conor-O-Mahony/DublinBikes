import json
import requests
import dbinfo

params = {"contract": dbinfo.contract, "apiKey": dbinfo.apiKey}

try:
    r = requests.get(dbinfo.STATIONS_URI, params=params)
    r.raise_for_status()  
    print(r.json())
except requests.exceptions.RequestException as e:
    print("Error:", e)
