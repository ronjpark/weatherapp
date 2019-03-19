#
# Copyright and so on
#

"""
Description of this file
"""

import json

import extractor
from BaseRequestHandler import BaseRequestHandler
from env import WEATHER_TEMP

SECOND_IN_DAY = 24*60*60

class WeatherRequestHandler(BaseRequestHandler):
    extract_fields = []    

    def get(self):
        # Get lat/long
        lat = self.request.get('lat')
        lng = self.request.get('lng')
        if not lat or not lng:
            self.response.write("No input lat/long")
            self.response.set_status(400)
            return
            
        # Get temperatures of a week
        start_time = int(self.request.get('start'))
        end_time = int(self.request.get('end'))
        weather_url = WEATHER_TEMP.format(lat=lat, lng=lng)
        output = []
        for ts in range(start_time, end_time, SECOND_IN_DAY):
            weather_res = self.fetch_n_extract(weather_url.format(ts),
                                               extractor.WEATHER,
                                               *self.extract_fields)
            if weather_res is None:
                break
            weather_res['timestamp'] = ts
            output.append(weather_res)
        else:
            # Return the result only if there is no error
            self.response.headers['Content-Type'] = 'application/json'
            self.response.write(json.dumps(output))


