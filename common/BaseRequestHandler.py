#
# Copyright and so on
#

"""
Description of this file
"""

import logging
import traceback
import webapp2

from google.appengine.api import urlfetch

import env
import extractor


class BaseRequestHandler(webapp2.RequestHandler):

    if env.IS_DEBUG_MODE:
        def handle_exception(self, exception, debug):
            # Log the error.
            logging.exception(exception)

            # Set a custom message with traceback for the debug
            self.response.write('An error occurred: {}'.format(exception))
            self.response.write(traceback.format_exc())

            # If the exception is a HTTPException, use its error code.
            # Otherwise use a generic 500 error code.
            if isinstance(exception, webapp2.HTTPException):
                self.response.set_status(exception.code)
            else:
                self.response.set_status(500)
            

    def fetch_n_extract(self, fetch_url, extractor_type=None, *extract_fields):
        def verify_res(res, url):
            if res.status_code != 200:
                self.response.write("{} returns {}".format(url, res.status_code))
                self.response.write("Body: {}".format(res.content))
                self.response.set_status(500)
                return False
            if not res.headers['Content-Type'].startswith('application/json'):
                self.response.write("{} returns invalid Content-Type: {}".format(url, res.headers['Content-Type']))
                self.response.set_status(500)
                return False
            return True
            
        res = urlfetch.fetch(fetch_url)
        if not verify_res(res, fetch_url):
            return None
        if extractor_type is not None:
            output = extractor.extract(extractor_type, res.content, extract_fields)
            if output is None:
                self.response.write("Invalid extractor type: {}".format(extractor_type))
                self.response.set_status(500)            
            return output
        return res.content
