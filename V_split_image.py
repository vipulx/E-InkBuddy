#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/siddhartpic')
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
    logging.info("epd2in13_V4 Photo Viewer with Split Display")

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

    # Cycle through the images in pairs and display them
    for i in range(0, len(image_files), 2):
        try:
            # Prepare the first image
            img1_path = os.path.join(picdir, image_files[i])
            img1 = Image.open(img1_path).convert('1')
            img1 = img1.resize((epd.height // 2, epd.width))  # Resize to fit left half of the display

            # Prepare the second image if available
            if i + 1 < len(image_files):
                img2_path = os.path.join(picdir, image_files[i + 1])
                img2 = Image.open(img2_path).convert('1')
                img2 = img2.resize((epd.height // 2, epd.width))  # Resize to fit right half of the display
            else:
                img2 = Image.new('1', (epd.height // 2, epd.width), 255)  # Blank image

            # Create a combined image
            combined_image = Image.new('1', (epd.height, epd.width), 255)
            combined_image.paste(img1, (0, 0))  # Paste first image on the left
            combined_image.paste(img2, (epd.height // 2, 0))  # Paste second image on the right

            # Display the combined image
            logging.info(f"Displaying {image_files[i]} and {image_files[i + 1] if i + 1 < len(image_files) else 'blank'}")
            epd.display(epd.getbuffer(combined_image))
            time.sleep(5)  # Display for 5 seconds
        except Exception as e:
            logging.error(f"Error displaying images: {e}")

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
