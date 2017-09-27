import argparse
import time
from threading import Thread

from kivy.core.window import Window
from kivy.logger import Logger

from SegmentDisplayController import SegmentDisplayController
from controller.ButtonControllerDummy import ButtonController
from controller.Camera4ControllerDummy import Camera4Controller
from util.Collage4Creator import Collage4Creator
from util.ConfUtil import ConfUtil
from util.ImageResize import ImageResize
#from util.InstagramUpload import InstagramUpload
from util.PhotoStore import PhotoStore


class Controller(object):
    conf = None
    collage_screen = None
    collage_print = None

    def __init__(self, app):
        self.app = app
        self.init_conf()

    def start(self):
        self.button = ButtonControllerDummy(self)
        self.camera = Camera4Controller()
        self.creator = Collage4Creator()
        #        self.resizer = ImageResizeDummy()
        self.resizer = ImageResize(self.conf.get("photo.path_target") + self.conf.get("photo.path_resized"),
                                   Window.size[0],
                                   Window.size[1])
        self.seg_display = SegmentDisplayController()

        self.camera.initCamera()
        # self.button.start()

    def init_conf(self):
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-cf", "--conffile", default="conf.json", dest="conf", help="path to the JSON configuration file")
        args = vars(ap.parse_args())

        conf_file = args.get("conf")
        self.conf = ConfUtil.load_json_conf(conf_file)

    def prepare_conf(self, type):
        conf_file_mode = self.conf.get("controller.mode_conf_{0}".format(type))
        mode_conf = ConfUtil.load_json_conf(conf_file_mode)
        self.conf.update(mode_conf)

        # update conf in workers
        self.creator.set_conf(self.conf)

    def get_conf(self, key):
        return self.conf.get(key)

    def button_pressed(self):
        Logger.debug("Controller.buttonPressed()")
        self.button.lights_off()

        # trigger switch to countdown screen
        self.app.show_button_pressed_screen_async()

        trigger_delay = self.conf.get("camera.trigger_delay")
        time_to_prepare = self.conf.get("app.time_to_prepare")
        seg_disp_time = self.conf.get("segment_display.time_to_prepare")

        self.seg_display.run_countdown_trigger(seg_disp_time,
                                               time_to_prepare - seg_disp_time)

        # wait for trigger delay
        time.sleep(time_to_prepare - trigger_delay)

        # run worker to update segment display after trigger delay
        std = SegementTriggerDelay(self.seg_display.run_countdown_photo, 4, trigger_delay)
        std.start()

        # shoot photo
        photos = self.camera.shoot()

        self.collage_screen = self.creator.collage_screen(photos)
        self.collage_print = self.creator.collage_print_async(photos)
        #resized = self.resizer.resize(collage)

        # update gui image
        self.app.show_image_screen_async(self.collage_screen)

        self.button.lights_on()

        with PhotoStore() as ps:
            self.last_log_id = ps.add_log(self.conf.get("project_name"),
                                          self.collage_print,
                                          0)

        # if self.conf.get("instagram.enabled"):
        #     iu = InstagramUpload(self.conf.get("instagram.username"),
        #                          self.conf.get("instagram.password"),
        #                          self.collage_print,
        #                          self.conf.get("instagram.hashtag"))
        #     iu.start()


    def print_image(self, nb_copies):
        Logger.info('Printing {0} copies'.format(nb_copies))

        # print (check if print image creation is finished!)
        with PhotoStore() as ps:
            ps.update_log(
                self.last_log_id,
                nb_copies
            )

        self.show_loop_screen()

    # on return from operations by secret gesture
    def show_admin_screen(self):
        self.app.show_admin_screen()

    # after printing or on abort print dialog
    def show_loop_screen(self):
        self.button.lights_on()
        self.seg_display.run_loop()
        self.app.show_loop_screen()

    # to operations by clicked mode
    def switch_mode(self, type):
        self.prepare_conf(type)
        self.app.switch_mode()

class SegementTriggerDelay(Thread):
    _callable = None
    _arg = None
    _delay = None

    def __init__(self, callable, arg, delay):
        super(SegementTriggerDelay, self).__init__()
        self._callable = callable
        self._arg = arg
        self._delay = delay

    def run(self):
        time.sleep(self._delay)
        self._callable(self.arg)