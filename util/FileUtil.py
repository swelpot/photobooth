import logging
import os

import time


class FileUtil(object):
    max_wait_time = 10  # seconds

    @staticmethod
    def is_file_ready(file):
        logging.debug("FileUtil.is_file_ready({0})".format(file))
        ''' check if file creation is finished! '''
        sleep_time = 0.5 # seconds

        counter = 0
        file_ready = os.path.isfile(file)
        while counter < (FileUtil.max_wait_time / sleep_time) and not file_ready:
            time.sleep(sleep_time)
            counter = counter + 1

            file_ready = os.path.isfile(file)

        logging.debug("FileUtil.is_file_ready({0}) --> {1}".format(file, file_ready))
        return file_ready
