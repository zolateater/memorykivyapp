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
from src.config.appconfig import NumberConfig
from src.widget.listscreen import ListScreen, NumberInputGroup
from src.widget.mainscreen import MainScreen, ButtonBoxMenu, MenuButton


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
        print("BEFORE BUILD")
        self.number_config = self.read_config_from_disk()
        return MemoryScreenManager()


if __name__ == '__main__':
    print("BEFORE APP RUN")
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
have to move everything to another method
putting everything in different files breaks the app

"""