import argparse
import time

import os
from kivy.core.window import Window
from kivy.logger import Logger

from ButtonController import ButtonController
from SegmentDisplayController import SegmentDisplayController
from controller.Camera4Controller import Camera4Controller
from util.Collage4Creator import Collage4Creator
from util.ConfUtil import ConfUtil
from util.ImageResize import ImageResize
#from util.InstagramUpload import InstagramUpload
from util.PhotoStore import PhotoStore
from util.PrintSpooler import PrintSpooler


class Controller(object):
    conf = None
    collage_screen = None
    collage_print = None
    last_log_id = None

    max_wait_time_for_print_image = 10  # seconds

    def __init__(self, app):
        self.app = app
        self.init_conf()

    def start(self):
        self.button = ButtonController(self)
        self.camera = Camera4Controller(self, self.conf.get("photo.path_target") + self.conf.get("photo.path_originals"))
        self.creator = Collage4Creator()
        self.resizer = ImageResize(self.conf.get("photo.path_target") + self.conf.get("photo.path_resized"),
                                   Window.size[0],
                                   Window.size[1])

        self.camera.initCamera()
        self.button.start()

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

        seg_display = SegmentDisplayController(self, self.conf.get("segment_display.time_to_prepare"))
        seg_display.start()

        # wait for trigger delay
        trigger_delay = self.conf.get("camera.trigger_delay")
        time_to_prepare = self.conf.get("app.time_to_prepare")

        time.sleep(time_to_prepare - trigger_delay)

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

    def check_print_image_ready(self):
        ''' check if print image creation is finished! '''
        sleep_time = 0.5 # seconds

        counter = 0
        image_ready = os.path.isfile(self.collage_print)
        while counter < (self.max_wait_time_for_print_image / sleep_time) and not image_ready:
            time.sleep(sleep_time)
            counter = counter + 1

            image_ready = os.path.isfile(self.collage_print)

    def print_image(self, nb_copies):
        Logger.info('Printing {0} copies'.format(nb_copies))

        # print (check if print image creation is finished!)
        image_ready = self.check_print_image_ready()

        if image_ready:
            # print
            with PrintSpooler as ps:
                ps.print_image_async(self.conf.get("printer.cups_name"), self.collage_print, nb_copies)
        else:
            Logger.error("Error while printing. Image {0} not ready after waiting {1}s.".format(self.collage_print, self.max_wait_time_for_print_image))


        self.show_loop_screen()

        # update photolog
        with PhotoStore() as ps:
            ps.update_log(
                self.last_log_id,
                nb_copies
            )

    # on return from operations by secret gesture
    def show_admin_screen(self):
        self.app.show_admin_screen()

    # after printing or on abort print dialog
    def show_loop_screen(self):
        self.app.show_loop_screen()

    # to operations by clicked mode
    def switch_mode(self, type):
        self.prepare_conf(type)
        self.app.switch_mode()
