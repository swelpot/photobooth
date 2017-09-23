from threading import Thread

import datetime
from kivy.logger import Logger
from wand.image import Image
import ntpath

class ImageResize(object):
    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height

    def resize(self, file):
        Logger.debug("ImageResize.resize() with {0}".format(file))
        target = self.path + ntpath.basename(file)

        w = Worker(file, target, self.width, self.height)
        w.run()

        return target

    def resize_async(self, file):
        Logger.debug("ImageResize.resize_async() with {0}".format(file))
        target = self.path + ntpath.basename(file)

        w = Worker(file, target, self.width, self.height)
        w.start()

        return target


class Worker(Thread):
    def __init__(self, file, target, width, height):
        super(Worker, self).__init__()
        self.daemon = True

        self.file = file
        self.target = target
        self.width = width
        self.height = height

    def run(self):
        start = datetime.datetime.now()

        with Image(filename = self.file) as img:
            img.sample(self.width, self.height)
            img.format = 'jpeg'
            img.save(filename = self.target)

        end = datetime.datetime.now()
        processing_time = end - start
        Logger.info("Resized image to {0}x{1}, filename {2}, took {3}.{4}s".format(self.width, self.height, self.target, processing_time.seconds, processing_time.microseconds))
