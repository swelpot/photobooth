from kivy.logger import Logger
from threading import Thread
import time


class ButtonController(Thread):
    def __init__(self, controller):
        super(ButtonController, self).__init__()

        self.controller = controller

    def run(self):
        #while True:
            # wait for Button pressed

        time.sleep(25)
        self.buttonPressed()

    def buttonPressed(self):
        Logger.debug("ButtonController.buttonPressed()")
        self.controller.buttonPressed()

    def lightsOff(self):
        pass

    def lightsOn(self):
        pass