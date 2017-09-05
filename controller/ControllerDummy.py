import argparse
import time

from kivy.core.window import Window
from kivy.logger import Logger

from SegmentDisplayController import SegmentDisplayController
from controller.ButtonControllerDummy import ButtonControllerDummy
from controller.CameraControllerDummy import CameraControllerDummy
from util.CollageCreator import CollageCreator
from util.ConfUtil import ConfUtil
from util.ImageResize import ImageResize


class ControllerDummy():
    conf = None

    def __init__(self, app):
        self.app = app
        self.init_conf()

    def start(self):
        self.button = ButtonControllerDummy(self)
        self.camera = CameraControllerDummy()
        self.creator = CollageCreator()
        #        self.resizer = ImageResizeDummy()
        self.resizer = ImageResize(self.conf.get("photo.path_target") + self.conf.get("photo.path_resized"),
                                   Window.size[0],
                                   Window.size[1])

        self.camera.initCamera()
        # self.button.start()

    def init_conf(self):
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-c", "--conf", default="conf.json", dest="conf", help="path to the JSON configuration file")
        args = vars(ap.parse_args())

        conf_file = args.get("conf")
        self.conf = ConfUtil.load_json_conf(conf_file)

    def prepare_conf(self, type):
        conf_file_mode = self.conf.get("controller.mode_conf_{0}".format(type))
        mode_conf = ConfUtil.load_json_conf(conf_file_mode)
        self.conf.update(mode_conf)

    def get_conf(self, key):
        return self.conf.get(key)

    def button_pressed(self):
        Logger.debug("Controller.buttonPressed()")
        self.button.lights_off()

        # trigger switch to countdown screen
        self.app.show_button_pressed_screen_async()

        seg_display = SegmentDisplayController(self, self.conf.get("segment_display.time_to_prepare"))
        seg_display.start()

        # wait for trigger delay
        time.sleep(self.conf.get("camera.trigger_delay"))
        # shoot photo
        photos = self.camera.shoot()
        #photos=['../IMG_5864.JPG']

        collage = self.creator.collage(photos)
        resized = self.resizer.resize(collage)

        # update gui image
        self.app.show_image_screen_async(resized)

        self.button.lights_on()

    # on return from operations by secret gesture
    def show_admin_screen(self):
        self.app.show_admin_screen()

    # to operations by clicked mode
    def switch_mode(self, type):
        self.prepare_conf(type)
        self.app.init_videos()
        self.app.show_loop_screen()
