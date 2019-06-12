import random
import string
from src.widget.base_screen import BaseScreen


class OneNumberCheckScreen(BaseScreen):

    def __init__(self, **kw):
        super(OneNumberCheckScreen, self).__init__(**kw)
        self.number = None
        self.state = None

    def update_state(self, state):
        self.ids.input_answer.text = ''
        self.number = state.remember_number
        self.state = state

    def update_answer(self, value):
        self.state.one_number_answer = value

    def forward(self):
        self.state.one_number_answer = self.answer.strip()


def generate_number(number_length):
    """
    :param int number_length:
    :return:
    """
    return "".join([random.choice(string.digits) for _ in range(number_length)])
