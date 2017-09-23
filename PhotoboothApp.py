IS_DUMMY = False

import logging
import kivy
kivy.require('1.10.0')

from kivy.properties import NumericProperty

from util.LoggerPatch import LoggerPatch
from screens.AdminScreen import AdminScreen
from screens.ButtonPressedScreen import ButtonPressedScreen
from screens.LoopVideoScreen import LoopVideoScreen
from screens.ShowImageScreen import ShowImageScreen

from kivy.config import Config
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, CardTransition


if not IS_DUMMY:
    from controller.Controller import Controller
else:
    from controller.ControllerDummy import Controller


class ScreenManagement(ScreenManager):
    r = NumericProperty(0.0)
    g = NumericProperty(0.0)
    b = NumericProperty(0.0)

    def update_backgroup(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class MainApp(App):
    controller = None
    sm = None
    scr_admin = None
    scr_loop_video = None
    scr_button_pressed = None
    scr_image = None

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

        self.button_pressed = False
        self.image_updated = False
        self.image_path = ''

    def build(self):
        Logger.debug("MainApp.build()")
        self.controller = Controller(mainApp)
        #self.controller = ControllerDummy(self)
        self.controller.start()

        self.sm = ScreenManagement(transition=CardTransition())
        self.sm.mode = 'pop' # 'push'
        self.sm.direction = 'left'

        self.scr_admin = AdminScreen(self.controller)
        self.scr_loop_video = LoopVideoScreen(self.controller)
        self.scr_button_pressed = ButtonPressedScreen()
        self.scr_image = ShowImageScreen(self.controller)

        Clock.schedule_interval(self._button_pressed, 0.1)
        Clock.schedule_interval(self._show_image, 0.5)

        self.scr_admin.update()

        self.sm.add_widget(self.scr_admin)
        self.sm.add_widget(self.scr_loop_video)
        self.sm.add_widget(self.scr_button_pressed)
        self.sm.add_widget(self.scr_image)

        return self.sm

    def _init_videos(self):
        self.scr_loop_video.init_video(self.controller.get_conf("app.video_loop"))
        self.scr_button_pressed.init_video(self.controller.get_conf("app.video_buttonpressed"))

    def _init_background(self):
        self.sm.update_backgroup(
            float(self.controller.get_conf("app.video_background_color_r")) / 255.0,
            float(self.controller.get_conf("app.video_background_color_g")) / 255.0,
            float(self.controller.get_conf("app.video_background_color_b")) / 255.0)

    # re-init when mode changed
    def switch_mode(self):
        self._init_videos()
        self._init_background()

        self.scr_image.switch_mode()
        self.show_loop_screen()

    def _button_pressed(self, *args):
        if self.button_pressed:
            Logger.debug("MainApp._button_pressed()")

            self.button_pressed = False
            self.scr_button_pressed.play()
            self.sm.current = 'button_pressed'

            self.scr_loop_video.stop()

    def _show_image(self, *args):
        if self.image_updated:
            Logger.debug("MainApp._show_image(): Updating image with {}".format(self.image_path))

            self.image_updated = False
            self.scr_image.set_image(self.image_path)
            self.sm.current = 'show_image'

            self.scr_button_pressed.stop()
            if not self.controller.get_conf("app.printing_enabled"):
                # trigger screen change after x seconds only if printing disabled
                Clock.schedule_once(self.show_loop_screen, self.controller.get_conf("app.show_image_duration"))

    def show_loop_screen(self, *args):
        Logger.debug("MainApp.show_loop_screen()")
        self.scr_loop_video.play()
        self.sm.current = 'loop_video'
        self.scr_admin.stop_log_read()

    def show_button_pressed_screen_async(self):
        self.button_pressed = True

    def show_image_screen_async(self, image_screen):
        Logger.debug("MainApp.update_image() with {0}".format(image_screen))
        self.image_path = image_screen
        self.image_updated = True

    def show_admin_screen(self):
        # set background like video and track changes in size/position
        self.sm.update_backgroup(0.0, 0.0, 0.0)

        self.scr_admin.start_log_read()
        self.scr_admin.update()
        self.sm.current = 'admin'


if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    logging.root = Logger

    # # construct the argument parser and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-c", "--conf", default="conf.json", dest="conf", help="path to the JSON configuration file")
    # #ap.add_argument("-lf", "--logfile", default="photobooth.log", dest="logfile", help="logfile path")
    # args = vars(ap.parse_args())
    #
    # # Logger.basicConfig(#filename=args["logfile"],
    # #                     format='%(asctime)-15s [%(levelname)-6s] %(message)s',
    # #                     level=logging.DEBUG)
    # #
    # warnings.filterwarnings("ignore")
    # conf = json.load(open(args.get("conf")))
    # pp = pprint.PrettyPrinter(indent=4)
    # Logger.info("Loaded Json config\n{}".format(pp.pformat(conf)))

    Builder.load_file("Photobooth.kv")
    # Window.fullscreen = 'auto'
    mainApp = MainApp()
    #Window.size = (1280, 800)


    mainApp.run()
