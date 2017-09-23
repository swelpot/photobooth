from kivy.logger import Logger

class Camera4Controller(object):
    def shoot(self):
        Logger.debug("CameraController.shoot()")
        return ["../photos/org/_MG_6161.JPG",
                "../photos/org/_MG_6162.JPG",
                "../photos/org/_MG_6163.JPG",
                "../photos/org/_MG_6164.JPG"]

    def initCamera(self):
        pass