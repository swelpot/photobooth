from kivy.logger import Logger

class CameraControllerDummy():
    def __init__(self, controller):
        self.controller = controller

    def shoot(self):
        Logger.debug("CameraController.shoot()")
        return ["../IMG_0142.jpg"]
