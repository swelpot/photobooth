from kivy.logger import Logger

class CollageCreator():
    def collage(self, photos):
        Logger.debug("CollageCreator.collage() with {0}".format(photos))

        filename = photos[0]

        return filename
