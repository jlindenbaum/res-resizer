#!/usr/bin/env python

"""
(c) 2012-2013 Johannes Lindenbaum
License: MIT License, see LICENSE file for details.
See README.md for usage and examples.
"""

import argparse
import os
import Image


class BaseResizer(object):
    VERSION = '0.4.0'
    SILENCE = False

    SCALES = {}

    ACCEPTED_EXTENSIONS = ['.png', '.jpg']
    UNACCEPTED_EXTENSIONS = ['.9.png']

    EXCLUDE_SCALE = []

    def set_verbosity(self, silence):
        """
        Set verbosity level of application. Supports verbose or silent
        :param silence:
        """
        if silence:
            self.SILENCE = silence

    def set_exclude_scale(self, scale):
        """
        Set a scale to exclude from processing.
        Android supports ldpi, mdpi, hdpi
        iOS supports non-retina
        :param scale:
        """
        self.EXCLUDE_SCALE = scale

    def log(self, message):
        """
        Print to console if script hasn't been silenced
        :param message:
        """
        if self.SILENCE is False:
            print(message)

    def create_dir_if_nonexistant(self, directory):
        """
        Create directory if it does not exist.
        :param directory:
        """
        if os.path.exists(directory) is False:
            self.log("Creating output directory for image.")
            os.makedirs(directory)

    def resize_all_in_folder(self, input_path):
        """
        Process all files in a folder iff these do not have
        illegal extensions and are not NinePatch files
        :param input_path:
        """
        self.log("Processing folder: " + input_path)

        for file_name in os.listdir(input_path):
            # when bulk processing a folder ignore NinePatch files
            if file_name[-6:] not in self.UNACCEPTED_EXTENSIONS:
                self.process_file(input_path, file_name)

    def resize_image(self, file_path, scale):
        """
        Opens the passed file_path, resizes that image with scale and
        returns a new image object with the resized image.
        :rtype : Image
        :param file_path:
        :param scale:
        """
        image = Image.open(file_path)
        image_size = image.size

        new_width = int(round(image_size[0] * scale))
        new_height = int(round(image_size[1] * scale))

        if new_width < 1:
            new_width = 1
        if new_height < 1:
            new_height = 1

        new_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        return new_image

    def can_process_file(self, file_extension):
        if file_extension in self.ACCEPTED_EXTENSIONS:
            return True
        return False

    def process_file(self, input_directory, file_name):
        """
        Process an individual file. This includes NinePatch files
        """
        self.log("This does nothing in the BaseResizer")


class AndroidResResize(BaseResizer):
    SCALES = {
        'xhdpi': float(2) / 3, # xhdpi is 2/3 of xxhdpi
        'hdpi': float(1.5) / 3,
        'mdpi': float(1) / 3,
    }

    def process_file(self, input_directory, file_name):
        # determine file extension
        file_path = os.path.join(input_directory, file_name)
        base_name, file_extension = os.path.splitext(file_path)
        if self.can_process_file(file_extension):
            for scale_name, scale_value in self.SCALES.items():
                new_image = self.resize_image(file_path, scale_value)

                # determine if where we're writing to exists
                scale_dir = "../drawable-" + scale_name + "/"
                output_directory = os.path.join(input_directory, scale_dir)

                try:
                    self.create_dir_if_nonexistant(output_directory)
                except Exception:
                    print("Could not create output directory: " + output_directory)
                    return

                # save processed image
                output_file_path = os.path.join(output_directory, file_name)
                try:
                    self.log("Saving: " + output_file_path)
                    new_image.save(output_file_path)
                except Exception:
                    print("Could not save image: " + output_file_path)


class IOSResResize(BaseResizer):
    SCALES = {
        'non-retina': 0.5,
    }

    def process_file(self, input_directory, file_name):
        # determine file extension
        file_path = os.path.join(input_directory, file_name)
        base_name, file_extension = os.path.splitext(file_path)
        if self.can_process_file(file_extension):
            for scale_name, scale_value in self.SCALES.items():
                new_image = self.resize_image(file_path, scale_value)

                # save processed image
                new_file_path = os.path.join(input_directory, file_name.replace("@2x", ""))
                try:
                    self.log("Saving: " + new_file_path)
                    new_image.save(new_file_path)
                except:
                    print("Could not save image: " + new_file_path)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="Automatically resize images for iOS and Android")
    argParser.add_argument("-i", default=False, action="store_true", dest="platform_ios", help="Scale images for iOS projects")
    argParser.add_argument("-a", default=False, action="store_true", dest="platform_android", help="Scale images for Android projects")
    argParser.add_argument("--prod", default=None, action="store_true", dest="prod", help="Looks for res/drawable-xhdpi subfolder and resize all the images in that folder.")
    argParser.add_argument("--folder", default=None, dest="folder_path", help="Resizes all images in provided folder path.")
    argParser.add_argument("--file", default=None, dest="file_path", help="Resizes individual file provided by folder path.")
    argParser.add_argument("--exclude-scale", default=None, dest="scale", nargs="+", help="Excludes a scale. Separate multiple scales by spaces.")
    argParser.add_argument("--silence", default=False, action="store_true", dest="option_silence", help="Silences all output.")
    argParser.add_argument("-v", default=False, action="store_true", dest="show_version", help="Shows the version.")
    args = argParser.parse_args()

    # show version, exit
    if args.show_version:
        print(BaseResizer.VERSION)
        exit()

    # determine platform
    resizer = None
    if args.platform_ios:
        resizer = IOSResResize()
    elif args.platform_android:
        resizer = AndroidResResize()

    # execute resizing
    if resizer is None:
        print("Must specify resize platform with -i or -a")
        print("")
        print(argParser.print_help())
    else:
        resizer.set_verbosity(args.option_silence)
        resizer.set_exclude_scale(args.scale)

        if args.prod:
            folder_path = os.path.join(os.getcwd(), "res/drawable-xxhdpi")
            if os.path.exists(folder_path):
                resizer.resize_all_in_folder(folder_path)
                resizer.log("Done.")
            else:
                print("Couldn't find res/drawable-xxhdpi from your current location.")
        elif args.folder_path is not None:
            resizer.resize_all_in_folder(args.folder_path)
            resizer.log("Done.")
        elif args.file_path is not None:
            input_directory, file_path = os.path.split(args.file_path)
            resizer.process_file(input_directory, file_path)
            resizer.log("Done.")
        else:
            print("Must specify file or folder to process.")
            print("")
            print(argParser.print_help())
