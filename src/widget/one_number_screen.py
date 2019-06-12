import random
import string
from kivy.clock import Clock
from src.widget.base_screen import BaseScreen


class OneNumberScreen(BaseScreen):

    def __init__(self, **kw):
        super(OneNumberScreen, self).__init__(**kw)
        self.number = None
        self.seconds_left = None
        self.current_event = None

    def set_seconds_label_text(self, seconds):
        self.ids.label_timer.text = 'Seconds left: ' + str(seconds)

    def update_state(self, state):
        self.cancel_countdown()
        self.number = generate_number(state.training_settings.number_length)
        self.seconds_left = state.training_settings.time_one_number

        self.ids.label_number.text = self.number
        self.set_seconds_label_text(self.seconds_left)

        state.remember_number = self.number
        self.current_event = self.schedule_countdown()

    def cancel_countdown(self):
        if self.current_event:
            self.current_event.cancel()
        self.current_event = None

    def schedule_countdown(self):
        return Clock.schedule_once(self.countdown, 1)

    def time_exceeded(self):
        return self.seconds_left < 1

    def countdown(self, dt):
        if self.time_exceeded():
            self.forward()
            return
        self.seconds_left -= 1
        self.set_seconds_label_text(self.seconds_left)
        self.current_event = self.schedule_countdown()

    def forward(self):
        self.cancel_countdown()
        self.parent.to_screen('one_number_check')


def generate_number(number_length):
    """
    :param int number_length:
    :return:
    """
    return "".join([random.choice(string.digits) for _ in range(number_length)])
