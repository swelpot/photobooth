from threading import Thread
import time

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, Clock
from kivy.uix.screenmanager import ScreenManager, Screen

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<MenuScreen>:
    name: 'show_image'
    image_path: imagetag

    BoxLayout:
        Button:
            text: 'Goto settings'
            #on_press: root.set_image('../IMG_0142.JPG')
        AsyncImage:
            id: imagetag
            source: '../IMG_5859.JPG'

""")

# Declare both screens
class MenuScreen(Screen):
    image_path = ObjectProperty()

    def __init__(self):
        super(MenuScreen, self).__init__()
        self.img = ''
        self.updated = False

    def set_image(self, image):
        print 'set_image'
        self.img = image
        self.updated = True
        Clock.schedule_once(self.inner_set_image, 1)

    def inner_set_image(self, *args):
        print 'inner_set_image'
        if self.updated:
            print 'inner_set_image updated'
            self.image_path.source = self.img
            self.updated = False

# Create the screen manager
sm = ScreenManager()
menuscreen = MenuScreen()
sm.add_widget(menuscreen)

class TestApp(App):
    def build(self):
        return sm

class MyTh(Thread):
    def __init__(self, app):
        super(MyTh, self).__init__()
        self.app = app

    def run(self):
        time.sleep(10)
        self.app.set_image('../IMG_0142.JPG')


if __name__ == '__main__':
    th = MyTh(menuscreen)
    #th.start()
    TestApp().run()