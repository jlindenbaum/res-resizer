#!/usr/bin/env python

import argparse
import os
import importlib
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def log(message):
    print(message)

def resize_image(file_path, width, height):
    image = Image.open(file_path)
    image = image.resize((width, height), Image.ANTIALIAS)
    return image

def process_file(source_image=None, width=0, height=0, destination='./', destination_suffix=''):
    # source image file info
    source_directory, source_file_name = os.path.split(source_image)
    source_base_name, source_file_extension = os.path.splitext(source_file_name)
    
    image = resize_image(source_image, width, height)
    log("Source dir: %s source base: %s" % (source_directory, source_base_name))
    target_image_file_name = "%s%s%s" % (source_base_name, destination_suffix, source_file_extension)
    log("Target file name %s" % target_image_file_name)
    target_image = os.path.join(source_directory, destination, target_image_file_name)
    log("Target: %s" % target_image)

    image.save(target_image)

def start_processing(source_file, size, plugin_module):
    """
    Method determines everything we need to resize the source image.
    """
    # determine width / height
    width, height = size.split('x')

    # load plugin and image scales
    plugin = importlib.import_module("plugins.%s" % plugin_module)

    log("Plugin config: %s" % plugin.config)

    log("Processing %s to 1x size of %s for %s" % (source_file, size, plugin))

    #process the file
    for scale in plugin.config:
        process_width = int(width) * scale
        process_height = int(height) * scale
        destination = plugin.config[scale][0]
        file_suffix = plugin.config[scale][1]
        log("Scale factor %s. Size %sx%s. Dest %s. Suffix %s." % (scale, int(process_width), int(process_height), destination, file_suffix))
        process_file(source_file, int(process_width), int(process_height), destination, file_suffix)


# base case
#python resizer.py -s 32x32 -p ios -f my-file.png

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="Image resizing for iOS and Android")
    argParser.add_argument("-p", default=False, dest="plugin", help="Determines which plugin to load scale factors form. ios / and")
    argParser.add_argument("-s", default=False, dest="size", help="Final size of the image at 1x - ex. -s 32x32")
    argParser.add_argument("-f", default=False, dest="source_image", help="Image path to source image")
    args = argParser.parse_args()
    start_processing(args.source_image, args.size, args.plugin)

