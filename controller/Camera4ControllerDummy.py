from kivy.logger import Logger

class Camera4ControllerDummy(object):
    def shoot(self):
        Logger.debug("CameraController.shoot()")
        return ["../photos/org/IMG_5864.JPG",
                "../photos/org/IMG_5857.JPG",
                "../photos/org/IMG_5864.JPG",
                "../photos/org/IMG_5857.JPG"]

    def initCamera(self):
        pass