import time
from kivy.logger import Logger

class Camera4Controller(object):
    def __init__(self, controller, target_path_org, target_path_resize, rotate):
        pass

    def shoot(self, capture_callback):
        Logger.debug("Camera4ControllerDummy.shoot()")

        time.sleep(1)
        capture_callback(3)
        time.sleep(1)
        capture_callback(2)
        time.sleep(1)
        capture_callback(1)
        time.sleep(1)
        capture_callback(0)

        return ["../photos/resized/_MG_6161.JPG",
                "../photos/resized/_MG_6162.JPG",
                "../photos/resized/_MG_6163.JPG",
                "../photos/resized/_MG_6164.JPG"]

    def initCamera(self):
        pass