import argparse
import json
import logging
import pprint
import warnings

import kivy

from controller.ControllerDummy import ControllerDummy
from screens.ButtonPressedScreen import ButtonPressedScreen
from screens.LoopVideoScreen import LoopVideoScreen
from screens.ShowImageScreen import ShowImageScreen

kivy.require('1.10.0')

from kivy.config import Config
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition



class ScreenManagement(ScreenManager):
    pass


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

        self.button_pressed = False
        self.image_updated = False
        self.image_path = ''

    def build(self):
        Logger.debug("MainApp.build()")
        # controller = Controller(mainApp, conf)
        self.controller = ControllerDummy(self, conf)
        self.controller.start()

        self.sm = ScreenManagement(transition=CardTransition())
        self.scr_loop_video = LoopVideoScreen(conf, self.controller)
        self.scr_button_pressed = ButtonPressedScreen()
        self.scr_image = ShowImageScreen()

        Clock.schedule_interval(self.inner_button_pressed, 0.1)
        Clock.schedule_interval(self.inner_show_image, 0.5)

        self.init_video()

        #self.sm.add_widget(self.scr_start)
        self.sm.add_widget(self.scr_loop_video)
        self.sm.add_widget(self.scr_button_pressed)
        self.sm.add_widget(self.scr_image)

        return self.sm

    def init_video(self):
        self.scr_loop_video.init_video(conf.get("app.video_loop"))
        self.scr_button_pressed.init_video(conf.get("app.video_buttonpressed"))

    def inner_button_pressed(self, *args):
        if self.button_pressed:
            Logger.debug("MainApp.inner_button_pressed()")
            self.button_pressed = False
            self.scr_loop_video.stop()
            self.scr_button_pressed.play()
            self.sm.current = 'button_pressed'

    def inner_show_image(self, *args):
        #Logger.debug("MainApp.show_image()")
        if self.image_updated:
            Logger.debug("MainApp.inner_show_image(): Updating image with {}".format(self.image_path))

            self.image_updated = False
            self.scr_image.set_image(self.image_path)
            self.sm.current = 'show_image'

            Clock.schedule_once(self.inner_show_loop_video, conf.get("app.show_image_duration"))

    def inner_show_loop_video(self, *args):
        Logger.debug("MainApp.show_loop_video()")
        self.scr_loop_video.play()
        self.sm.current = 'loop_video'

    def update_button_pressed(self):
        self.button_pressed = True

    def update_image(self, imagepath):
        Logger.debug("MainApp.update_image() with {0}".format(imagepath))
        self.image_path = imagepath
        self.image_updated = True


if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    logging.root = Logger

    #Config.set('graphics', 'resizable', 0)
    #Config.set('graphics', 'width', '1280')
    #Config.set('graphics', 'height', '800')

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", default="conf.json", dest="conf", help="path to the JSON configuration file")
    #ap.add_argument("-lf", "--logfile", default="photobooth.log", dest="logfile", help="logfile path")
    args = vars(ap.parse_args())

    # Logger.basicConfig(#filename=args["logfile"],
    #                     format='%(asctime)-15s [%(levelname)-6s] %(message)s',
    #                     level=logging.DEBUG)
    #
    warnings.filterwarnings("ignore")
    conf = json.load(open(args.get("conf")))
    pp = pprint.PrettyPrinter(indent=4)
    Logger.info("Loaded Json config\n{}".format(pp.pformat(conf)))

    presentation = Builder.load_file("Photobooth.kv")
    # Window.fullscreen = 'auto'
    mainApp = MainApp()
    #Window.size = (1280, 800)


    mainApp.run()
