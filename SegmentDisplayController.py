from threading import Thread

import time
from kivy.logger import Logger


class SegmentDisplayController(Thread):
    def __init__(self, controller, from_number):
        super(SegmentDisplayController, self).__init__()
        self.controller = controller
        self.from_number = from_number

    def run(self):
        i = self.from_number
        while i <= 0:
            self.showNumber(i)
            i = i - 1
            time.sleep(1)

    def showNumber(self, number):
        pass
