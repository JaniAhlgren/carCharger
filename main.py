from asyncio.log import logger
from asyncio.windows_events import NULL
import sys
from urllib import response
from matplotlib.font_manager import json_dump
import requests
import json
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parse_dt
from logger import chargerLogger as cl
from jsonHandler import *
def main():
    # Call getJson.getTomorrowsElectricityPrice
    #carunaNightTime=["22","23","0","1","2","3","4","5","6"]
    #NGE_Margin=0.16
    value = getJson()._fetch_nordpool_json(35)
    x=json.loads(value)
    hourlyPrices= getJson.getTomorrowsElectricityPrice(x)
    print(hourlyPrices)



if __name__ == "__main__":
    main()