from kivy.logger import Logger

class Camera4Controller(object):
    def __init__(self, controller, target_path_org, target_path_resize):
        pass

    def shoot(self):
        Logger.debug("CameraController.shoot()")
        return ["../photos/org/_MG_6161.JPG",
                "../photos/org/_MG_6162.JPG",
                "../photos/org/_MG_6163.JPG",
                "../photos/org/_MG_6164.JPG"]

    def initCamera(self):
        pass