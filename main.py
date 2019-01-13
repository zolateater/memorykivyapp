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



# DIGIT_GROUPS = [
#     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', # For 0-9
# ]
# DIGIT_GROUP_NAMES = [
#     '00-09', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '0-9'
# ]


# def get_numbers_keys_for_group(group: str):
#     return [group + str(i) for i in range(0, 10)]

# def get_number_values_for_group(group: str):
#     if group == '_':
#         group = ''
#     return [group + str(i) for i in range(0, 10)]

# def get_all_keys():
#     return [key for g in DIGIT_GROUPS for key in get_numbers_keys_for_group(g)]





class MenuButton(Button):
    pass


# class ButtonBoxMenu(BoxLayout):
#     pass


class MainScreen(Screen):
    pass



# class NumberConfig:
#     def __init__(self, data: Optional[dict] = None) -> None:
#         self._data = dict()
#         for key in get_all_keys():
#             self._data[key] = data[key]['person'] if data and key in data else ''

#     def get_value_for(self, assoc: str) -> str:
#         return self._data[assoc]

#     def set_value_for(self, assoc: str, value: str) -> None:
#         self._data[assoc] = value

#     def digit_group_filled(self, group: str) -> bool:
#         return all([self._data[key] for key in get_numbers_keys_for_group(group)])

#     @staticmethod
#     def get_named_groups():
#         return zip(DIGIT_GROUPS, DIGIT_GROUP_NAMES)


# def read_config_from_stream(stream) -> NumberConfig:
#     return NumberConfig(json.loads(stream.read()))


# def write_config_to_stream(stream, config: NumberConfig) -> None:
#     result = {k: {'person': config.get_value_for(k)} for k in get_all_keys()}
#     stream.write(json.dumps(result))


# def by_chunk(iterable, n):
#     buffer = []
#     for i in iterable:
#         buffer.append(i)
#         if len(buffer) >= n:
#             yield buffer
#             buffer = []

#     yield buffer


# class NumberInputGroup(BoxLayout):
#     pass


# class ListScreen(Screen):
#     def __init__(self, config: NumberConfig, **kwargs):
#         super().__init__(**kwargs)
#         self.config = config
#         self.local_config = deepcopy(config) 
#         self.current_group_id = None
#         self.group_switch_buttons = WeakValueDictionary()
#         self.inputs = WeakValueDictionary()
#         self.populate_tabs()
#         self.colorize_buttons()
#         self.select_group('0')
#         self.set_input_handlers()

#     def get_group_switch_layout(self) -> BoxLayout:
#         return self.ids.switch_layout

#     def populate_tabs(self):
#         parent = self.get_group_switch_layout()
#         for chunk in by_chunk(self.local_config.get_named_groups(), 5):
#             anchor = AnchorLayout()
#             layout = BoxLayout()
#             layout.spacing = '5dp'
#             layout.size_hint_x = len(chunk) / 5
#             parent.add_widget(anchor)
#             anchor.add_widget(layout)
#             for group, group_name in chunk:
#                 button = ToggleButton(id=group, text=group_name)
#                 button.bind(on_press=self.handle_group_release)
#                 self.group_switch_buttons[group] = button
#                 layout.add_widget(button)

#     def colorize_buttons(self):
#         for group, button in self.group_switch_buttons.items():
#             if self.local_config.digit_group_filled(group):
#                 button.background_color = 0, 1, 0, 1
#             else:
#                 button.background_color = 1, 0, 0, 1

#     def handle_group_release(self, btn: ToggleButton):
#         self.select_group(btn.id)

#     def select_group(self, group_id):
#         for btn in self.group_switch_buttons.values():
#             btn.state = 'normal'

#         btn: ToggleButton = self.group_switch_buttons[group_id]
#         btn.state = 'down'

#         label_names = reversed(get_number_values_for_group(group_id))
#         label_ids = reversed(get_numbers_keys_for_group(group_id))

#         self.unset_input_handlers()
#         for text, label_id, number_input in zip(label_names, label_ids, self.number_inputs()):
#             number_input.ids.label.text = text
#             number_input.ids.input.text = self.local_config.get_value_for(label_id)
#             number_input.ids.input.config_id = label_id

#         self.set_input_handlers()
#         self.current_group_id = group_id

#     def set_input_handlers(self):
#         for number_input in self.number_inputs():
#             number_input.ids.input.bind(text=self.update_text_value)

#     def unset_input_handlers(self):
#         for number_input in self.number_inputs():
#             number_input.ids.input.unbind(text=self.update_text_value)

#     def number_inputs(self):
#         return self.ids.number_input_layout.children

#     def update_text(self, label_id, text):
#         self.local_config.set_value_for(label_id, text)

#     def save_changes(self):
#         for key, value in self.local_config._data.items():
#             self.config.set_value_for(key, value)
#         with open('memory_config.json', 'w') as file_stream:
#             write_config_to_stream(file_stream, self.config)
#         self._to_main_screen()

#     def cancel(self):
#         self.local_config = deepcopy(self.config)
#         self._to_main_screen()

#     def update(self):
#         self.select_group(self.current_group_id)
#         self.colorize_buttons()
    
#     def _to_main_screen(self):
#         self.parent.transition.direction = 'right'
#         self.parent.current = 'main'

#     def update_text_value(self, instance, value):
#         self.local_config.set_value_for(instance.config_id, value)
#         self.colorize_buttons()




class MemoryScreenManager(ScreenManager):
    pass
    # def to_list_screen(self, number_config):
    #     if 'list' not in self.screen_names:
    #         list_screen = ListScreen(name='list', config=number_config)
    #         self.add_widget(list_screen)
    #     self.transition.direction = 'left'
    #     self.current = 'list'
    #     self.current_screen.update()


class MemoryApp(App):

    def read_config_from_disk(self):
        try:
            with open('memory_config.json', 'r') as file_stream:
                # return read_config_from_stream(file_stream)
                pass
        except FileNotFoundError:
            logging.info('No config file found.')
            # return NumberConfig()

    def build(self):
        # self.number_config = self.read_config_from_disk()
        manager = MemoryScreenManager()
        manager.current_screen = 'main'
        return manager


if __name__ == '__main__':
    MemoryApp().run()