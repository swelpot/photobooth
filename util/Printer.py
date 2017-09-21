import cups
from os import unlink

import logging
from PIL import Image
from tempfile import mktemp
from time import sleep


class Printer():
    @staticmethod
    def is_connected(cups_name):
        conn = cups.Connection()
        printers = conn.getPrinters()

        return cups_name in printers

    @staticmethod
    def print_image(cups_name, image_path):
        # Set up CUPS
        conn = cups.Connection()

        # Image (code taken from boothcam.py)
#        im = Image.new('RGBA', (683, 384))
#        im.paste(Image.open(image_path).resize((683, 384)), ( 0, 0, 683, 384))

        # Save data to a temporary file
#        output = mktemp(prefix='jpg')
#        im.save(output, format='jpeg')

        # Send the picture to the printer
#        print_id = conn.printFile(cups_name, output, "Photobooth", {})

        logging.info("Sending file {0} to print on {1}".format(image_path, cups_name))
        print_id = conn.printFile(cups_name, image_path, "Photobooth", {})

        # Wait until the job finishes
        finished = False
        # while not finished:
        #     jobs = conn.getJobs()
        #     print("Jobs: {0}".format(jobs))
        #
        #     job = jobs.get(print_id)
        #     print("Job: {0}".format(job))
        #
        #     if not job:
        #         finished = True
        #
        #     sleep(1)
        while conn.getJobs().get(print_id, None):
            sleep(1)
#        unlink(output)

if __name__ == '__main__':
    Printer.print_image("Canon_SELPHY_CP1300", "../../IMG_2495_2537_2686_2764_print.JPG")
