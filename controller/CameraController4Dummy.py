from kivy.logger import Logger

class CameraController4Dummy():
    def shoot(self):
        Logger.debug("CameraController.shoot()")
        return ["../photos/org/IMG_5864.JPG",
                "../photos/org/IMG_5864.JPG",
                "../photos/org/IMG_5864.JPG",
                "../photos/org/IMG_5864.JPG"]

    def initCamera(self):
        pass