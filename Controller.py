from kivy.logger import Logger
import time
from ButtonController import ButtonController
from CameraController import CameraController
from CameraControllerDummy import CameraControllerDummy
from CollageCreator import CollageCreator
from ImageResize import ImageResize
from SegmentDisplayController import SegmentDisplayController


class Controller():
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def start(self):
        self.button = ButtonController(self)
        self.seg_display = SegmentDisplayController(self, self.conf.get("segment_display.time_to_prepare"))
        self.camera = CameraController(self, self.conf.get("photo.path_target") + self.conf.get("photo.path_originals"))
        self.creator = CollageCreator()
        self.resizer = ImageResize(self.conf.get("photo.path_target") + self.conf.get("photo.resized"),
                                   self.conf.get("display.width"),
                                   self.conf.get("display.height"))

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
        #photos=['../IMG_5864.JPG']

        collage = self.creator.collage(photos)
        resized = self.resizer.resize(collage)

        # update gui image
        self.app.update_image(resized)

        self.button.lights_on()


