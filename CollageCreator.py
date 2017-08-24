from kivy.logger import Logger
from wand.image import Image

class CollageCreator():
    def __init__(self, controller):
        self.controller = controller

    def collage(self, photos):
        Logger.debug("CollageCreator.collage() with {0}".format(photos))

        with Image(filename=photos[0]) as img:
            img.sample(1280, 800)
            img.format = 'jpeg'
            img.save(filename='testresize.jpg')
        return '../IMG_5834.jpg' #photos[0]
