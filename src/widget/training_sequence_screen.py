import random

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from src.widget.training_sequence_settings_screen import TrainingSettings
from src.config.number_config import NumberConfig


class _TrainingAnswer:
    __slots__ = ('answer', 'seconds_taken')


class TrainingSequenceScreen(Screen):

    def __init__(self, settings, number_config, **kw):
        """

        :param TrainingSettings settings:
        :param NumberConfig number_config:
        :param kw:
        """
        super(TrainingSequenceScreen, self).__init__(**kw)
        self.settings = settings
        self.number_config = number_config
        print('Groups: ', self.settings.selected_groups)

    def update(self):
        self.sequence = generate_sequence(self.settings.selected_groups, self.settings.numbers_count)
        self.seconds_left = self.settings.time_per_number
        self.current_sequence_index = -1
        self.current_event = None
        self.to_next_number()

    def time_exceeded(self):
        """
        :rtype: bool
        """
        return self.seconds_left <= 1

    def count_down(self, dt):
        if not self.time_exceeded():
            self.seconds_left -= 1
            self.ids.label_time_left.text = str(self.seconds_left)
            self.current_event = self.schedule_changes()
            return

        self.to_next_number()

    def remind_btn(self):
        return self.ids.button_assoc

    def remind_label(self):
        return self.ids.label_assoc

    def cancel_countdown(self):
        if self.current_event:
            self.current_event.cancel()
        self.current_event = None

    def to_next_number(self):
        self.cancel_countdown()

        if self.is_last_number():
            self.finish_training()
            return

        self.current_sequence_index += 1
        self.seconds_left = self.settings.time_per_number
        self.ids.label_time_left.text = str(self.seconds_left)
        self.ids.label_current_number.text = to_num_str(self.sequence[self.current_sequence_index])
        self.current_event = self.schedule_changes()

        remind_btn = self.remind_btn()
        self.remind_label().text = ''
        remind_value = self.number_config.get_value_for(self.sequence[self.current_sequence_index])
        if remind_value:
            remind_btn.disabled = False
            remind_btn.text = 'Show association'
        else:
            remind_btn.disabled = True
            remind_btn.text = 'No association'

    def remind(self):
        self.remind_label().text = self.number_config.get_value_for(self.sequence[self.current_sequence_index])

    def schedule_changes(self):
        return Clock.schedule_once(self.count_down, 1)

    def is_last_number(self):
        """
        :rtype: bool
        """
        return self.current_sequence_index == len(self.sequence) - 1

    def on_cancel(self):
        self.cancel_countdown()
        self.parent.back()

    def finish_training(self):
        pass

def generate_sequence(groups, numbers_count):
    """
    :param groups:
    :param numbers_count:
    :rtype: list
    """
    return [random.choice(list(groups)) + str(random.choice(range(10))) for _ in range(numbers_count)]


def to_num_str(grouped_num):
    """
    :rtype: str
    :param str grouped_num:
    :return: Returns number to display
    """
    if grouped_num[0] == "_":
        return grouped_num[1:]
    return grouped_num
