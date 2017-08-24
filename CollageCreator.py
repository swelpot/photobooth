from kivy.logger import Logger
#from wand.image import Image

class CollageCreator():
    def __init__(self, controller):
        self.controller = controller

    def collage(self, photos):
        Logger.debug("CollageCreator.collage() with {0}".format(photos))

        # with Image(filename=photos[0]) as img:
        #      img.sample(1280, 800)
        #      img.format = 'jpeg'
        #      img.save(filename='testresize.jpg')
        return photos[0]
        #return '../photos/IMG_5834.JPG' #photos[0]
        #return '../IMG_5834.JPG'
        #return '../IMG_0142.jpg'