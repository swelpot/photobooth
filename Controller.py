from kivy.logger import Logger
import time
from ButtonController import ButtonController
from CameraController import CameraController
from CameraControllerDummy import CameraControllerDummy
from CollageCreator import CollageCreator
from SegmentDisplayController import SegmentDisplayController


class Controller():
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def start(self):
        self.button = ButtonController(self)
        self.seg_display = SegmentDisplayController(self, self.conf.get("segment_display.time_to_prepare"))
        self.camera = CameraController(self, self.conf.get("photo.target_path"))
        self.creator = CollageCreator(self)

        self.camera.initCamera()
        self.button.start()

    def button_pressed(self):
        Logger.debug("Controller.buttonPressed()")
        self.button.lights_off()

        # trigger switch to countdown screen
        self.app.update_button_pressed()

        self.seg_display.start()

        # wait for trigger delay
        time.sleep(self.conf.get("photo.trigger_delay"))
        # shoot photo
        photos = self.camera.shoot()
        photos=['../IMG_5864.JPG']

        collage = self.creator.collage(photos)

        # update gui image
        self.app.update_image(collage)

        self.button.lights_on()


