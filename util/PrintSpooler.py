import logging
from Queue import Queue
from threading import Thread

import time

if __name__ == '__main__':
    from Printer import Printer
else:
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
        logging.debug("Adding task {0} for printer {1}".format(task[1], task[0]))
        self._tasks.put(task)

    def run(self):
        while True:
            if self._tasks.empty():
                time.sleep(self.sleep_time)
                continue

            logging.debug("Getting next task, queue size {0}".format(self._tasks.qsize()))
            task = self._tasks.get(False)

            if task:
                logging.debug("Printing task {0} for printer {1}".format(task[1], task[0]))
                Printer.print_image(task[0], task[1])

if __name__ == '__main__':
    with PrintSpooler() as pd:
        pd.print_image_async("Canon_SELPHY_CP1300", "../../IMG_8049.JPEG", 2)
