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
    def print_image(image_path):
        # Set up CUPS
        conn = cups.Connection()
        #printers = conn.getPrinters()
        printer_name = "Canon_SELPHY_CP1300"
        logging.info("Printer: {0}".format(printer_name))
#cups.setUser('tiger-222')

        # Image (code taken from boothcam.py)
        im = Image.new('RGBA', (683, 384))
        im.paste(Image.open(image_path).resize((683, 384)), ( 0, 0, 683, 384))

        # Save data to a temporary file
        output = mktemp(prefix='jpg')
        im.save(output, format='jpeg')

        # Send the picture to the printer
        print_id = conn.printFile(printer_name, output, "Photo Booth", {})
        # Wait until the job finishes
        while conn.getJobs().get(print_id, None):
            sleep(1)
        unlink(output)

if __name__ == '__main__':
    Printer.print_image("../../IMG_8049.JPEG")
