import glob
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

    def run(self):
        fileBytePos = 0

        while True:
            if self.active:
                inFile = open(self.log_file, 'r')
                inFile.seek(fileBytePos)

                data = inFile.read()
                if data:
                    self.log_consumer.add_log(data)

                fileBytePos = inFile.tell()
                inFile.close()

            time.sleep(read_frequency)