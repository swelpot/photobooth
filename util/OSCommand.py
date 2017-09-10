import logging
import re
import subprocess

import datetime
from kivy import Config
from kivy.logger import Logger


class OSCommand():
    def execute(self, templatename, **kwargs):

        filename_result = "/Users/stefan/Downloads/montage/pol2.jpg"

        cmd = self._load_template(templatename)
        cmd = self._replace_keywords(cmd, kwargs)
        cmd_args = cmd.split(' ')

        start = datetime.datetime.now()
        subprocess.check_call(cmd_args)
        end = datetime.datetime.now()

        processing_time = end - start
        Logger.debug('Executing command "{0}" took {1}.{2}s'.format(cmd, processing_time.seconds, processing_time.microseconds))
        return filename_result

    def _load_template(self, templatefile):
        filename = 'cmd_templates/{0}.txt'.format(templatefile)

        inFile = open(filename, 'r')
        template = inFile.read()

        # clean up
        template = template.replace('\n', '')
        while template.find('  ') >= 0:
            template = template.replace('  ', ' ')

        return template

    def _replace_keywords(self, text, keywords):
        for key, value in keywords.iteritems():
            text = self._replace_keyword(text, key, value)

        return text

    def _replace_keyword(self, text, key, value):
        regex = '{{{0}}}'.format(key)
        text = text.replace(regex, value)

        return text


if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    logging.root = logging.Logger

    cmd = OSCommand()
    cmd.execute('montage_2x2',
                #'montage_2x4_polaroid',
                result='/Users/stefan/Downloads/montage/pol2.jpg',
                photo1="/Users/stefan/Downloads/IMG_9369.JPG",
                photo2="/Users/stefan/Downloads/IMG_9417.JPG",
                photo3="/Users/stefan/Downloads/IMG_9715.JPG",
                photo4="/Users/stefan/Downloads/IMG_9916.JPG"
                )