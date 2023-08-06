#
# This file is part of the Fonolo Python Wrapper package.
#
# (c) Foncloud, Inc.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

import re

from .requesthandler import RequestHandler
from ..exception.exception import FonoloException

class CallBack(object):

    def __init__(self, _handler, _call_id=''):
        self.handler = _handler;
        self.call_id = _call_id;

    def start(self, _args):
        return self.handler.post('callback', _args);

    def cancel(self):
        return self.handler.post('callback/' + self.call_id + '/cancel', {});

    def status(self):
        return self.handler.get('callback/' + self.call_id + '/status');
