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

class Question(object):

    def __init__(self, _handler, _profile_id, _question_id):
        self.handler = _handler;
        self.profile_id = _profile_id;
        self.question_id = _question_id;

    def get(self):
        return self.handler.get('profile/' + self.profile_id + '/question/' + self.question_id);
