import logging
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
import json
from collections import defaultdict
from weakref import WeakValueDictionary
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from copy import deepcopy
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen



DIGIT_GROUPS = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', # For 0-9
]
DIGIT_GROUP_NAMES = [
    '00-09', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '0-9'
]


def get_numbers_keys_for_group(group):
    return [group + str(i) for i in range(0, 10)]

def get_number_values_for_group(group):
    if group == '_':
        group = ''
    return [group + str(i) for i in range(0, 10)]

def get_all_keys():
    return [key for g in DIGIT_GROUPS for key in get_numbers_keys_for_group(g)]





class MenuButton(Button):
    pass


class ButtonBoxMenu(BoxLayout):
    pass


class MainScreen(Screen):
    pass



class NumberConfig:
    def __init__(self, data=None):
        self._data = dict()
        for key in get_all_keys():
            self._data[key] = data[key]['person'] if data and key in data else ''

    def get_value_for(self, assoc):
        return self._data[assoc]

    def set_value_for(self, assoc, value):
        self._data[assoc] = value

    def digit_group_filled(self, group):
        return all([self._data[key] for key in get_numbers_keys_for_group(group)])

    @staticmethod
    def get_named_groups():
        return zip(DIGIT_GROUPS, DIGIT_GROUP_NAMES)


def read_config_from_stream(stream):
    return NumberConfig(json.loads(stream.read()))


def write_config_to_stream(stream, config):
    result = {k: {'person': config.get_value_for(k)} for k in get_all_keys()}
    stream.write(json.dumps(result))


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


class ListScreen(Screen):
    
    def set_up(self, config):
        self.config = config
        print("Before calling deepcopy()")
        self.local_config = deepcopy(config) 
        print("After calling deepcopy()")
        self.current_group_id = None
        print("Before weakref()")
        self.group_switch_buttons = WeakValueDictionary()
        self.inputs = WeakValueDictionary()
        print("Before populate_tabs()")
        self.populate_tabs()
        print("Before colorize_buttons()")
        self.colorize_buttons()
        print("Before select_group(0)")
        self.select_group('0')
        print("Before set_input_handlers()")
        self.set_input_handlers()


    def get_group_switch_layout(self):
        return self.ids.switch_layout

    def populate_tabs(self):
        parent = self.get_group_switch_layout()
        for chunk in by_chunk(self.local_config.get_named_groups(), 5):
            anchor = AnchorLayout()
            layout = BoxLayout()
            layout.spacing = '5dp'
            layout.size_hint_x = len(chunk) / 5
            parent.add_widget(anchor)
            anchor.add_widget(layout)
            for group, group_name in chunk:
                button = ToggleButton(id=group, text=group_name)
                button.bind(on_press=self.handle_group_release)
                self.group_switch_buttons[group] = button
                layout.add_widget(button)

    def colorize_buttons(self):
        for group, button in self.group_switch_buttons.items():
            if self.local_config.digit_group_filled(group):
                button.background_color = 0, 1, 0, 1
            else:
                button.background_color = 1, 0, 0, 1

    def handle_group_release(self, btn):
        self.select_group(btn.id)

    def select_group(self, group_id):
        for btn in self.group_switch_buttons.values():
            btn.state = 'normal'

        btn = self.group_switch_buttons[group_id]
        btn.state = 'down'

        label_names = reversed(get_number_values_for_group(group_id))
        label_ids = reversed(get_numbers_keys_for_group(group_id))

        self.unset_input_handlers()
        for text, label_id, number_input in zip(label_names, label_ids, self.number_inputs()):
            number_input.ids.label.text = text
            number_input.ids.input.text = self.local_config.get_value_for(label_id)
            number_input.ids.input.config_id = label_id

        self.set_input_handlers()
        self.current_group_id = group_id

    def set_input_handlers(self):
        for number_input in self.number_inputs():
            number_input.ids.input.bind(text=self.update_text_value)

    def unset_input_handlers(self):
        for number_input in self.number_inputs():
            number_input.ids.input.unbind(text=self.update_text_value)

    def number_inputs(self):
        return self.ids.number_input_layout.children

    def update_text(self, label_id, text):
        self.local_config.set_value_for(label_id, text)

    def save_changes(self):
        for key, value in self.local_config._data.items():
            self.config.set_value_for(key, value)
        with open('memory_config.json', 'w') as file_stream:
            write_config_to_stream(file_stream, self.config)
        self._to_main_screen()

    def cancel(self):
        self.local_config = deepcopy(self.config)
        self._to_main_screen()

    def update(self):
        self.select_group(self.current_group_id)
        self.colorize_buttons()
    
    def _to_main_screen(self):
        self.parent.transition.direction = 'right'
        self.parent.current = 'main'

    def update_text_value(self, instance, value):
        self.local_config.set_value_for(instance.config_id, value)
        self.colorize_buttons()




class MemoryScreenManager(ScreenManager):

    def to_list_screen(self, number_config):
        if 'list' not in self.screen_names:
            print('Before creating ListScreen')
            list_screen = ListScreen(name='list')
            list_screen.set_up(config=number_config)
            self.add_widget(list_screen)
        self.transition.direction = 'left'
        self.current = 'list'
        self.current_screen.update()


class MemoryApp(App):

    def read_config_from_disk(self):
        try:
            #with open('memory_config.json', 'r') as file_stream:
            return NumberConfig()
                # return read_config_from_stream(file_stream)
        except FileNotFoundError:
            logging.info('No config file found.')
            return NumberConfig()
        except:
            logging.exception("Cannot read the file")
            return NumberConfig()

    def build(self):
        self.number_config = self.read_config_from_disk()
        return MemoryScreenManager()


if __name__ == '__main__':
    MemoryApp().run()

"""
No need to select current screen
Commenting out ListScreen doesn't fix the app
Uncommenting config code crushes the app
Uncommenting NumberConfig and functions breaks the app
typings crashes the app
uncommented read config file - crashes
commented # self.number_config = self.read_config_from_disk() app works
seems like self.read_config_from_disk() breaks the app
except on file read doesn't help
seems like open('memory_config.json', 'r') as file_stream breaks the app
def to_list_screen doesn't break the app itself
on_release: app.root.to_list_screen(app.number_config) itself doesn't break the app, but calling it does
creating ListScreen breaks the app on clicking Your List
"""