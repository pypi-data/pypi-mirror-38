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

class Options(object):

    def __init__(self, _handler, _profile_id):
        self.handler = _handler;
        self.profile_id = _profile_id;

    def get(self, _args=None):
        return self.handler.get('profile/' + self.profile_id + '/options');
