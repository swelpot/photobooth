import time
from threading import Thread

import kivy
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.video import Video

kivy.require('1.10.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen


class LoopVideoScreen(Screen):
    video_loop = ObjectProperty()

    def build(self):
        self.video_loop.bind(state=self.replay)

    def replay(self, instance, value):
        print "fired by {0} with {1}".format(instance, value)
        if value != "play":
            #self.vid.play = True
            self.vid.state = "play"

    def stop(self):
        self.video_loop.state = 'stop'

    def play(self):
        self.video_loop.position = 0
        self.video_loop.state = 'play'


class ShowImageScreen(Screen):
    pass

class ButtonPressedScreen(Screen):
    video_buttonpressed = ObjectProperty()

    # def __init__(self, **kwargs):
    #     super(ButtonPressedScreen, self).__init__(**kwargs)
    # #     self.video_buttonpressed = Video(source='/Users/stefan/PycharmProjects/loopvideo.mp4', play=True, allow_fullscreen=True,
    # #                        options={'fullscreen': True, 'allow_stretch': True})
    # #     #self.video_buttonpressed = Video(source='/Users/stefan/PycharmProjects/buttonpressed.mp4', play=True)
    # #     #self.video_buttonpressed.load()
    #
    # # def build(self):
    # #     img = Image(source='../IMG_0142.jpg')
    #     self.video = Video(source='../buttonpressed.mp4')
    #     self.video.state='pause'
    #     self.video.options = {'eos': 'stop', 'fullscreen': True}
    #     self.video.allow_stretch=True
    #     self.add_widget(self.video)
    # #     return self
    # #     # video_buttonpressed = Video(source='/Users/stefan/PycharmProjects/buttonpressed.mp4')
    # #     # self.add_widget(video_buttonpressed)

    def play(self):
        self.video_buttonpressed.position = 0
        self.video_buttonpressed.state = 'play'

class ScreenManagement(ScreenManager):
    pass




class MainApp(App):
    def __init__(self):
        super(MainApp, self).__init__()
        self.scrButtonPressed = ButtonPressedScreen(name='button_pressed')
        self.scrLoopVideo = LoopVideoScreen()

    def build(self):
        self.sm = ScreenManagement()
        self.sm.add_widget(self.scrLoopVideo)
        self.sm.add_widget(self.scrButtonPressed)
        self.sm.add_widget(ShowImageScreen())

        #self.scrButtonPressed = ButtonPressedScreen(name='button_pressed')

        return self.sm

    def buttonPressed(self):
        self.scrLoopVideo.stop()
        self.scrButtonPressed.play()
        self.sm.current = 'button_pressed'

    def showImage(self): #, imagepath):
        self.sm.current = 'show_image'

    def showLoopVideo(self):
        self.scrLoopVideo.play()
        self.sm.current = 'loop_video'

class Simulator(Thread):
    def __init__(self, app):
        super(Simulator, self).__init__()

        self.app = app

    def run(self):
        time.sleep(15)
        self.app.buttonPressed()
        time.sleep(12)
        self.app.showImage()
        time.sleep(10)
        self.app.showLoopVideo()

presentation = Builder.load_file("main.kv")
#Window.fullscreen = 'auto'
mainApp = MainApp()
simulator = Simulator(mainApp)
simulator.start()

mainApp.run()