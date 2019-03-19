#
# Copyright and so on
#

"""
Description of this file
"""

import webapp2

from weatherapp import common


class GetWeatherSummaryHandler(common.WeatherRequestHandler):
    extract_fields = ['summary']


app = webapp2.WSGIApplication([
    ('/', GetWeatherSummaryHandler),
], debug=True)
