
import kivy
from kivy import Config
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('1.10.0')

from kivy.app import App

class ShowImageScreen(Screen):
    image_path = ObjectProperty()

    def set_image(self, image):
        self.image_path.source = image #"../IMG_0142.jpg"

# Create the screen manager
sm = ScreenManager()
sm.add_widget(ShowImageScreen())

class MainApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    presentation = Builder.load_file("ImageTest.kv")
    mainApp = MainApp()
    mainApp.run()
