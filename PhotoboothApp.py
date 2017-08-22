import argparse
import warnings
import json
import pprint
import kivy

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

    def setImage(self, image):
        Logger.debug("ShowImageScreen.setImage()")
        self.image_path.source = image

class ScreenManagement(ScreenManager):
    pass


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.scrLoopVideo = LoopVideoScreen()
        self.scrButtonPressed = ButtonPressedScreen()
        self.scrImage = ShowImageScreen()

    def build(self):
        Logger.debug("MainApp.build()")
        self.scrLoopVideo.init_video(conf.get("app.video_loop"))
        self.scrButtonPressed.init_video(conf.get("app.video_buttonpressed"))

        self.sm = ScreenManagement()
        self.sm.add_widget(self.scrLoopVideo)
        self.sm.add_widget(self.scrButtonPressed)
        self.sm.add_widget(self.scrImage)

        return self.sm

    def buttonPressed(self):
        Logger.debug("MainApp.buttonPressed()")
        self.scrLoopVideo.stop()
        self.scrButtonPressed.play()
        self.sm.current = 'button_pressed'

    def showImage(self, imagepath):
        Logger.debug("MainApp.showImage() with {0}".format(imagepath))
        self.scrImage.setImage(imagepath)
        self.sm.current = 'show_image'

    def showLoopVideo(self):
        Logger.debug("MainApp.showLoopVideo()")
        self.scrLoopVideo.play()
        self.sm.current = 'loop_video'


if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conf", default="conf.json", dest="conf", help="path to the JSON configuration file")
    ap.add_argument("-lf", "--logfile", default="photobooth.log", dest="logfile", help="logfile path")
    args = vars(ap.parse_args())

    # Logger.basicConfig(#filename=args["logfile"],
    #                     format='%(asctime)-15s [%(levelname)-6s] %(message)s',
    #                     level=logging.DEBUG)
    #
    warnings.filterwarnings("ignore")
    conf = json.load(open(args.get("conf")))
    pp = pprint.PrettyPrinter(indent=4)
    Logger.info("Loaded Json config\n{}".format(pp.pformat(conf)))

    presentation = Builder.load_file("main.kv")
    # Window.fullscreen = 'auto'
    mainApp = MainApp()

    controller = Controller(mainApp)
    controller.start()

    mainApp.run()
