from asyncio.log import logger
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
    
    def _fetch_json(self, data_type, end_date=None):
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
    def _parse_json(self, data, areas=[]):
        '''
            Parse json response from fetcher.
            Returns dictionary with
                - start time
                - end time
                - update time
                - currency
                - dictionary of areas, based on selection
                    - list of values (dictionary with start and endtime and value)
                    - possible other values, such as min, max, average for hourly
            '''

        # If areas isn't a list, make it one
        if not isinstance(areas, list):
            areas = list(areas)

        # Update currency from data
        currency = str(data[0])
        print(currency)
        # Ensure that the provided currency match the requested one
        if currency != self.currency:
            raise Exception

        # All relevant data is in data['data']
        data = data['data']
        start_time = self._parse_dt(data['DataStartdate'])
        end_time = self._parse_dt(data['DataEnddate'])
        updated = self._parse_dt(data['DateUpdated'])

        area_data = {}
        # Loop through response rows
        for r in data['Rows']:
            row_start_time = self._parse_dt(r['StartTime'])
            row_end_time = self._parse_dt(r['EndTime'])

            # Loop through columns
            for c in r['Columns']:
                name = c['Name']
                # If areas is defined and name isn't in areas, skip column
                if areas and name not in areas:
                    continue

                # If name isn't in area_data, initialize dictionary
                if name not in area_data:
                    area_data[name] = {
                        'values': [],
                    }

                # Time based and average, max, min etc rows are separated
                # with 'IsExtraRow' -marking
                if r['IsExtraRow']:
                    # Update extra data to dictionary
                    area_data[name][r['Name']] = self._conv_to_float(c['Value'])
                else:
                    # Append dictionary to value list
                    area_data[name]['values'].append({
                        'start': row_start_time,
                        'end': row_end_time,
                        'value': self._conv_to_float(c['Value']),
                    })

        return {
            'start': start_time,
            'end': end_time,
            'updated': updated,
            'currency': currency,
            'areas': area_data
        }  
        


