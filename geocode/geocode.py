#
# Copyright and so on
#

"""
Description of this file
"""

import json
import webapp2

from weatherapp import common
from weatherapp.common.env import GEOCODE_TEMP


class GetGeocodeHandler(common.BaseRequestHandler):

    def get(self):
        # Convert address into lat/long
        address = self.request.get('address')
        if not address:
            self.response.write("No input address")
            self.response.set_status(400)
            return
            
        url = GEOCODE_TEMP.format(address=address)
        geo_res = self.fetch_n_extract(url, common.extractor.GEOCODE)
        if geo_res is None:
            return
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(geo_res))

            
app = webapp2.WSGIApplication([
    ('/', GetGeocodeHandler),
], debug=True)
