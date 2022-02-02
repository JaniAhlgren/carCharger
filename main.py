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

    carunaNightTime=["22","23","0","1","2","3","4","5","6"]
    NGE_Margin=0.16
    value = getJson()._fetch_json(35)
    x=json.loads(value)
    hourlyPrices=getTomorrowsElectricityPrice(x)
   

def getTomorrowsElectricityPrice(json, carunaNightTime=["22","23","0","1","2","3","4","5","6"], NGE_Margin=0.16):
    listedPrices=[]
    carunaNightPrice=2.74
    carunaDayPrice=4.45
    for y in range(24):
        startTime=json["data"]["Rows"][y]["StartTime"]
        # this should be used to verify that the time is rightprint(x["data"]["Rows"][0]["Columns"][0]["Name"])
        price=json["data"]["Rows"][y]["Columns"][0]["Value"]

        #convert price to float
        price=price.replace(',', '.').replace(" ", "")
        startHour=datetime.fromisoformat(startTime).hour
        hourlyPrice=NULL
        if str(startHour) in carunaNightTime:
            totalPrice=float(price)/10+float(NGE_Margin)+float(carunaNightPrice)
                       
        else:
            totalPrice=float(price)/10+float(NGE_Margin)+float(carunaDayPrice)
        hourlyPrice=f"{startTime} : {totalPrice}"
        listedPrices.append(hourlyPrice)
    cl.logWriter(listedPrices)
    return listedPrices   



if __name__ == "__main__":
    main()