from kivy.uix.label import Label
from src.widget.base_screen import BaseScreen


class OneNumberResultScreen(BaseScreen):

    def __init__(self, **kw):
        super(OneNumberResultScreen, self).__init__(**kw)
        self.answer = None
        self.number = None
        self.state = None
        self.label_error_count = self.ids.label_error_count  # type: Label
        self.label_expected = self.ids.label_expected_answer  # type: Label
        self.label_actual = self.ids.label_actual_answer  # type: Label

    def update_state(self, state):
        self.label_error_count.text = ''
        self.label_expected.text = ''
        self.label_actual.text = ''

        if state.one_number_answer == state.remember_number:
            self.report_success(state.one_number_answer)
        else:
            self.report_errors(state.remember_number, state.one_number_answer)

    def report_errors(self, expected, actual):
        """
        :param str expected:
        :param str actual:
        :return:
        """
        actual = actual.ljust(len(expected), ' ')
        error_count = 0
        error_text = ''

        for i in range(len(expected)):
            expected_char = expected[i]
            actual_char = actual[i]
            if expected_char != actual_char:
                error_text += '[color=ff0000]%s[/color]' % actual_char
                error_count += 1
            else:
                error_text += actual_char

        self.label_error_count.text = "You've made %s mistakes" % error_count
        self.label_actual.text = error_text
        self.label_expected.text = expected

    def report_success(self, expected):
        """
        :param str expected:
        :return:
        """
        self.label_expected.text = '[color=00ff00]%s[/color]' % expected
        self.label_error_count.text = 'You are correct!'
