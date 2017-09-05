import threading

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger


class LoopVideoScreen(Screen):
    video_loop = ObjectProperty()

    def __init__(self, controller):
        super(LoopVideoScreen, self).__init__()
        self.controller = controller

        self.display_width = Window.size[0]
        self.display_height = Window.size[1]

        self.admin_key_tol_x = self.display_width * 0.1
        self.admin_key_tol_y = self.display_height * 0.1
        self.admin_key_started1 = False
        self.admin_key_started2 = False
        self.admin_key_started3 = False

        Logger.debug("Admin-Key Tolerance {0}/{1}".format(self.admin_key_tol_x, self.admin_key_tol_y))

    def init_video(self, video_files):
        Logger.debug("LoopVideoScreen.init_video()")
        self.video_loop.source = video_files
        self.video_loop.bind(state=self.replay)

    def replay(self, instance, value):
        Logger.debug("LoopVideoScreen.replay() fired by {0} with {1}".format(instance, value))
        if value == "stop":
            self.play()

    def stop(self):
        Logger.debug("LoopVideoScreen.stop()")
        self.video_loop.state = 'pause'

    def play(self):
        Logger.debug("LoopVideoScreen.play()")
        self.video_loop.position = 0
        self.video_loop.state = 'play'

    # Admin-Key control
    def on_touch_down(self, touch):
        self.admin_key_started1 = False
        self.admin_key_started2 = False
        self.admin_key_started3 = False

        Logger.debug("Touch DOWN: x: {0}, y: {1}".format(touch.px, touch.py))
        if touch.px < self.admin_key_tol_x and touch.py < self.admin_key_tol_y:
            self.admin_key_started1 = True
            Logger.debug("Admin-Key1 started")

    def on_touch_move(self, touch):
        if self.admin_key_started1 \
                and not self.admin_key_started2 \
                and touch.px > (self.display_width - self.admin_key_tol_x) \
                and touch.py > (self.display_height - self.admin_key_tol_y):
            self.admin_key_started2 = True
            Logger.debug("Admin-Key2 started")

        if self.admin_key_started2 \
                and not self.admin_key_started3 \
                and touch.px > (self.display_width - self.admin_key_tol_x) \
                and touch.py < self.admin_key_tol_y:
            self.admin_key_started3 = True
            Logger.debug("Admin-Key3 started")

    def on_touch_up(self, touch):
        Logger.debug("Touch UP: x: {0}, y: {1}".format(touch.px, touch.py))
        if self.admin_key_started3 and touch.px < self.admin_key_tol_x and touch.py > (self.display_height - self.admin_key_tol_y):
            Logger.debug("Admin gesture recognized")
            self.controller.show_admin_screen()

        # trigger camera when screen pressed
        if self.controller.get_conf("app.touch_trigger") and not self.admin_key_started1:
            threading.Thread(target=self.controller.button_pressed).start()
