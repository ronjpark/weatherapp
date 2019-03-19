#
# Copyright and so on
#

"""
Description of this file
"""

import webapp2

from weatherapp import common


class GetTemperatureHandler(common.WeatherRequestHandler):
    extract_fields = ['temperatureHigh', 'temperatureLow']


app = webapp2.WSGIApplication([
    ('/', GetTemperatureHandler),
], debug=True)
