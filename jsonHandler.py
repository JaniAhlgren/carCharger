from asyncio.log import logger
from asyncio.windows_events import NULL
import sys
from urllib import response
import requests
import json
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parse_dt
from logger import chargerLogger as cl
#Using nordpool api
class getJson():
    API_URL = 'https://www.nordpoolgroup.com/api/marketdata/page/%i'
    
    def _fetch_nordpool_json(self, data_type, end_date=None):
        ''' Fetch JSON from API '''
        # If end_date isn't set, default to tomorrow
        if end_date is None:
            end_date = date.today() + timedelta(days=1)
        # If end_date isn't a date or datetime object, try to parse a string
        if not isinstance(end_date, date) and not isinstance(end_date, datetime):
            end_date = parse_dt(end_date)

        # Create request to API
        r = requests.get(self.API_URL % data_type, params={
            'currency': 'EUR',
            'endDate': end_date.strftime('%d-%m-%Y'),
        })
        # Return JSON response
        return(r.content)
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

