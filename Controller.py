from kivy.logger import Logger
import time
from ButtonController import ButtonController
from CameraController import CameraController
from CollageCreator import CollageCreator

class Controller():
    def __init__(self, app):
        self.app = app

    def start(self):
        self.button = ButtonController(self)
        self.camera = CameraController(self)
        self.creator = CollageCreator(self)

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


