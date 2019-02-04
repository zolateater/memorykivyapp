from kivy.uix.boxlayout import BoxLayout


class NumberGroupSelector(BoxLayout):

    def get_wrappers(self):
        yield self.ids.group_wrapper_1
        yield self.ids.group_wrapper_2
        yield self.ids.group_wrapper_3

    def get_checkboxes(self):
        for wrapper in self.get_wrappers():
            for child in wrapper.children:
                if isinstance(child, NumberGroupCheckbox):
                    yield child

    def select_all(self):
        [checkbox.press() for checkbox in self.get_checkboxes() if not checkbox.is_selected()]

    def deselect_all(self):
        [checkbox.press() for checkbox in self.get_checkboxes() if checkbox.is_selected()]


class NumberGroupCheckbox(BoxLayout):
    def press(self):
        self.ids.checkbox._do_press()

    def is_selected(self):
        return self.ids.checkbox.active
