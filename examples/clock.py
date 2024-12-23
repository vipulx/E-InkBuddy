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
from PIL import Image, ImageDraw, ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V4 Clock")

    # Initialize the e-paper display
    epd = epd2in13_V4.EPD()
    logging.info("Initializing and clearing display")
    epd.init()
    epd.Clear(0xFF)

    # Load font
    font_path = os.path.join(picdir, 'Font.ttc')
    if not os.path.exists(font_path):
        logging.error("Font file not found!")
        exit()
    font_large = ImageFont.truetype(font_path, 24)

    # Create a blank image for the clock
    clock_image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear screen
    clock_draw = ImageDraw.Draw(clock_image)

    # Display the base image
    logging.info("Setting up partial refresh")
    epd.displayPartBaseImage(epd.getbuffer(clock_image))

    # Update the clock display every second
    while True:
        try:
            # Clear the area for the clock
            clock_draw.rectangle((0, 0, epd.height, epd.width), fill=255)

            # Get current time and draw it
            current_time = time.strftime('%H:%M:%S')
            clock_draw.text((30, 50), current_time, font=font_large, fill=0)

            # Refresh the display with partial update
            epd.displayPartial(epd.getbuffer(clock_image))
            time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Clock interrupted by user")
            break

    # Cleanup
    logging.info("Clearing display and going to sleep")
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
