IS_DUMMY = False

import logging
import kivy
kivy.require('1.10.0')

from kivy.properties import StringProperty, ObjectProperty

from kivy.config import Config
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, CardTransition, Screen

class ScreenManagement(ScreenManager):
    pass

class ShowImageScreen2(Screen):
    str_image1 = StringProperty()
    str_image2 = StringProperty()
    str_image3 = StringProperty()
    str_image4 = StringProperty()
    obj_image1 = ObjectProperty()
    obj_image2 = ObjectProperty()
    obj_image3 = ObjectProperty()
    obj_image4 = ObjectProperty()

    def __init__(self):
        super(ShowImageScreen2, self).__init__()

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

    def build(self):
        Logger.debug("MainApp.build()")

        self.sm = ScreenManagement(transition=CardTransition())
        self.sm.mode = 'pop' # 'push'
        self.sm.direction = 'left'

        self.scr_image = ShowImageScreen2()

        Clock.schedule_once(self._button_pressed, 3)
        self.sm.add_widget(self.scr_image)

        return self.sm


    def _button_pressed(self, *args):
        Logger.info("Update")
        self.scr_image.str_image1 = '../photos/resized/_MG_6161.JPG'
        self.scr_image.str_image2 = '../photos/resized/_MG_6162.JPG'
        self.scr_image.str_image3 = '../photos/resized/_MG_6163.JPG'
        self.scr_image.str_image4 = '../photos/resized/_MG_6164.JPG'



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

    Builder.load_file("ShowImageScreen2.kv")
    # Window.fullscreen = 'auto'
    mainApp = MainApp()
    #Window.size = (1280, 800)


    mainApp.run()
