from LoggerPatch import LoggerPatch

import argparse
import warnings
import json
import pprint
import logging
import kivy
import time

kivy.require('1.10.0')

from Controller import Controller
from kivy.config import Config
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen


class LoopVideoScreen(Screen):
    video_loop = ObjectProperty()

    def __init__(self):
        super(LoopVideoScreen, self).__init__()

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
        
    def on_touch_down(self, touch):
        print(touch)
    def on_touch_move(self, touch):
        print(touch)
    def on_touch_up(self, touch):
        print("RELEASED!",touch)        

class ButtonPressedScreen(Screen):
    video_buttonpressed = ObjectProperty()

    def init_video(self, video_files):
        Logger.debug("ButtonPressedScreen.init_video()")
        self.video_buttonpressed.source = video_files

    def play(self):
        Logger.debug("ButtonPressedScreen.play()")
        self.video_buttonpressed.position = 0
        self.video_buttonpressed.state = 'play'


class ShowImageScreen(Screen):
    image_path = ObjectProperty()

    def set_image(self, image):
        Logger.debug("ShowImageScreen.set_image() with {0}".format(image))
        self.image_path.source = image #"../IMG_0142.jpg"

class ScreenManagement(ScreenManager):
    pass


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.scr_loop_video = LoopVideoScreen()
        self.scr_button_pressed = ButtonPressedScreen()
        self.scr_image = ShowImageScreen()

        self.button_pressed = False
        self.image_updated = False
        self.image_path = ''

    def build(self):
        Logger.debug("MainApp.build()")
        Clock.schedule_interval(self.inner_button_pressed, 0.1)
        Clock.schedule_interval(self.inner_show_image, 0.5)

        self.init_video()

        self.sm = ScreenManagement()
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

    presentation = Builder.load_file("PhotoboothApp.kv")
    # Window.fullscreen = 'auto'
    mainApp = MainApp()

    controller = Controller(mainApp, conf)
    controller.start()

    mainApp.run()
