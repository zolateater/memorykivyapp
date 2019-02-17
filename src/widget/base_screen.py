from kivy.uix.screenmanager import Screen


class BaseScreen(Screen):

    def update_state(self, state):
        """
        Called each time screen becomes active

        :param src.config.app_state.AppState state:
        :return:
        """
        pass
