from kivy.graphics import Color
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, Clock, StringProperty, ListProperty
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger

from util.PhotoStore import PhotoStore


class ShowImageScreen(Screen):
    obj_lbl_print_copies = ObjectProperty()

    str_image1 = StringProperty()

    r = NumericProperty(0.0)
    g = NumericProperty(0.0)
    b = NumericProperty(0.0)

    list_pos_print_dialog = ListProperty()
    org_pos_print_dialog = None

    event = None

    def __init__(self, controller):
        super(ShowImageScreen, self).__init__()
        self.controller = controller

        # initial hide of print dialog
        Clock.schedule_once(self._hide_print_dialog, 10)

    def switch_mode(self):
        self.r = float(self.controller.get_conf("app.video_background_color_r")) / 255.0
        self.g = float(self.controller.get_conf("app.video_background_color_g")) / 255.0
        self.b = float(self.controller.get_conf("app.video_background_color_b")) / 255.0

    def set_image(self, image):
        Logger.debug("ShowImageScreen.set_image() with {0}".format(image))
        self.str_image1 = image

        if self.controller.get_conf("app.printing_enabled"):
            # show print dialog after x seconds if printing enabled
            self.event = Clock.schedule_once(self._show_print_dialog, self.controller.get_conf("app.show_image_duration"))

    def on_touch_up(self, touch):
        Logger.debug("Touch UP: x: {0}, y: {1}".format(touch.px, touch.py))

        # show print dialog when screen pressed
        if self.controller.get_conf("app.printing_enabled"):
            self.event.cancel()
            self._show_print_dialog()

    def print_image(self):
        """ called from kv file """
        nb_copies = int(self.obj_lbl_print_copies.text)
        self.controller.print_image(nb_copies)

        self._hide_print_dialog()

    def abort_print_dialog(self):
        """ called from kv file """
        self.controller.show_loop_screen()

        # cancel Clock if present
        if self.event:
            self.event.cancel()

        self._hide_print_dialog()

    def _show_print_dialog(self, *args):
        Logger.debug('ShowImageScreen.show_print_dialog()')

        self.list_pos_print_dialog[0] = self.org_pos_print_dialog

    def _hide_print_dialog(self, *args):
        Logger.debug('ShowImageScreen.hide_print_dialog()')

        self.org_pos_print_dialog = self.list_pos_print_dialog[0]
        self.list_pos_print_dialog[0] = 10000
        self.obj_lbl_print_copies.text = '1'

#Builder.load_file("screens/ShowImagePrintDialog.kv")
Builder.load_file("screens/ShowImageScreen.kv")