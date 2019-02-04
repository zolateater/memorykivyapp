from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from src.widget.number_group_selector import NumberGroupSelector, NumberGroupCheckbox


class TrainingSettings:
    """
    # TODO: rename and include to the general big config
    Configuration class for storing training data.
    """
    TRAINING_SEQUENCE = 1
    TRAINING_NUMBER = 2

    def __init__(self, training_type=None, selected_groups=None, time_per_number=None, time_one_number=None,
                 numbers_count=None, number_length=None):
        """
        :param int training_type:
        :param int training_type:
        :param set selected_groups:
        :param int time_per_number:
        :param int time_one_number:
        :param int number_length:
        :param int numbers_count:
        """
        self.training_type = training_type
        self.selected_groups = set() if selected_groups is None else selected_groups
        self.time_per_number = time_per_number
        self.time_one_number = time_one_number
        self.numbers_count = numbers_count
        self.number_length = number_length

    def add_group(self, group):
        self.selected_groups.add(group)

    def remove_group(self, group):
        self.selected_groups.remove(group)


class TrainingScreen(Screen):
    pass


class TrainingSelectionScreen(Screen):
    pass


class TrainingOneNumberSettingsScreen(Screen):
    pass


class TrainingSequenceSettingsScreen(Screen):
    VALIDATION_TEXT_NO_GROUPS = 'Please, select at least one group'

    def set_up(self, settings):
        """
        :param TrainingSettings settings:
        :return:
        """
        self.settings = settings

    def on_numbers_count_change(self, new_value):
        self.ids.label_numbers_count.text = "Numbers: " + str(new_value)
        self.settings.numbers_count = new_value

    def on_time_per_number_change(self, new_value):
        self.ids.label_time_per_number.text = "Seconds to remember one number: " + str(new_value)
        self.settings.time_per_number = new_value

    def show_error_tooltip(self):
        label = self.ids.label_error
        label.text = self.VALIDATION_TEXT_NO_GROUPS
        anim_start = Animation(opacity=1, duration=0.3)
        anim_end = Animation(opacity=0, duration=0.3)
        Clock.schedule_once(lambda _: anim_end.start(label), 3)
        anim_start.start(label)

    def validate_and_start(self):
        if not self.settings.selected_groups:
            self.show_error_tooltip()
            return

        self.parent.to_screen('training_sequence')

# Sequence of numbers: X seconds for remembering each number of selected groups
# Then you have to choose each number

# Two modes: one number for X seconds number should consist of selected groups
# In the end you need to type the whole number
