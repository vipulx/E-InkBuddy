#!/usr/bin/python
# -*- coding:utf-8 -*-
# Import necessary modules
import sys
import os

# Define the directory paths for images and libraries
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

# Check if the library directory exists and add it to the system path
if os.path.exists(libdir):
    sys.path.append(libdir)

# Import required libraries for logging, e-paper display, image processing, and error handling
import logging
from waveshare_epd import epd2in13_V4
import time
from PIL import Image
import traceback

# Set up logging configuration to display debug messages
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13_V4 Photo Viewer")  # Log the start of the photo viewer

    # Initialize the e-paper display
    epd = epd2in13_V4.EPD()  # Create an instance of the EPD class
    logging.info("Initializing and clearing display")  # Log initialization
    epd.init()  # Initialize the display
    epd.Clear(0xFF)  # Clear the display with white color

    # Check if the picture directory exists
    if not os.path.exists(picdir):
        logging.error("Picture directory not found!")  # Log error if directory is missing
        exit()  # Exit the program

    # List all image files in the "pic" directory with specific extensions
    image_files = [f for f in os.listdir(picdir) if f.endswith(('.bmp', '.png', '.jpg', '.jpeg'))]

    # Check if any images were found
    if not image_files:
        logging.warning("No images found in the 'pic' directory.")  # Log warning if no images
        exit()  # Exit the program

    logging.info(f"Found {len(image_files)} images.")  # Log the number of images found

    # Cycle through the images and display them
    for img_file in image_files:
        try:
            logging.info(f"Displaying {img_file}")  # Log the current image being displayed
            image_path = os.path.join(picdir, img_file)  # Construct the full image path

            # Open and process the image
            image = Image.open(image_path)  # Open the image file
            image = image.convert('1')  # Convert the image to 1-bit mode for e-paper
            image = image.resize((epd.height, epd.width))  # Resize the image to fit the display

            # Display the image on the e-paper
            epd.display(epd.getbuffer(image))  # Send the image buffer to the display
            time.sleep(5)  # Keep the image displayed for 5 seconds
        except Exception as e:
            logging.error(f"Error displaying {img_file}: {e}")  # Log any errors that occur during display

    # Clear the display and put the device to sleep after cycling through images
    logging.info("Clearing display and entering sleep mode.")  # Log the transition to sleep mode
    epd.init()  # Reinitialize the display
    epd.sleep()  # Put the display into sleep mode

except IOError as e:
    logging.info(e)  # Log any IO errors that occur

except KeyboardInterrupt:
    logging.info("ctrl + c:")  # Log if the program is interrupted by the user
    epd2in13_V4.epdconfig.module_exit(cleanup=True)  # Clean up the display module
    exit()  # Exit the program
