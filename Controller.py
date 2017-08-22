from kivy.logger import Logger
import time
from ButtonController import ButtonController
from CameraControllerDummy import CameraControllerDummy
from CollageCreator import CollageCreator

class Controller():
    def __init__(self, app):
        self.app = app

    def start(self):
        self.button = ButtonController(self)
        self.camera = CameraControllerDummy(self)
        self.creator = CollageCreator(self)

        #self.camera.initCamera()
        self.button.start()

    def buttonPressed(self):
        Logger.debug("Controller.buttonPressed()")
        self.button.lightsOff()
        self.app.buttonPressed()
        time.sleep(3)
        photos = self.camera.shoot()
        collage = self.creator.collage(photos)
        self.app.showImage(collage)
        time.sleep(10)
        self.app.showLoopVideo()


