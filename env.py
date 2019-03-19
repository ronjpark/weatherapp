#
# Copyright and so on...
#

"""
Configuration of this project
"""

from google.appengine.api import modules

# Constants
PAST_DAYS = 7
SECOND_IN_DAY = 24*60*60
DATE_FORMAT = '%b %d, %Y'

# API to other microservices
_geocode_hostname = modules.get_hostname(module='my-geocode')
_temperature_hostname = modules.get_hostname(module='my-temperature')
_weather_summary_hostname = modules.get_hostname(module='my-weather-summary')

GEOCODE_URL = "https://{}/".format(_geocode_hostname)
TEMPERATURE_URL = "http://{}/".format(_temperature_hostname)
WEATHER_SUMMARY_URL = "http://{}/".format(_weather_summary_hostname)