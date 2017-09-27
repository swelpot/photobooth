import logging
from threading import Thread

import time
import datetime

IS_RPI = True
try:
    from Adafruit_LED_Backpack import SevenSegment
except:
    IS_RPI = False

MODE_COUNTDOWN_TRIGGER = 1
MODE_COUNTDOWN_PHOTO = 2
MODE_LOOP = 3

MULTIPLIER_MICRO = 1000000.0


class SegmentDisplayController(Thread):
    _display = None

    _seconds = 10  # initial
    _init_seconds = 3.0  # initial
    _photo_number = 1  # initial

    _current_mode = MODE_LOOP
    _start_time = datetime.datetime.now()

    def __init__(self):
        super(SegmentDisplayController, self).__init__()
        self.daemon = True

        if IS_RPI:
            # Create display instance on default I2C address (0x70) and bus number.
            self._display = SevenSegment.SevenSegment()

            # Alternatively, create a display with a specific I2C address and/or bus.
            # display = SevenSegment.SevenSegment(address=0x74, busnum=1)

            # Initialize the display. Must be called once before using the display.
            try:
                self._display.begin()
            except:
                logging.error("No 7-Segment-Display found. Proceeding without display!")
                self._display = None

    def run(self):
        sleep_time = 0.05
        frequency = 2  # per second, default

        digits = [None] * 4
        colon = False  # show colon
        visible = True  # number is visible

        while True:
            now = datetime.datetime.now()
            diff = (now - self._start_time).microseconds
            div = 1.0 / frequency * MULTIPLIER_MICRO
            rest = diff % div
            visible = False if rest > 0 and rest < (sleep_time * MULTIPLIER_MICRO) else True

            # print "Now {0}, Start {1}, diff {2}, div {3}, rest {4}, io {5}".format(now, self._start_time, diff, div, rest, io)

            if self._current_mode == MODE_COUNTDOWN_TRIGGER:
                frequency = 2  # per second
                number = int(self._seconds + self._init_seconds - (now - self._start_time).seconds)
                if number < 0:
                    number = 0
                elif number > self._seconds:
                    number = self._seconds

                digits = self._convert(number)
                colon = False

                if number == 1:
                    # fast blink last second
                    frequency = 5
                elif number == 0:
                    frequency = 10

            elif self._current_mode == MODE_COUNTDOWN_PHOTO:
                frequency = 2
                digits = self._convert(self._photo_number)
                colon = False

            else:
                frequency = 2

                hour = now.hour
                minute = now.minute
                second = now.second

                number = hour * 100 + minute
                digits = self._convert(number)
                colon = second % 2
                visible = True

            self.show_number(digits, colon, visible)

            time.sleep(sleep_time)

    def _convert(self, number):
        #print "number: " + str(number)
        digit1 = number / 1000
        digit2 = (number - digit1 * 1000) / 100
        digit3 = (number - digit1 * 1000 - digit2 * 100) / 10
        digit4 = number - digit1 * 1000 - digit2 * 100 - digit3 * 10

        if digit1 == 0:
            digit1 = None

            if digit2 == 0:
                digit2 = None

                if digit3 == 0: digit3 = None
        #if digit4 == 0: digit4 = None

        return [digit1, digit2, digit3, digit4]

    _current_digits = [None] * 4
    _current_colon = False
    _current_visible = True

    def show_number(self, digits, colon, visible):

        if self._current_digits == digits and self._current_colon == colon and self._current_visible == visible:
            return

        self._current_digits = digits
        self._current_colon = colon
        self._current_visible = visible

        if self._display:
            # Clear the display buffer.
            self._display.clear()

            if visible:
                self._display.set_digit(0, digits[0])
                self._display.set_digit(1, digits[1])
                self._display.set_digit(2, digits[2])
                self._display.set_digit(3, digits[3])

                # Set the colon on or off (True/False).
                self._display.set_colon(colon)

            # Write the display buffer to the hardware.  This must be called to
            # update the actual display LEDs.
            self._display.write_display()
        elif not IS_RPI:
            now = datetime.datetime.now()

            if visible:
                print str(now) + " " + str(digits[0]) + "," + str(digits[1]) + "," + (":" if colon else "") + str(digits[2]) + "," + str(
                    digits[3])
            else:
                print str(now)


    def run_countdown_trigger(self, seconds, init_seconds):
        self._start_time = datetime.datetime.now()
        self._seconds = seconds
        self._init_seconds = init_seconds
        self._current_mode = MODE_COUNTDOWN_TRIGGER


    def run_countdown_photo(self, photo_number):
        self._start_time = datetime.datetime.now()
        self._photo_number = photo_number
        self._current_mode = MODE_COUNTDOWN_PHOTO


if __name__ == '__main__':
    d = SegmentDisplayController()
    d.start()

    time.sleep(10)
    seconds = 10
    d.run_countdown_trigger(seconds, 1)
    time.sleep(seconds + 3)
    d.run_countdown_photo(4)
    time.sleep(2)
    d.run_countdown_photo(3)
    time.sleep(2)
    d.run_countdown_photo(2)
    time.sleep(2)
    d.run_countdown_photo(1)
    time.sleep(2)
    d.run_countdown_photo(0)
    time.sleep(2)
