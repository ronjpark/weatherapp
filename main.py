#
# Copyright and so on
#

"""
Description of this file
"""

import json
import time
import webapp2

from datetime import datetime
from google.appengine.api import modules
from google.appengine.api import urlfetch

from weatherapp.common import BaseRequestHandler
from env import (GEOCODE_URL, WEATHER_SUMMARY_URL, TEMPERATURE_URL,
                 PAST_DAYS, SECOND_IN_DAY, DATE_FORMAT)


def getUrl(baseurl, **kwargs):
    if kwargs:
        arg_list = ["{}={}".format(key, val) for key, val in kwargs.items()]
        return baseurl + '?' + '&'.join(arg_list)
    return baseurl
    
    
class GetWeatherHandler(BaseRequestHandler):

    def get(self):
        # Convert address into lat/long
        address = self.request.get('address')
        if not address:
            self.response.write("No input address")
            self.response.set_status(400)
            return

        url = getUrl(GEOCODE_URL, address=address)
        geo_res = self.fetch_n_extract(url)
        if not geo_res:
            return
        location = geo_res.get('location')
        if not location:
            self.response.write("Invalid address: {}".format(re.content))
            self.response.set_status(400)
            return
            
        # Get timestamps of the present and a week ago
        current_time = int(time.time())
        week_ago_time = max(0, current_time - PAST_DAYS*SECOND_IN_DAY)

        # Get Weather summary of a week
        url = getUrl(WEATHER_SUMMARY_URL, start=week_ago_time, end=current_time, **location)
        weather_summary_res = self.fetch_n_extract(url)
        if not weather_summary_res:
            return
        
        # Get Temperatures
        url = getUrl(TEMPERATURE_URL, start=week_ago_time, end=current_time, **location)
        temperature_res = self.fetch(url)
        if not temperature_res:
            return
            
        # Build up Output
        output = {
            'address': geo_res.get('formatted_address') or address,
            'weather': []
        }
        weather_list = output['weather']
        for summary, temperature in zip(weather_summary_res, temperature_res):
            if not summary or not temperature or summary.get('timestamp') != temperature.get('timestamp'):
                self.response.write("Fail to get weather")
                self.response.set_status(500)
                break
            ts = int(summary.get('timestamp'))
            weather_res = {'date': datetime.fromtimestamp(ts).strftime(DATE_FORMAT),
                           'summary': summary.get('summary'),
                           'temperatureHigh': temperature.get('temperatureHigh'),
                           'temperatureLow': temperature.get('temperatureLow')}
            weather_list.append(weather_res)
        else:
            # Return the result only if there is no error
            self.return_response(output)
            
            
    def return_response(self, output):
        """
        This function could be defined as another microservice
        """
        
        format = self.request.get('format', 'web')
        if format == 'web':
            self.response.write("<h1>Last 7 days weather of {}</h1>".format(output.get('address')))
            for weather in output.get('weather', []):
                self.response.write("<h3>{date}</h3>\nSummary: {summary}<br>High: {temperatureHigh} &#8457;<br>Low: {temperatureLow} &#8457;<br>\n".format(**weather))
        elif format == 'json':
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(output))
        else:
            # Validation check should be done at the begining of the request processing
            self.response.write("Invalid format: {}".format(format))
            self.response.set_status(400)


app = webapp2.WSGIApplication([
    ('/', GetWeatherHandler),
], debug=True)
