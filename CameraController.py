import os
from kivy.logger import Logger
import gphoto2 as gp
import logging

class CameraController():
    def __init__(self, controller):
        self.controller = controller

        gp.use_python_logging(mapping={
            gp.GP_LOG_ERROR: logging.INFO,
            gp.GP_LOG_VERBOSE: logging.DEBUG,
            gp.GP_LOG_DEBUG: logging.DEBUG - 3,
            gp.GP_LOG_DATA: logging.DEBUG - 6})

    def initCamera(self):
        self.context = gp.gp_context_new()
        error, self.camera = gp.gp_camera_new()
        error = gp.gp_camera_init(self.camera, self.context)
        if error >= gp.GP_OK:
            # operation completed successfully so exit loop
            return
        if error != gp.GP_ERROR_MODEL_NOT_FOUND:
            # some other error we can't handle here
            raise gp.GPhoto2Error(error)

    def shoot(self):
        Logger.debug("CameraController.shoot()")
        return ["../IMG_0142.jpg"]

    def shootNew(self):
        print('Capturing image')
        file_path = gp.check_result(gp.gp_camera_capture(
            self.camera, gp.GP_CAPTURE_IMAGE, self.context))
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join('/tmp', file_path.name)
        print('Copying image to', target)
        camera_file = gp.check_result(gp.gp_camera_file_get(
            self.camera, file_path.folder, file_path.name,
            gp.GP_FILE_TYPE_NORMAL, self.context))
        gp.check_result(gp.gp_file_save(camera_file, target))
        error = gp.gp_camera_exit(self.camera, self.context)
