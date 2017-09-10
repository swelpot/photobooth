import logging
import ntpath
import re

from kivy import Config
from kivy.logger import Logger

from util.ImageMagickOSCommand import ImageMagickOSCommand


class Collage4Creator():
    conf = None

    def set_conf(self, conf):
        self.conf = conf

    def collage_print_async(self, photos):
        pass

    # create collage for screen display
    def collage_screen(self, photos):
        Logger.debug("CollageCreator.collage_screen() with {0}".format(photos))

        filename1 = photos[0]
        filename2 = photos[1]
        filename3 = photos[2]
        filename4 = photos[3]

        collage_filename = self._get_collage_filename(photos)
        collage_path = self.conf.get("photo.path_target") + self.conf.get("photo.path_collage")

        filepath = collage_path + collage_filename

        cmd_template = self.conf.get("collage.cmd_template_screen")

        os_cmd = ImageMagickOSCommand(self.conf.get('app.imagemagick_path'))
        os_cmd.execute(cmd_template, result = filepath,
                       photo1 = filename1,
                       photo2 = filename2,
                       photo3 = filename3,
                       photo4 = filename4)



        Logger.info('Created collage {0}'.format(collage_filename))
        return filepath

    def _get_img_nb(self, filename):
        regex = self.conf.get("photo.img_nb_regex")

        img_nb = ntpath.basename(filename)
        img_nb_search = re.search(regex, filename, re.IGNORECASE)

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

    conf = {'photo.path_target': '/Users/stefan/Downloads/',
            'photo.path_collage': 'montage/',
            'photo.img_nb_regex': 'IMG_(\d\d\d\d).JPG',
            "collage.cmd_template_screen": "montage_2x2",
            "app.imagemagick_path": "/usr/local/Cellar/imagemagick@6/6.9.9-10/bin/"}

    creator = Collage4Creator()
    creator.set_conf(conf)
    creator.collage_screen(["/Users/stefan/Downloads/IMG_9369.JPG",
                     "/Users/stefan/Downloads/IMG_9417.JPG",
                     "/Users/stefan/Downloads/IMG_9715.JPG",
                     "/Users/stefan/Downloads/IMG_9916.JPG"])
