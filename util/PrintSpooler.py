from Queue import Queue
from threading import Thread

import time

from util.Printer import Printer


class PrintSpooler():
    print_thread = None

    def __init__(self):
        self.print_thread = PrintThread()
        self.print_thread.start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def print_image_async(self, cups_name, image_path, prints):
        task = (cups_name, image_path)
        for a in xrange(1, prints):
            self.print_thread.put(task)

class PrintThread(Thread):
    sleep_time = 1
    _tasks = Queue()

    def __init__(self):
        super(PrintThread, self).__init__()
        #self.daemon = True

    def put(self, task):
        self._tasks.put(task)

    def run(self):
        while True:
            if self._tasks.empty():
                time.sleep(self.sleep_time)
                continue

            task = self._tasks.get(False)

            if task:
                Printer.print_image(task[0], task[1])

if __name__ == '__main__':
    with PrintSpooler() as pd:
        pd.print_image_async("Canon_SELPHY_CP1300", "../../IMG_8049.JPEG", 2)
