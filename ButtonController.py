from kivy.logger import Logger
from threading import Thread
import RPi.GPIO as GPIO
import time

gpioPin = 18

class ButtonController(Thread):
    def __init__(self, controller):
        super(ButtonController, self).__init__()
        self.daemon = True

        self.controller = controller

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


    def run(self):
        while True:
            input_state = GPIO.input(gpioPin)
            if input_state == False:
                self.button_pressed()
                time.sleep(0.2)
        
        #time.sleep(5)
        #self.button_pressed()
        #time.sleep(30)
        #self.button_pressed()

    def button_pressed(self):
        Logger.debug("ButtonController.buttonPressed()")
        self.controller.button_pressed()

    def lights_off(self):
        pass

    def lights_on(self):
        pass

class MyController():
    def button_pressed(self):
        pass
    
if __name__ == '__main__':
    buttonController = ButtonController(MyController())
    buttonController.start()
    time.sleep(60)
