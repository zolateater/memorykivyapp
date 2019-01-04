from weakref import WeakValueDictionary
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from src.config.appconfig import NumberConfig, write_config_to_stream
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


class ListScreen(Screen):
    def __init__(self, config: NumberConfig, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.local_config = deepcopy(config) 
        self.current_group_id = '0'
        self.group_switch_buttons = WeakValueDictionary()
        self.inputs = WeakValueDictionary()
        self.populate_tabs()
        self.colorize_buttons()
        self.select_group(self.current_group_id)

    def get_group_switch_layout(self) -> BoxLayout:
        # Is there a reason why you can't use ids during __init__?
        return self.children[0].children[0].children[2]

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

    def handle_group_release(self, btn: ToggleButton):
        self.select_group(btn.id)

    def select_group(self, group_id):
        for btn in self.group_switch_buttons.values():
            btn.state = 'normal'

        btn: ToggleButton = self.group_switch_buttons[group_id]
        btn.state = 'down'

    def save_changes(self):
        for key, value in self.local_config._data.items():
            self.config.set_value_for(key, value)
        with open('memory_config.json', 'w') as file_stream:
            write_config_to_stream(file_stream, self.config)
        self._to_main_screen()

    def cancel(self):
        self.local_config = deepcopy(self.config)
        self._to_main_screen() 
    
    def _to_main_screen(self):
        self.parent.transition.direction = 'right'
        self.parent.current = 'main'
