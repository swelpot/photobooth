from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger

class ShowImageScreen(Screen):
    image_path = ObjectProperty()

    def set_image(self, image):
        Logger.debug("ShowImageScreen.set_image() with {0}".format(image))
        self.image_path.source = image #"../IMG_0142.jpg"
