from util.OSCommand import OSCommand


class ImageMagickOSCommand(OSCommand):
    def __init__(self, cmd_templatename, imagemagick_path):
        super(ImageMagickOSCommand, self).__init__(cmd_templatename)

        self.imagemagick_path = imagemagick_path

    def replace_keywords(self, text, keywords):
        keywords['imagemagick_path'] = self.imagemagick_path

        return super(ImageMagickOSCommand, self).replace_keywords(text, keywords)


if __name__ == '__main__':
    cmd = ImageMagickOSCommand('/usr/local/Cellar/imagemagick@6/6.9.9-10/bin/')
    cmd.execute('montage_2x2',
                #'montage_2x4_polaroid',
                result='/Users/stefan/Downloads/montage/pol2.jpg',
                photo1="/Users/stefan/Downloads/IMG_9369.JPG",
                photo2="/Users/stefan/Downloads/IMG_9417.JPG",
                photo3="/Users/stefan/Downloads/IMG_9715.JPG",
                photo4="/Users/stefan/Downloads/IMG_9916.JPG"
                )