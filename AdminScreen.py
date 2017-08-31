import logging
import kivy
from kivy.uix.floatlayout import FloatLayout

from util.NetworkUtil import NetworkUtil

kivy.require('1.10.0')

from kivy.config import Config
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition



class ScreenManagement(ScreenManager):
    pass



class AdminScreen(FloatLayout):
    attr_ip = ObjectProperty()
    attr_imgtarget = ObjectProperty()
    attr_camera_status = ObjectProperty()

    def update(self):
        self.attr_ip = NetworkUtil.getIp()

class MainApp(App):
    def build(self):
        #super(MainApp, self).build()
        Logger.debug("MainApp.build()")
        admin = AdminScreen()
        admin.update()

        return admin




if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    logging.root = Logger

    presentation = Builder.load_file("AdminScreen.kv")
    # Window.fullscreen = 'auto'
    mainApp = MainApp()
    #Window.size = (1280, 800)

    mainApp.run()
