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

from .option import Option
from .options import Options
from .question import Question
from .questions import Questions
from .scheduling import Scheduling

class Profile(object):

    def __init__(self, _handler, _profile_id):
        self.handler = _handler;
        self.profile_id = _profile_id;

        self.options    = Options(self.handler, self.profile_id);
        self.questions  = Questions(self.handler, self.profile_id);
        self.scheduling = Scheduling(self.handler, self.profile_id);

    def get(self):
        return self.handler.get('profile/' + self.profile_id);

    #
    # options
    #
    def option(self, _option_id):
        return Option(self.handler, self.profile_id, _option_id);

    #
    # pre-call questions
    #
    def question(self, _question_id):
        return Question(self.handler, self.profile_id, _question_id);
