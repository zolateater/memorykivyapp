from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from src.config.number_config import write_config_to_stream, get_readable_key
from copy import deepcopy


def by_chunk(iterable, n):
    buffer = []
    for i in iterable:
        buffer.append(i)
        if len(buffer) >= n:
            yield buffer
            buffer = []

    yield buffer


class NumberInputGroup(BoxLayout):
    pass


# TODO: refactor this shit
class ListScreen(Screen):

    def set_up(self, config):
        self.config = config
        self.local_config = deepcopy(self.config)
        self.current_group_id = "0"
        self.colorize_buttons()
        self.populate_inputs_and_labels()

    def on_group_select(self, toggle_button):
        self.current_group_id = toggle_button.group_id
        self.populate_inputs_and_labels()

    def colorize_buttons(self):
        for button in self.get_group_buttons():
            if self.local_config.digit_group_filled(button.group_id):
                button.background_color = 0, 1, 0, 1
            else:
                button.background_color = 1, 0, 0, 1

    def get_group_buttons(self):
        return [
            self.ids.group_button_0,
            self.ids.group_button_1,
            self.ids.group_button_2,
            self.ids.group_button_3,
            self.ids.group_button_4,
            self.ids.group_button_5,
            self.ids.group_button_6,
            self.ids.group_button_7,
            self.ids.group_button_8,
            self.ids.group_button_9,
            self.ids.group_button__
        ]

    def number_inputs(self):
        return self.ids.number_input_layout.children

    def populate_inputs_and_labels(self):
        for input_group in self.ids.number_input_layout.children:
            input_group.ids.label.text = get_readable_key(self.current_group_id, input_group.index)
            input_group.ids.input.text = self.local_config.get_value_for(self.current_group_id + str(input_group.index))

    def update_config(self, index, text):
        self.local_config.set_value_for(self.current_group_id + str(index), text)
        self.colorize_buttons()

    def save_changes(self):
        # TODO: better NumberConfig interface
        for key, value in self.local_config._data.items():
            self.config.set_value_for(key, value)
        with open('memory_config.json', 'w') as file_stream:
            write_config_to_stream(file_stream, self.config)
        self.parent.to_main_screen()

    def cancel(self):
        self.local_config = deepcopy(self.config)  # Drop changes in config
        self.parent.to_main_screen()

    def update(self):
        self.colorize_buttons()
        self.populate_inputs_and_labels()
