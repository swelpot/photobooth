import time

import RPi.GPIO as GPIO

PIN_RELAIS = 16

class ButtonLight(object):
    def __init__(self):
        super(ButtonLight, self).__init__()

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(PIN_RELAIS, GPIO.OUT)

    def lights_off(self):
        GPIO.output(PIN_RELAIS, GPIO.HIGH)

    def lights_on(self):
        GPIO.output(PIN_RELAIS, GPIO.LOW)

if __name__ == '__main__':
    bl = ButtonLight()

    counter = 10.0
    while counter >= 0:
        print "Counter: {0}".format(counter)
        sleeptime = 1.0
        if counter <= 1.0:
            sleeptime = 0.1

        GPIO.output(PIN_RELAIS, GPIO.HIGH)
        time.sleep(sleeptime / 2)
        GPIO.output(PIN_RELAIS, GPIO.LOW)
        time.sleep(sleeptime / 2)

        counter = counter - (sleeptime)