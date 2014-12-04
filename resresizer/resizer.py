#!/usr/bin/env python

"""
(c) 2012-2014 Johannes Lindenbaum
License: MIT License, see LICENSE file for details.
See README.md for usage and examples.
"""

import argparse
import os
from PIL import Image

class BaseResizer(object):
    VERSION = '1.0.0'
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

    def log(self, message):
        """
        Print to console if script hasn't been silenced
        :param message:
        """
        if self.SILENCE is False:
            print(message)

    def set_exclude_scale(self, scale):
        """
        Set a scale to exclude from processing.
        Android supports mdpi, hdpi, xhdpi, xxhdpi
        iOS supports non-retina
        :param scale:
        """
        self.EXCLUDE_SCALE = scale

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

    def convert_all_in_folder(self, input_path):
        """
        Converts all images in provided folder to PNG.
        This does not alter the file's extension.
        :param input_path:
        :return:
        """
        self.log("Processing folder: " + input_path)
        
        for file_name in os.listdir(input_path):
            base_name, file_extension = os.path.splitext(file_name)
            if self.can_process_file(file_extension):
                image = Image.open(os.path.join(input_path, file_name))
                image.save(os.path.join(input_path, file_name), 'PNG')

    def save_image(self, image, file_path):
        """
        Saves a passed image object to the file path provided, otherwise an exception is printed.
        :param image:
        :param file_path:
        """
        try:
            self.log("Saving: " + file_path)
            image.save(file_path)
        except:
            print("Could not save image: " + file_path)

    def resize_image(self, file_path, width=1, height=1, save=False):
        """
        Opens the passed file_path and resizes the image to the
        provided width and height. Returns the unsaved Image
        object.
        """
        image = Image.open(file_path)
        image = image.resize((width, height), Image.ANTIALIAS)
        return image
    
    def scale_image(self, file_path, scale):
        """
        Opens the passed file_path, sacles that image with scale parameter and
        returns a new image object with the resized image.
        :rtype : Image
        :param file_path:
        :param scale:
        :return:
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
        """
        Determines if we can process the file based off the file extension
        :param file_extension:
        :return:
        """
        return file_extension in self.ACCEPTED_EXTENSIONS

    def process_file(self, input_directory, file_name):
        """
        Process an individual file. This includes NinePatch files
        """
        self.log("This does nothing in the BaseResizer")


class AndroidResResize(BaseResizer):
    SCALES = {
        'xxhdpi' : float(3) / 4, # xxhdpi is 3/4 of xxxhdpi
        'xhdpi': float(2) / 4, 
        'hdpi': float(1.5) / 4,
        'mdpi': float(1) / 4,
    }

    def process_file(self, input_directory, file_name):
        # determine file extension
        file_path = os.path.join(input_directory, file_name)
        base_name, file_extension = os.path.splitext(file_path)
        if self.can_process_file(file_extension):
            for scale_name, scale_value in self.SCALES.items():
                new_image = self.scale_image(file_path, scale_value)

                # determine if where we're writing to exists
                scale_dir = "../drawable-" + scale_name + "/"
                output_directory = os.path.join(input_directory, scale_dir)

                try:
                    self.create_dir_if_nonexistant(output_directory)
                except:
                    print("Could not create output directory: " + output_directory)
                    return

                # save processed image
                output_file_path = os.path.join(output_directory, file_name)
                self.save_image(new_image, output_file_path)


class IOSResResize(BaseResizer):
    app_icon = False
    
    SCALES = {
        '@2x': float(2) / 3, # @2x is 2/3
        '@1x': float(1) / 3
    }
    
    APP_ICON_SIZES = [29, 40, 44, 50, 57, 58, 60, 66, 76, 80, 87, 100, 114, 120, 144, 152, 180]

    def set_process_app_icon(self, process):
        self.app_icon = process

    def process_app_icon(self, input_directory, file_name):
        """
        Processes a provided file name into all known iOS app icon sizes (iOS 6/7).
        :param input_directory:
        :param file_name:
        :return:
        """
        file_path = os.path.join(input_directory, file_name)
        base_name, file_extension = os.path.splitext(file_path)
        base_file_name, extension = os.path.splitext(file_name)
        self.log(base_name + " " + file_extension)
        if self.should_process_file(base_name, file_extension):
            for img_size in self.APP_ICON_SIZES:
                image = self.resize_image(file_path, img_size, img_size)
                new_file_name = "%s-%dx%d%s" % (base_file_name, img_size, img_size, file_extension)
                new_file_path = os.path.join(input_directory, new_file_name)
                self.save_image(image, new_file_path)

    def should_process_file(self, base_name, file_extension):
        """
        Determine if iOS should process this image based off the @2x
        in the file name
        :param base_name:
        :param file_extension:
        :return:
        """
        can_process = self.can_process_file(file_extension)
        should_process = False
        if can_process:
            if "@2x" in base_name or self.app_icon == True:
                should_process = True
        return should_process

    def process_file(self, input_directory, file_name):
        # determine file extension
        file_path = os.path.join(input_directory, file_name)
        base_name, file_extension = os.path.splitext(file_path)
        if self.should_process_file(base_name, file_extension):
            for scale_name, scale_value in self.SCALES.items():
                new_image = self.scale_image(file_path, scale_value)

                # save processed image
                new_file_path = os.path.join(input_directory, file_name.replace("@2x", ""))
                self.save_image(new_image, new_file_path)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="Automatically resize images for iOS and Android")
    
    
    argParser.add_argument("--pngconv", default=False, action="store_true", dest="png_convert", help="Convert an image to PNG format")
    argParser.add_argument("--resize", default=None, dest="resize_dimension", help="Resizes following --file argument to WxH dimension")
    
    argParser.add_argument("--folder", default=None, dest="folder_path", help="Resizes all images in provided folder path.")
    argParser.add_argument("--file", default=None, dest="file_path", help="Resizes individual file provided by folder path.")
    
    argParser.add_argument("-ios", default=False, action="store_true", dest="platform_ios", help="Scale images for iOS projects")
    argParser.add_argument("-android", default=False, action="store_true", dest="platform_android", help="Scale images for Android projects")
    
    argParser.add_argument("--ios-app-icon", default=False, action="store_true", dest="app_icon", help="Takes big image and sizes it for all iOS icon sizes. Use with --i and --file")

    argParser.add_argument("--exclude-scale", default=None, dest="scale", nargs="+", help="Excludes a scale. Separate multiple scales by spaces.")
    argParser.add_argument("--silence", default=False, action="store_true", dest="option_silence", help="Silences all output.")
    argParser.add_argument("-v", default=False, action="store_true", dest="show_version", help="Shows the version.")
    
    argParser.add_argument("--prod", default=None, action="store_true", dest="prod", help="Looks for res/drawable-xxxhdpi subfolder and resizes all the images in that folder.")
    
    args = argParser.parse_args()

    # show version, exit
    if args.show_version:
        print(BaseResizer.VERSION)
        exit()
        
    # convert to png
    if args.png_convert:
        resizer = BaseResizer()
        resizer.set_verbosity(args.option_silence)
        
        resizer.log("Converting file(s) to PNG.")
        if args.file_path is not None:
            input_directory, file_path = os.path.split(args.file_path)
            resizer.process_file(input_directory, file_path)
        elif args.folder_path is not None:
            resizer.convert_all_in_folder(args.folder_path)
        else:
            print("Must specify file or folder to PNG convert")
            print(argParser.print_help())
            
        resizer.log("Done.")

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

        if args.png_convert and args.folder_path is not None:
            resizer.convert_all_in_folder(args.folder_path)
        elif args.prod:
            folder_path = os.path.join(os.getcwd(), "res/drawable-xxxhdpi")
            if os.path.exists(folder_path):
                resizer.resize_all_in_folder(folder_path)
                resizer.log("Done.")
            else:
                print("Couldn't find res/drawable-xxxhdpi from your current location.")
        elif args.folder_path is not None:
            resizer.resize_all_in_folder(args.folder_path)
            resizer.log("Done.")
        elif args.file_path is not None:
            input_directory, file_path = os.path.split(args.file_path)
            if args.app_icon:
                resizer.set_process_app_icon(args.app_icon)
                resizer.process_app_icon(input_directory, file_path)
            else:
                resizer.process_file(input_directory, file_path)
            resizer.log("Done.")
        else:
            print("Must specify file or folder to process.")
            print("")
            print(argParser.print_help())
