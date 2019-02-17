import logging
import os

from kivy.app import App
from kivy.base import EventLoop
from kivy.uix.screenmanager import ScreenManager, Screen

from src.config.app_state import AppState
from src.config.number_config import NumberConfig, read_config_from_stream
from src.widget.base_screen import BaseScreen
from src.widget.list_screen import ListScreen
from src.widget.sequence_check_screen import SequenceCheckScreen
from src.widget.sequence_result_screen import SequenceResultScreen
from src.widget.training_sequence_settings_screen import TrainingScreen, TrainingSelectionScreen, TrainingSettings, \
    TrainingSequenceSettingsScreen
from src.widget.training_sequence_screen import TrainingSequenceScreen
from kivy.core.window import Window


Window.softinput_mode = 'below_target'
ESC_BUTTON = 27


class MemoryScreenManager(ScreenManager):

    SCREEN_PARENTS = {
        'list': 'main',
        'training_selection': 'main',
        'training_sequence_settings': 'training_selection',
        'training_sequence': 'training_sequence_settings',
        'sequence_check': 'training_sequence_settings',
        'sequence_result': 'main',
    }

    SCREEN_NAME_TO_CLASS = {
        'list': ListScreen,
        'training_selection': TrainingSelectionScreen,
        'training_sequence_settings': TrainingSequenceSettingsScreen,
        'training_sequence': TrainingSequenceScreen,
        'sequence_check': SequenceCheckScreen,
        'sequence_result': SequenceResultScreen
    }

    def __init__(self, app_state, **kw):
        """

        :param AppState sequence:
        :param kw:
        """
        super(MemoryScreenManager, self).__init__(**kw)
        self.state = app_state

    # screen manager should have access to config - thus we will be able to encapsulate screen changes

    def back(self):
        parent = self.SCREEN_PARENTS.get(self.current_screen.name)
        if parent is None:
            raise Exception('No parent for current_screen = {}'.format(self.current_screen.name))
        self.__back_to_screen(parent)

    def to_screen(self, screen_name):
        if screen_name not in self.screen_names:
            self.add_widget(self.__build_screen(screen_name))
        parent = self.SCREEN_PARENTS.get(self.current_screen.name, None)

        if screen_name == parent:
            self.__back_to_screen(screen_name)
        else:
            self.__forward_to_screen(screen_name)

        if not isinstance(self.current_screen, BaseScreen):
            raise TypeError('All screens must be derived from BaseScreen class.')

        self.current_screen.update_state(self.state)

    def __forward_to_screen(self, screen_name):
        """
        Changes active screen using forward animation
        :param str screen_name:
        :return:
        """
        self.transition.direction = 'left'
        self.current = screen_name

    def __back_to_screen(self, screen_name):
        """
        Changes active screen using back animation
        :param str screen_name:
        :return:
        """

        self.transition.direction = 'right'
        self.current = screen_name

    def __build_screen(self, screen_name):
        """
        Screen factory method
        :param str screen_name:
        :rtype: BaseScreen
        """
        if screen_name in self.SCREEN_NAME_TO_CLASS:
            screen_class = self.SCREEN_NAME_TO_CLASS[screen_name]
            return screen_class(name=screen_name)

        raise Exception('Unknown screen type - ' + screen_name)

    def to_main_screen(self):
        self.__back_to_screen('main')


def read_config_from_disk(path):
    """
    :param str path:
    :rtype: NumberConfig
    """
    try:
        if not os.path.exists(path):
            return NumberConfig()
        with open(path, 'r') as file_stream:
            return read_config_from_stream(file_stream)
    except FileNotFoundError:
        logging.info('No config file found.')
        return NumberConfig()
    except Exception as e:
        logging.exception("Cannot read the file")
        return NumberConfig()


class MemoryApp(App):

    def get_application_config(self, **kwargs):
        """
        :param kwargs:
        :return: path to config file
        :rtype: str
        """
        return super(MemoryApp, self).get_application_config('~/.memory_config.json')

    def build(self):
        app_state = AppState(
            number_config=read_config_from_disk(self.get_application_config()),
            training_settings=TrainingSettings(numbers_count=10, time_per_number=10),
            remember_sequence=[],
            answers=[]
        )

        return MemoryScreenManager(app_state)

    def on_stop(self):
        return True

    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.on_keypress)

    def on_keypress(self, window, key, *args):
        if key == ESC_BUTTON and self.root.current_screen.name != 'main':
            self.root.back()
            return True


if __name__ == '__main__':
    MemoryApp().run()
