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

        #time.sleep(5)
        self.button_pressed()

    def button_pressed(self):
        Logger.debug("ButtonController.buttonPressed()")
        self.controller.button_pressed()

    def lights_off(self):
        pass

    def lights_on(self):
        pass