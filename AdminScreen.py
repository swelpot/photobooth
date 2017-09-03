import glob
import logging
from Queue import Queue
from threading import Thread

import kivy
import time
from kivy.uix.floatlayout import FloatLayout

from util.NetworkUtil import NetworkUtil

kivy.require('1.10.0')

from kivy.config import Config
from kivy.logger import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, Clock
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
import os


class ScreenManagement(ScreenManager):
    pass



class AdminScreen(FloatLayout):
    attr_ip = StringProperty()
    attr_imgtarget = StringProperty()
    attr_camera_status = StringProperty()
    attr_text_log = StringProperty()
    obj_scroll_view = ObjectProperty()

    new_log_store = Queue()

    def __init__(self):
        super(AdminScreen, self).__init__()

        Clock.schedule_interval(self.inner_update_log, .5)

    def update(self):
        self.attr_ip = NetworkUtil.getIp()

    def switch_mode(self, type):
        Logger.info("Test " + type)

    def shutdown(self):
        os.system('sudo shutdown -h now')

    def reboot(self):
        os.system('sudo shutdown -r now')

    def inner_update_log(self, *args):
        message = ''
        while not self.new_log_store.empty():
            message = message + self.new_log_store.get(False)
            #q.task_done()

        if message:
            update_scroll_view = False
            if self.obj_scroll_view.scroll_y == 0:
                update_scroll_view = True

            self.attr_text_log = self.attr_text_log + message

            if update_scroll_view:
                self.obj_scroll_view.scroll_y = 0

    def add_log(self, log_text):
        self.new_log_store.put(log_text)

class LogReader(Thread):
    def __init__(self, logpath, log_consumer):
        super(LogReader, self).__init__()
        self.daemon = True
        self.logpath = logpath
        self.log_consumer = log_consumer

        list_of_files = glob.glob(logpath + '/kivy*.txt')
        self.log_file = max(list_of_files, key=os.path.getctime) # latest file in dir

    def run(self):
        fileBytePos = 0
        while True:
            inFile = open(self.log_file, 'r')
            inFile.seek(fileBytePos)

            data = inFile.read()
            if data:
                self.log_consumer.add_log(data)

            fileBytePos = inFile.tell()
            inFile.close()

            time.sleep(1)

class MainApp(App):
    def build(self):
        #super(MainApp, self).build()
        Logger.debug("MainApp.build()")
        admin = AdminScreen()
        admin.update()

        log_read = LogReader('/Users/stefan/.kivy/logs', admin)
        log_read.start()

        return admin




if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    logging.root = Logger

    presentation = Builder.load_file("AdminScreen.kv")
    # Window.fullscreen = 'auto'
    mainApp = MainApp()
    #Window.size = (1280, 800)

    mainApp.run()
