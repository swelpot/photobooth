import glob
import logging
from threading import Thread
import time
import os

read_frequency = 1

class LogReader(Thread):
    active = True

    def __init__(self, logpath, log_consumer):
        super(LogReader, self).__init__()
        self.daemon = True
        self.logpath = logpath
        self.log_consumer = log_consumer

        list_of_files = glob.glob(logpath + '/kivy*.txt')
        self.log_file = max(list_of_files, key=os.path.getctime) # latest file in dir
        logging.info("LogReader: using log file {0}".format(self.log_file))

    def run(self):
        fileBytePos = 0

        while True:
            if self.active:
                logging.debug("LogReader: reading log file {0}".format(self.log_file))
                inFile = open(self.log_file, 'r')
                inFile.seek(fileBytePos)

                data = inFile.read()
                if data:
                    self.log_consumer(data)

                fileBytePos = inFile.tell()
                inFile.close()

            time.sleep(read_frequency)