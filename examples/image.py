#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V4 Photo Viewer")

    # Initialize the e-paper display
    epd = epd2in13_V4.EPD()
    logging.info("Initializing and clearing display")
    epd.init()
    epd.Clear(0xFF)

    # List all images in the "pic" directory
    if not os.path.exists(picdir):
        logging.error("Picture directory not found!")
        exit()

    image_files = [f for f in os.listdir(picdir) if f.endswith(('.bmp', '.png', '.jpg', '.jpeg'))]

    if not image_files:
        logging.warning("No images found in the 'pic' directory.")
        exit()

    logging.info(f"Found {len(image_files)} images.")

    # Cycle through the images and display them
    for img_file in image_files:
        try:
            logging.info(f"Displaying {img_file}")
            image_path = os.path.join(picdir, img_file)

            # Open and process the image
            image = Image.open(image_path)
            image = image.convert('1')  # Convert to 1-bit mode for e-paper
            image = image.resize((epd.height, epd.width))  # Resize to fit the display

            # Display the image
            epd.display(epd.getbuffer(image))
            time.sleep(5)  # Display each image for 5 seconds
        except Exception as e:
            logging.error(f"Error displaying {img_file}: {e}")

    # Clear the display and put the device to sleep
    logging.info("Clearing display and entering sleep mode.")
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
