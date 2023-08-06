#
# This file is part of the Fonolo Python Wrapper package.
#
# (c) Foncloud, Inc.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

import requests

from ..exception.exception import FonoloException

class RequestHandler(object):

    def __init__(self, _account_sid, _api_token, _options):

        self.account_sid = _account_sid
        self.api_token = _api_token
        self.options = _options

    def get(self, _path):

        #
        # build the API URL using the path provided
        #
        url = self.options['url'] + _path

        #
        # make the post request
        #
        res = requests.get(url, auth=(self.account_sid, self.api_token), verify=True)

        #
        # catch any JSON parsing exceptions
        #
        try:
            self.json = res.json()
        except ValueError:
            raise FonoloException('ERROR: failed to parse JSON response')

        return self.json

    def post(self, _path, _params):

        #
        # build the API URL using the path provided
        #
        url = self.options['url'] + _path

        #
        # make the post request
        #
        res = requests.post(url, data = _params, auth=(self.account_sid, self.api_token), verify=True)

        #
        # catch any JSON parsing exceptions
        #
        try:
            self.json = res.json()
        except ValueError:
            raise FonoloException('ERROR: failed to parse JSON response')

        return self.json
