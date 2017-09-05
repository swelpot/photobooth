from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.logger import Logger


class ButtonPressedScreen(Screen):
    video_buttonpressed = ObjectProperty()

    def init_video(self, video_files):
        Logger.debug("ButtonPressedScreen.init_video()")
        self.video_buttonpressed.source = video_files

    def play(self):
        Logger.debug("ButtonPressedScreen.play()")
        self.video_buttonpressed.position = 0
        self.video_buttonpressed.state = 'play'

    def stop(self):
        Logger.debug("ButtonPressedScreen.stop()")
        self.video_buttonpressed.state = 'pause'
