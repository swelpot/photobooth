import time

import RPi.GPIO as GPIO

PIN_3V = 20
PIN_RELAIS = 16

class ButtonLight(object):
    def __init__(self):
        super(ButtonLight, self).__init__()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_3V, GPIO.OUT)
        GPIO.output(PIN_3V, GPIO.HIGH)

        GPIO.setup(PIN_RELAIS, GPIO.OUT)

    def lights_off(self):
        GPIO.output(PIN_RELAIS, GPIO.HIGH)

    def lights_on(self):
        GPIO.output(PIN_RELAIS, GPIO.LOW)
    
if __name__ == '__main__':
    bl = ButtonLight()
    time.sleep(2)

    while True:
        bl.lights_off()
        time.sleep(1)
        bl.lights_on()
        time.sleep(1)
