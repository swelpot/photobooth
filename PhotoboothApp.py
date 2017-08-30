import argparse
import json
import logging
import pprint
import warnings

import kivy
from kivy.core.window import Window

from controller.ControllerDummy import ControllerDummy

kivy.require('1.10.0')

from kivy.config import Config
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition


class LoopVideoScreen(Screen):
    video_loop = ObjectProperty()

    def __init__(self, conf):
        super(LoopVideoScreen, self).__init__()
        self.conf = conf

        #self.display_width = self.conf.get("display.width")
        #self.display_height = self.conf.get("display.height")
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

        Logger.debug("DOWN: x: {0}, y: {1}".format(touch.px, touch.py))
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
        Logger.debug("UP: x: {0}, y: {1}".format(touch.px, touch.py))
        if self.admin_key_started3 and touch.px < self.admin_key_tol_x and touch.py > (self.display_height - self.admin_key_tol_y):
            print "ADMIN"

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
        self.scr_loop_video = LoopVideoScreen(conf)
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

        self.sm = ScreenManagement(transition=CardTransition())
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

    #controller = Controller(mainApp, conf)
    controller = ControllerDummy(mainApp, conf)
    controller.start()

    mainApp.run()
