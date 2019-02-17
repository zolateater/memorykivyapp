import random
from string import digits

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from src.config.number_config import to_num_str, DIGIT_GROUPS
from src.widget.base_screen import BaseScreen
from src.widget.training_sequence_settings_screen import TrainingSettings


class SequenceCheckScreen(BaseScreen):

    def __init__(self, **kw):
        """

        :param list sequence:
        :param kw:
        """
        super(SequenceCheckScreen, self).__init__(**kw)
        self.sequence = None
        self.answers = None

    def update_state(self, state):
        self.sequence = state.remember_sequence
        self.answers = []
        self.ask_next()

    def get_buttons(self):
        return [
            self.ids.answer_button_1,
            self.ids.answer_button_2,
            self.ids.answer_button_3,
            self.ids.answer_button_4
        ]

    def select_answer(self, answer):
        if not self.all_answers_given():
            self.answers.append(answer)

        if not self.all_answers_given():
            self.ask_next()

        if self.all_answers_given():
            self.parent.state.answers = self.answers
            self.parent.to_screen('sequence_result')

    def ask_next(self):
        for button, option in zip(self.get_buttons(), self.get_answer_options()):
            button.text = to_num_str(option)
            button.answer = option

        self.ids.label_question_count.text = "{} out of {}".format(len(self.answers) + 1, len(self.sequence))

    def all_answers_given(self):
        return len(self.sequence) == len(self.answers)

    def get_answer_options(self):
        cur_answer = self.current_correct_answer()

        potential_answers = {
            get_wrong_answer_same_group(cur_answer),
            get_wrong_answer_same_number(cur_answer)
        }

        if not self.is_last_question():
            next_answer = self.sequence[len(self.answers) + 1]
            if cur_answer != next_answer:
                potential_answers.add(next_answer)

        if self.answers:
            previous_answer = self.sequence[len(self.answers) - 1]
            if previous_answer != cur_answer:
                potential_answers.add(previous_answer)

        while len(potential_answers) < 3:
            potential_answers.add(get_wrong_answer_same_group(cur_answer))

        answer_options = list(potential_answers)[:3]
        answer_options.append(self.current_correct_answer())
        random.shuffle(answer_options)

        return answer_options

    def is_last_question(self):
        return len(self.sequence) - len(self.answers) == 1

    def current_correct_answer(self):
        return self.sequence[len(self.answers)]


def get_group(number):
    return number[0]


def get_digit(number):
    return number[1]


def get_wrong_answer_same_number(number):
    current_group = get_group(number)
    current_digit = get_digit(number)
    wrong_groups = list(set(DIGIT_GROUPS) - set(current_group))

    return random.choice(wrong_groups) + current_digit


def get_wrong_answer_same_group(number):
    current_group = get_group(number)
    current_digit = get_digit(number)
    wrong_digits = list(set(digits) - set(current_digit))

    return current_group + random.choice(wrong_digits)
