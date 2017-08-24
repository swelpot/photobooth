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

    def buttonPressed(self):
        Logger.debug("Controller.buttonPressed()")
        self.button.lightsOff()
        self.app.buttonPressed()
        self.seg_display.start()
        time.sleep(2)
        photos = self.camera.shoot()
        collage = self.creator.collage(photos)
        self.app.show_image(collage)
        #time.sleep(10)
        #self.app.show_loop_video()


