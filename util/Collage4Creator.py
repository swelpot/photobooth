import logging
import ntpath
import re
from threading import Thread

from kivy import Config
from kivy.logger import Logger

from util.ImageMagickOSCommand import ImageMagickOSCommand


class Collage4Creator(object):
    conf = None

    def set_conf(self, conf):
        self.conf = conf

    def collage_print_async(self, photos):
        logging.debug("Collage4Creator.collage_print_async() with {0}".format(photos))

        worker = self._get_worker(photos, 'print')
        worker.start()

        return worker.filepath

    # create collage for screen display
    def collage_screen(self, photos):
        logging.debug("Collage4Creator.collage_screen() with {0}".format(photos))

        collage_filename = self._get_collage_filename(photos, 'screen')
        collage_path = self.conf.get("photo.path_target") + self.conf.get("photo.path_collage")
        filepath = collage_path + collage_filename
        logging.debug("result filename {0}".format(filepath))

        imagemagick_path = self.conf.get('app.imagemagick_path')
        cmd_template = self.conf.get("collage.cmd_template_" + 'screen')

        os_cmd = ImageMagickOSCommand(cmd_template, imagemagick_path)

        filename1 = photos[0]
        filename2 = photos[1]
        filename3 = photos[2]
        filename4 = photos[3]

        os_cmd.execute(result = filepath,
                       photo1 = filename1,
                       photo2 = filename2,
                       photo3 = filename3,
                       photo4 = filename4)

        logging.info('Created collage {0}'.format(filepath))

        return filepath

    def _get_worker(self, photos, template_type):
        collage_filename = self._get_collage_filename(photos, template_type)
        collage_path = self.conf.get("photo.path_target") + self.conf.get("photo.path_collage")
        filepath = collage_path + collage_filename
        logging.debug("result filename {0}".format(filepath))

        imagemagick_path = self.conf.get('app.imagemagick_path')
        cmd_template = self.conf.get("collage.cmd_template_" + template_type)

        os_cmd = ImageMagickOSCommand(cmd_template, imagemagick_path)

        worker = WorkerThread(os_cmd, filepath, photos)

        return worker

    def _get_img_nb(self, filename):
        regex = self.conf.get("photo.img_nb_regex")

        img_nb = ntpath.basename(filename)
        img_nb_search = re.search(regex, filename, re.IGNORECASE)

        if img_nb_search:
            img_nb = img_nb_search.group(1)
        else:
            logging.warn('Could not extract image number from file {0}'.format(filename))

        return img_nb

    def _get_collage_filename(self, photos, template_type):
        collage_filename = 'IMG'

        for filename in photos:
            img_nb = self._get_img_nb(filename)
            collage_filename = '{0}_{1}'.format(collage_filename, img_nb)

        collage_filename = '{0}_{1}.JPG'.format(collage_filename, template_type)

        return collage_filename

class WorkerThread(Thread):
    def __init__(self, cmd, filepath, photos):
        super(WorkerThread, self).__init__()
        self.daemon = True

        self.cmd = cmd
        self.filepath = filepath
        self.photos = photos

    def run(self):
        filename1 = self.photos[0]
        filename2 = self.photos[1]
        filename3 = self.photos[2]
        filename4 = self.photos[3]

        self.cmd.execute(result = self.filepath,
                       photo1 = filename1,
                       photo2 = filename2,
                       photo3 = filename3,
                       photo4 = filename4)

        logging.info('Created collage {0}'.format(self.filepath))


if __name__ == '__main__':
    Config.set("kivy", "log_level", "debug")
    logging.root = Logger

    conf = {'photo.path_target': '/Users/stefan/Downloads/',
            'photo.path_collage': 'montage/',
            'photo.img_nb_regex': '[_I]MG_(\d\d\d\d).JPG',
            "collage.cmd_template_screen": "montage_2x2",
            "collage.cmd_template_print": "montage_2x4",
            "app.imagemagick_path": "/usr/local/Cellar/imagemagick@6/6.9.9-10/bin/"}

    creator = Collage4Creator()
    creator.set_conf(conf)
    creator.collage_print_async(["/Users/stefan/Downloads/montage/IMG_2495.JPG",
                     "/Users/stefan/Downloads/montage/IMG_2537.JPG",
                     "/Users/stefan/Downloads/montage/_MG_2686.JPG",
                     "/Users/stefan/Downloads/montage/IMG_2764.JPG"])
