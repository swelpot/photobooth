from kivy.logger import Logger


class CollageCreator():
    def __init__(self, controller):
        self.controller = controller

    def collage(self, photos):
        Logger.debug("CollageCreator.collage() with {0}".format(photos))
        return "../IMG_0142.jpg"
