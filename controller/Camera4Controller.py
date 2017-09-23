import subprocess
import time

import os
from kivy.logger import Logger
import gphoto2 as gp
import logging

from controller.CameraController import CameraController


class Camera4Controller(CameraController):
    def __init__(self, controller, target_path):
        super(Camera4Controller, self).__init__(controller, target_path)


    def shoot(self):
        Logger.debug("CameraController4.shoot()")
        image1 = self._capture_image()
        image2 = self._capture_image()
        image3 = self._capture_image()
        image4 = self._capture_image()
        return [image1, image2, image3, image4]
