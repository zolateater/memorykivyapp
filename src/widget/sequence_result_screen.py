from src.widget.base_screen import BaseScreen


class SequenceResultScreen(BaseScreen):

    def __init__(self, **kw):
        super(SequenceResultScreen, self).__init__(**kw)
        self.sequence = None
        self.answers = None

    def update_state(self, state):
        self.sequence = state.remember_sequence
        self.answers = state.answers
        self.calc_result()

    def calc_result(self):
        correct_total = 0
        for answer, correct in zip(self.answers, self.sequence):
            if answer == correct:
                correct_total += 1

        self.ids.label_score.text = "{} out of {}".format(correct_total, len(self.sequence))
