import logging
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.config.appconfig import read_config_from_stream, NumberConfig
from src.widget.listscreen import ListScreen
from src.widget.mainscreen import MainScreen



class MemoryScreenManager(ScreenManager):
    
    def to_list_screen(self, number_config: NumberConfig):
        if 'list' not in self.screen_names:
            list_screen = ListScreen(name='list', config=number_config)
            self.add_widget(list_screen)
        
        self.transition.direction = 'left'
        self.current = 'list'


class MemoryApp(App):
    number_config: NumberConfig

    def read_config_from_disk(self):
        try:
            with open('memory_config.json', 'r') as file_stream:
                return read_config_from_stream(file_stream)
        except FileNotFoundError:
            logging.info('No config file found.')
            return NumberConfig()

    def build(self):
        self.number_config = self.read_config_from_disk()
        return MemoryScreenManager()


if __name__ == '__main__':
    MemoryApp().run()