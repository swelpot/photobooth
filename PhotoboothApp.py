import argparse
import json
import logging
import pprint
import warnings

import kivy
kivy.require('1.10.0')

from util.LoggerPatch import LoggerPatch
from controller.ControllerDummy import ControllerDummy
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


class ScreenManagement(ScreenManager):
    pass


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
        # controller = Controller(mainApp)
        self.controller = ControllerDummy(self)
        self.controller.start()

        self.sm = ScreenManagement(transition=CardTransition())
        self.scr_admin = AdminScreen(self.controller)
        self.scr_loop_video = LoopVideoScreen(self.controller)
        self.scr_button_pressed = ButtonPressedScreen()
        self.scr_image = ShowImageScreen()

        Clock.schedule_interval(self._button_pressed, 0.1)
        Clock.schedule_interval(self._show_image, 0.5)

        self.scr_admin.update()

        self.sm.add_widget(self.scr_admin)
        self.sm.add_widget(self.scr_loop_video)
        self.sm.add_widget(self.scr_button_pressed)
        self.sm.add_widget(self.scr_image)

        return self.sm

    def init_videos(self):
        self.scr_loop_video.init_video(self.controller.get_conf("app.video_loop"))
        self.scr_button_pressed.init_video(self.controller.get_conf("app.video_buttonpressed"))

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
            Clock.schedule_once(self.show_loop_screen, self.controller.get_conf("app.show_image_duration"))

    def show_loop_screen(self, *args):
        Logger.debug("MainApp.show_loop_screen()")
        self.scr_loop_video.play()
        self.sm.current = 'loop_video'
        self.scr_admin.stop_log_read()

    def show_button_pressed_screen_async(self):
        self.button_pressed = True

    def show_image_screen_async(self, imagepath):
        Logger.debug("MainApp.update_image() with {0}".format(imagepath))
        self.image_path = imagepath
        self.image_updated = True

    def show_admin_screen(self):
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
