import time

from kivy import Logger
from kivy.core.window import Window

from ButtonControllerDummy import ButtonControllerDummy
from CameraControllerDummy import CameraControllerDummy
from SegmentDisplayController import SegmentDisplayController
from util.CollageCreator import CollageCreator
from util.ImageResize import ImageResize


class ControllerDummy():
    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def start(self):
        self.button = ButtonControllerDummy(self)
        self.camera = CameraControllerDummy()
        self.creator = CollageCreator()
#        self.resizer = ImageResizeDummy()
        self.resizer = ImageResize(self.conf.get("photo.path_target") + self.conf.get("photo.path_resized"),
                                   Window.size[0],
                                   Window.size[1])

        self.camera.initCamera()
        self.button.start()

    def button_pressed(self):
        Logger.debug("Controller.buttonPressed()")
        self.button.lights_off()

        # trigger switch to countdown screen
        self.app.update_button_pressed()

        self.seg_display = SegmentDisplayController(self, self.conf.get("segment_display.time_to_prepare"))
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

