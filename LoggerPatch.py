from kivy.logger  import Logger
import logging
import time


class LoggerPatch():
    
    def __init__(self):
        self.emit_org = None
        
        # we create a formatter object once to avoid
        # inialisation on every log line
        self.oFormatter=logging.Formatter(None)

        # we just need to patch the first Handler
        # as we change the message itself
        oHandler = Logger.handlers[0]
        self.emit_org=oHandler.emit
        oHandler.emit=self.emit


    def emit(self,record):
        # we do not use the formatter by purpose as it runs on failure
        # if the message string contains format characters

        ct = self.oFormatter.converter(record.created)
        t = time.strftime("%Y-%m-%d %H|%M|%S", ct)
        s = "%s.%03d: " % (t, record.msecs)
    
        record.msg= s +record.msg
        self.emit_org(record)


oLoggerPatch=LoggerPatch()
