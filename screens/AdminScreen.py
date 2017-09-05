import os
from Queue import Queue

from util.LogReader import LogReader
from util.NetworkUtil import NetworkUtil

from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, Clock

class AdminScreen(Screen):
    attr_ip = StringProperty()
    attr_imgtarget = StringProperty()
    attr_camera_status = StringProperty()
    attr_text_log = StringProperty()
    obj_scroll_view = ObjectProperty()

    new_log_store = Queue()

    def __init__(self, controller):
        super(AdminScreen, self).__init__()

        self.controller = controller

        self.log_read = LogReader('/Users/stefan/.kivy/logs', self)
        self.log_read.start()

        Clock.schedule_interval(self._update_log, .5)

    def update(self):
        self.attr_ip = NetworkUtil.getIp()

    def switch_mode(self, type):
        Logger.debug("Selected " + type)
        self.controller.switch_mode(type)

    def shutdown(self):
        os.system('sudo shutdown -h now')

    def reboot(self):
        os.system('sudo shutdown -r now')

    def _update_log(self, *args):
        message = ''
        while not self.new_log_store.empty():
            message = message + self.new_log_store.get(False)

        if message:
            self.attr_text_log = self.attr_text_log + message

    def add_log(self, log_text):
        self.new_log_store.put(log_text)

    def stop_log_read(self):
        self.log_read.active = False

    def start_log_read(self):
        self.log_read.active = True


Builder.load_file("screens/AdminScreen.kv")
