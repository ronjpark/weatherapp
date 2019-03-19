#
# Copyright and so on...
#

"""
Configuration of this project
"""

# TODO: Provide a way to get different env.py based on the environment, such like Dev/Prod

IS_DEBUG_MODE=1

GEOCODE_TEMP = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key=AIzaSyBWNaKC_y8-PuMlHDo2sFJKOEZ-aw98ZVU"
WEATHER_TEMP = "https://api.darksky.net/forecast/c793cf3c9953f4de0a6a87901aae3d83/{lat},{lng},{{}}?exclude=currently,minutely,hourly,flags"
