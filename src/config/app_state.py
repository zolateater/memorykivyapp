from src.config.number_config import NumberConfig
from src.widget.training_sequence_settings_screen import TrainingSettings


class AppState:

    __slots__ = ('number_config', 'training_settings', 'remember_sequence', 'answers')

    def __init__(self, number_config, training_settings, remember_sequence, answers):
        """
        :param NumberConfig number_config:
        :param TrainingSettings training_settings:
        :param list remember_sequence:
        :param list answers:
        """
        self.number_config = number_config
        self.training_settings = training_settings
        self.remember_sequence = remember_sequence
        self.answers = answers
