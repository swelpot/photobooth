from kivy.logger import Logger
from threading import Thread
import time

import RPi.GPIO as GPIO


PIN_BUTTON = 12
PIN_RELAIS = 16


class ButtonController(Thread):
    def __init__(self, controller):
        super(ButtonController, self).__init__()
        self.daemon = True

        self.controller = controller

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(PIN_RELAIS, GPIO.OUT)

        self.lights_on()

    def run(self):
        while True:
            input_state = GPIO.input(PIN_BUTTON)
            #print "state: {0}".format(input_state)
            if input_state == False:
                self.button_pressed()

            time.sleep(0.2)

    def button_pressed(self):
        Logger.debug("ButtonController.buttonPressed()")
        self.controller.button_pressed()

    def lights_on(self):
        GPIO.output(PIN_RELAIS, GPIO.HIGH)

    def lights_off(self):
        GPIO.output(PIN_RELAIS, GPIO.LOW)

    def lights_countdown(self, duration):
        counter = duration
        while counter >= 0:
            #print "Counter: {0}".format(counter)
            sleeptime = 1.0
            if counter <= 1.0:
                sleeptime = 0.1

            self.lights_off()
            time.sleep(sleeptime / 2)
            self.lights_on()
            time.sleep(sleeptime / 2)

            counter = counter - (sleeptime)

class MyController():
    def button_pressed(self):
        pass
    
if __name__ == '__main__':
    buttonController = ButtonController(MyController())
    buttonController.start()
    buttonController.lights_off()
    time.sleep(2)
    buttonController.lights_on()
    time.sleep(2)
    buttonController.lights_off()
    time.sleep(2)

    time.sleep(60)
