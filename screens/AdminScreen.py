import os
from Queue import Queue

import sys

from util.LogReader import LogReader
from util.NetworkUtil import NetworkUtil
from os.path import expanduser

from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, Clock

from util.PhotoStore import PhotoStore
from util.Printer import Printer


class AdminScreen(Screen):
    attr_ip = StringProperty()
    attr_imgtarget = StringProperty()
    attr_camera_status = StringProperty()
    attr_printer_status = StringProperty()
    attr_text_log = StringProperty()
    attr_photocnt = StringProperty()
    attr_printcnt = StringProperty()
    obj_scroll_view = ObjectProperty()

    new_log_store = Queue()

    def __init__(self, controller):
        super(AdminScreen, self).__init__()

        self.controller = controller

        home_dir = expanduser("~")
        self.log_read = LogReader(home_dir + '/.kivy/logs', self.add_log)
        self.log_read.start()

        Clock.schedule_interval(self._update_log, .5)

    def update(self):
        self.attr_ip = NetworkUtil.getIp()

        self.attr_printer_status = "Ready" if Printer.is_connected(self.controller.conf.get("printer.cups_name")) else "Missing"

        with PhotoStore() as ps:
            self.attr_printcnt = str(ps.get_print_count(self.controller.conf.get("project_name")))
            self.attr_photocnt = str(ps.get_photo_count(self.controller.conf.get("project_name")))

    def switch_mode(self, type):
        Logger.debug("Selected " + type)
        self.controller.switch_mode(type)

    def shutdown(self):
        os.system('sudo shutdown -h now')

    def reboot(self):
        os.system('sudo shutdown -r now')

    def exit_console(self):
        sys.exit()

    def reset_printcnt(self):
        with PhotoStore() as ps:
            ps.reset_printcnt(self.controller.conf.get("project_name"))
            self.attr_printcnt = '0'

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
