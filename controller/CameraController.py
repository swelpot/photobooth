import subprocess
import time

import os
from kivy.logger import Logger
import gphoto2 as gp
import logging

from util.ImageResize import ImageResize


class CameraController(object):
    def __init__(self, controller, target_path_org, target_path_resize):
        self.controller = controller
        self.target_path_org = target_path_org
        self.target_path_resize = target_path_resize

        gp.use_python_logging(mapping={
            gp.GP_LOG_ERROR: logging.INFO,
            gp.GP_LOG_VERBOSE: logging.DEBUG,
            gp.GP_LOG_DEBUG: logging.DEBUG - 3,
            gp.GP_LOG_DATA: logging.DEBUG - 6})

    def initCamera(self):
#        img = subprocess.check_output(['gphoto2', '--set-config capturetarget=1'])
#        Logger.info('Config: {0}'.format(img))

        self.context = gp.gp_context_new()
        error, self.camera = gp.gp_camera_new()
        error = gp.gp_camera_init(self.camera, self.context)

        self._set_capture_target()

        if error >= gp.GP_OK:
            # operation completed successfully so exit loop
            return
        if error != gp.GP_ERROR_MODEL_NOT_FOUND:
            # some other error we can't handle here
            raise gp.GPhoto2Error(error)

    def _set_capture_target(self):
        value = 1

        # get configuration tree
        config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))
        # find the capture target config item
        capture_target = gp.check_result(
            gp.gp_widget_get_child_by_name(config, 'capturetarget'))
        # check value in range
        #count = gp.check_result(gp.gp_widget_count_choices(capture_target))

        #if value < 0 or value >= count:
        #    print('Parameter out of range')

        #return 1
        # set value
        value = gp.check_result(gp.gp_widget_get_choice(capture_target, value))
        gp.check_result(gp.gp_widget_set_value(capture_target, value))
        # set config
        gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))
        # clean up
        #gp.check_result(gp.gp_camera_exit(camera, context))

    def shoot(self):
        Logger.debug("CameraController.shoot()")
        image1 = self._capture_image()
        return [image1]

    def _capture_image(self):
        # img = subprocess.check_output(['gphoto2', '--capture-image-and-download'])
        # Logger.info('Image: {0}'.format(img))
        # return img
        Logger.info('Capturing image')
        file_path = gp.check_result(gp.gp_camera_capture(
            self.camera, gp.GP_CAPTURE_IMAGE, self.context))

        Logger.debug('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target_rel = os.path.join(self.target_path_org, file_path.name)
        target_abs = os.path.abspath(target_rel)
        Logger.debug('Copying image to {0}'.format(target_abs))

        camera_file = gp.check_result(gp.gp_camera_file_get(
            self.camera, file_path.folder, file_path.name,
            gp.GP_FILE_TYPE_NORMAL, self.context))
        gp.check_result(gp.gp_file_save(camera_file, str(target_abs)))

        #gp.gp_file_free(camera_file)

        #error = gp.gp_camera_exit(self.camera, self.context)
        #time.sleep(2)

        ir = ImageResize(self.target_path_resize, 900, 600)
        filename = ir.resize_async(str(target_abs))

        return filename
