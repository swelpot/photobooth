from kivy.logger import Logger
from threading import Thread
import time

class ButtonControllerDummy(Thread):
    def __init__(self, controller):
        super(ButtonControllerDummy, self).__init__()

        self.controller = controller


    def run(self):
        time.sleep(15)
        self.button_pressed()
        time.sleep(30)
        self.button_pressed()

    def button_pressed(self):
        Logger.debug("ButtonController.buttonPressed()")
        self.controller.button_pressed()

    def lights_off(self):
        pass

    def lights_on(self):
        pass
