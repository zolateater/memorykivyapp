from src.config.app_state import AppState
from src.widget.base_screen import BaseScreen


class OneNumberSettingsScreen(BaseScreen):

    def __init__(self, **kw):
        super(OneNumberSettingsScreen, self).__init__(**kw)
        self.state = None  # type: AppState

    def update_state(self, state):
        """

        :param state:
        :return:
        """
        self.state = state
        self.ids.slider_time.value = self.state.training_settings.time_one_number
        self.ids.slider_number_length.value = self.state.training_settings.number_length

    def on_length_change(self, value):
        int_val = int(value)
        self.state.training_settings.number_length = int_val
        self.ids.label_number_length.text = 'Number length: ' + str(int_val)

    def on_seconds_change(self, value):
        int_val = int(value)
        self.state.training_settings.time_one_number = int_val
        self.ids.label_time.text = 'Seconds to remember the number: ' + str(int_val)
