import logging
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from src.config.number_config import NumberConfig
from src.widget.list_screen import ListScreen
from src.widget.training_sequence_settings_screen import TrainingScreen, TrainingSelectionScreen, TrainingSettings, \
    TrainingSequenceSettingsScreen
from src.widget.training_sequence_screen import TrainingSequenceScreen


class MemoryScreenManager(ScreenManager):

    SCREEN_PARENTS = {
        'list': 'main',
        'training_selection': 'main',
        'training_sequence_settings': 'training_selection',
        'training_sequence': 'training_sequence_settings'
    }

    def set_up(self, number_config):
        self.number_config = number_config
        # TODO: take value from settings
        self.training_settings = TrainingSettings(numbers_count=10, time_per_number=10)

    # screen manager should have access to config - thus we will be able to encapsulate screen changes

    def back(self):
        parent = self.SCREEN_PARENTS.get(self.current_screen.name)
        if parent is None:
            raise Exception('No parent for current_screen = {}'.format(self.current_screen.name))
        self.__back_to_screen(parent)

    def set_answer_sequence(self, seq):
        """

        :param set seq:
        :return:
        """
        self.answer_sequence = seq

    def to_screen(self, screen_name):
        if screen_name not in self.screen_names:
            self.add_widget(self.__build_screen(screen_name))
        parent = self.SCREEN_PARENTS.get(self.current_screen.name, None)

        # TODO: check time and memory consumption for removing each screen or recreating it

        if screen_name == parent:
            self.__back_to_screen(screen_name)
        else:
            self.__forward_to_screen(screen_name)

        # TODO: remove this crunch by notification of a
        #  screen or removing it on switch
        if hasattr(self.current_screen, 'update'):
            self.current_screen.update()

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
        :return Screen:
        """
        if screen_name == 'list':
            screen = ListScreen(name='list')
            screen.set_up(config=self.number_config)
            return screen
        if screen_name == 'training_selection':
            return TrainingSelectionScreen(name='training_selection')
        if screen_name == 'training_sequence_settings':
            screen = TrainingSequenceSettingsScreen(name=screen_name)
            screen.set_up(self.training_settings)
            return screen
        if screen_name == 'training_sequence':
            return TrainingSequenceScreen(name=screen_name, settings=self.training_settings,
                                          number_config=self.number_config)

        raise Exception('Unknown screen type - ' + screen_name)

    def to_main_screen(self):
        self.__back_to_screen('main')


def read_config_from_disk():
    try:
        # with open('memory_config.json', 'r') as file_stream:
        return NumberConfig()
        # return read_config_from_stream(file_stream)
    except FileNotFoundError:
        logging.info('No config file found.')
        return NumberConfig()
    except Exception as e:
        logging.exception("Cannot read the file")
        return NumberConfig()


class MemoryApp(App):
    def build(self):
        msm = MemoryScreenManager()
        msm.set_up(read_config_from_disk())
        return msm


if __name__ == '__main__':
    MemoryApp().run()
