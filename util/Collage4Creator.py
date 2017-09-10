import logging
import ntpath
import re

from kivy import Config
from kivy.logger import Logger

class Collage4Creator():
    def __init__(self, path, regex):
        self.path = path
        self.regex = regex

    # create collage for screen display
    def collage_screen(self, photos):
        Logger.debug("CollageCreator.collage() with {0}".format(photos))

        filename1 = photos[0]
        filename2 = photos[1]
        filename3 = photos[2]
        filename4 = photos[3]

        collage_filename = self._get_collage_filename(photos)

        Logger.info('Created collage {0}'.format(collage_filename))
        return collage_filename

    def _get_img_nb(self, filename):
        img_nb = ntpath.basename(filename)
        img_nb_search = re.search(self.regex, filename, re.IGNORECASE)

        if img_nb_search:
            img_nb = img_nb_search.group(1)
        else:
            Logger.warn('Could not extract image number from file {0}'.format(filename))

        return img_nb

    def _get_collage_filename(self, photos):
        collage_filename = 'IMG'

        for filename in photos:
            img_nb = self._get_img_nb(filename)
            collage_filename = '{0}_{1}'.format(collage_filename, img_nb)

        collage_filename = '{0}.JPG'.format(collage_filename)

        return collage_filename


if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    logging.root = Logger

    creator = Collage4Creator('/Users/stefan/Downloads/', 'IMG_(\d\d\d\d).JPG')
    creator.collage_screen(["/Users/stefan/Downloads/IMG_9369.JPG",
                     "/Users/stefan/Downloads/IMG_9417.JPG",
                     "/Users/stefan/Downloads/IMG_9715.JPG",
                     "/Users/stefan/Downloads/IMG_9916.JPG"])
