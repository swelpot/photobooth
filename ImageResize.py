from kivy.logger import Logger
from wand.image import Image
import ntpath

class ImageResize():
    def __init__(self, path, width, height):
        self.path = path
        self.width = width
        self.height = height

    def resize(self, file):
        Logger.debug("ImageResize.resize() with {0}".format(file))

        #withoutSuffix = file.split(".")[0]
        target = self.path + ntpath.basename(file)

        with Image(filename = file) as img:
            img.sample(self.width, self.heigt)
            img.format = 'jpeg'
            img.save(filename = target)

        Logger.info("Resized image to {0}x{1}, filename {2}".format(self.width, self.height, target))
        return target

