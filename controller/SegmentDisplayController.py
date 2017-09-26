from threading import Thread

import time
import datetime

IS_MAC = False
try:
    from Adafruit_LED_Backpack import SevenSegment
except:
    IS_MAC = True


MODE_COUNTDOWN_TRIGGER = 1
MODE_COUNTDOWN_PHOTO = 2
MODE_LOOP = 3

class SegmentDisplayController(Thread):
    _display = None

    _seconds = 10 # initial
    _init_seconds = 3.0 # initial
    _photo_number = 1 # initial

    _counter = 0

    _current_mode = MODE_LOOP

    def __init__(self):
        super(SegmentDisplayController, self).__init__()
        self.daemon = True

        if not IS_MAC:
            # Create display instance on default I2C address (0x70) and bus number.
            self._display = SevenSegment.SevenSegment()

            # Alternatively, create a display with a specific I2C address and/or bus.
            # display = SevenSegment.SevenSegment(address=0x74, busnum=1)

            # Initialize the display. Must be called once before using the display.
            self._display.begin()

    def run(self):
        sleep_time = 0.2
        next_clear = False

        while True:
            if self._current_mode == MODE_COUNTDOWN_TRIGGER:
                self._counter = self._counter + 1
                #sleep_time = 0.25

                if self._init_seconds >= 0:
                    self.show_number(self._seconds, False, next_clear)
                    self._init_seconds = self._init_seconds - sleep_time
                else:
                    self.show_number(self._seconds, False, next_clear)

                    if self._counter > (1.0 / sleep_time) and self._seconds >= 0:
                        self._counter = 0
                        self._seconds = self._seconds - 1

                    if self._seconds < -1:
                        self._current_mode = MODE_COUNTDOWN_PHOTO

            elif self._current_mode == MODE_COUNTDOWN_PHOTO:
                #sleep_time = 0.25
                self.show_number(self._photo_number, False, next_clear)
            else:
                now = datetime.datetime.now()
                hour = now.hour
                minute = now.minute
                second = now.second

                number = hour * 100 + minute
                colon = second % 2

                self.show_number(number, colon, False)

            # do loop
            next_clear = not next_clear
            time.sleep(sleep_time)

    def run_countdown_trigger(self, seconds, init_seconds, trigger_count):
        self._seconds = seconds
        self._init_seconds = float(init_seconds)
        self._photo_number = trigger_count
        self._counter = 0

        self._current_mode = MODE_COUNTDOWN_TRIGGER

    def run_countdown_photo(self, photo_number):
        self._photo_number = photo_number

        self._current_mode = MODE_COUNTDOWN_PHOTO

    def run_loop(self):
        self._current_mode = MODE_LOOP

    def show_number(self, number, colon, clear_display):
        if self._display:
            # Clear the display buffer.
            self._display.clear()

            if not clear_display:
                # Print a floating point number to the display.
                self._display.print_float(number, decimal_digits=0)
                # Set the colon on or off (True/False).
                self._display.set_colon(colon)

            # Write the display buffer to the hardware.  This must be called to
            # update the actual display LEDs.
            self._display.write_display()
        else:
            now = datetime.datetime.now()

            if not clear_display:
                    print str(now) + " " + str(number) + (":" if colon else "")
            else:
                print str(now) + " clear"

if __name__ == '__main__':

    d = SegmentDisplayController()
    d.start()

    time.sleep(10)
    d.run_countdown_trigger(10, 3, 4)
    time.sleep(15)
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
    d.show_number(1, False, True)
