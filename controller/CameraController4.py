import subprocess
import time

import os
from kivy.logger import Logger
import gphoto2 as gp
import logging

from controller.CameraController import CameraController


class CameraController4(CameraController):
    def __init__(self, controller, target_path):
        super(CameraController4, self).__init__(controller, target_path)


    def shoot(self):
        Logger.debug("CameraController.shoot()")
        image1 = self.capture_image()
        image2 = self.capture_image()
        image3 = self.capture_image()
        image4 = self.capture_image()
        return [image1, image2, image3, image4]
