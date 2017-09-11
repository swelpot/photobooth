from kivy.graphics import Color
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, Clock
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger

class ShowImageScreen(Screen):
    image_path = ObjectProperty()
    obj_lbl_print_copies = ObjectProperty()

    r = NumericProperty(0.0)
    g = NumericProperty(0.0)
    b = NumericProperty(0.0)
    a = NumericProperty(0.5)

    pos_x = NumericProperty()

    event = None

    def __init__(self, controller):
        super(ShowImageScreen, self).__init__()
        self.controller = controller

    def switch_mode(self):
        self.r = float(self.controller.get_conf("app.video_background_color_r")) / 255.0
        self.g = float(self.controller.get_conf("app.video_background_color_g")) / 255.0
        self.b = float(self.controller.get_conf("app.video_background_color_b")) / 255.0

    def set_image(self, image):
        Logger.debug("ShowImageScreen.set_image() with {0}".format(image))
        self.image_path.source = image

        if self.controller.get_conf("app.printing_enabled"):
            # show print dialog after x seconds if printing enabled
            self.event = Clock.schedule_once(self.show_print_dialog, self.controller.get_conf("app.show_image_duration"))

    def on_touch_up(self, touch):
        Logger.debug("Touch UP: x: {0}, y: {1}".format(touch.px, touch.py))

        # show print dialog when screen pressed
        if self.controller.get_conf("app.printing_enabled"):
            self.event.cancel()
            self.show_print_dialog()

    def print_image(self):
        nb_copies = int(self.obj_lbl_print_copies.text)
        Logger.info('Printing {0} copies'.format(nb_copies))

        # print (check if print image creation is finished!)

        self.abort_print_dialog()

    def show_print_dialog(self, *args):
        Logger.debug('ShowImageScreen.show_print_dialog()')

        self.pos_x = 500

    def hide_print_dialog(self, *args):
        Logger.debug('ShowImageScreen.hide_print_dialog()')

        self.pos_x = 5000

    def abort_print_dialog(self):
        self.controller.show_loop_screen()
        self.hide_print_dialog()

Builder.load_file("screens/ShowImageScreen.kv")