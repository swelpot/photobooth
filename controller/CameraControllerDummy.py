import time
from kivy.logger import Logger

class CameraControllerDummy(object):
    def shoot(self, capture_callback):
        Logger.debug("CameraController.shoot()")
        time.sleep(1)
        capture_callback(0)
        return ["../photos/org/IMG_5864.JPG"]

    def initCamera(self):
        pass