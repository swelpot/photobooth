import logging
import os
import time
from threading import Thread
from instagramapi.InstagramAPI import InstagramAPI

class InstagramUpload(Thread):
    max_wait = 10
    def __init__(self, username, password, image_path, hashtag):
        super(InstagramUpload, self).__init__()
        self.daemon = False

        self.username = username
        self.password = password
        self.image_path = image_path
        self.hashtag = hashtag

    def run(self):
        wait = 0
        file_is_ok = False

        while wait < self.max_wait and not file_is_ok:
            logging.debug("Waiting for image {0}".format(self.image_path))
            wait = wait + 1
            time.sleep(1)

            file_is_ok = (os.path.isfile(self.image_path) and os.access(self.image_path, os.R_OK))

        if not file_is_ok:
            logging.error("File {0} is not ready. Cannot upload".format(self.image_path))
            return

        insta = InstagramAPI(self.username, self.password)
        try:
            insta.login()  # login
            insta.uploadPhoto(self.image_path, self.hashtag)
        finally:
            insta.logout()
        #insta.up
        #insta.uploadVideo(video_local_path, thumbnail_local_path, caption="Tortuguero")

        logging.info("Uploaded image {0} to instagram".format(self.image_path))


if __name__ == '__main__':
    iu = InstagramUpload("colawedding", "s22a10C!", "/Users/stefan/Downloads/IMG_1092.JPG", "#colawedding")
    iu.start()