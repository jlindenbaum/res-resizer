#!/usr/bin/env python

"""
    Version 0.3.2
    (c) 2012-2013 Johannes Lindenbaum

    License: MIT License, see LICENSE file for details.

    See README.md for usage and examples.

"""

import argparse
import os
import Image


class AndroidResResize:

    VERSION = '0.3.1'

    SCALES = {
        'hdpi': 0.75,
        'mdpi': 0.5,
        'ldpi': 0.5 * 0.75,
    }

    ACCEPTED_EXTENSIONS = ['.png', '.jpg']

    SILENCE = False

    EXCLUDE_SCALE = []

    """
    Set verbosity level of application.
    Supports verbose or silent
    """
    def setVerbosity(self, silence):
        if silence:
            self.SILENCE = silence;

    """
    Set a scale to exclude from processing.
    Supports ldpi, mdpi, hdpi
    """
    def setExcludeScale(self, scale):
        self.EXCLUDE_SCALE = scale;

    """
    Print to console if script hasn't been silenced
    """
    def log(self, message):
        if self.SILENCE == False:
            print message

    """
    Create directory if it does not exist.
    """
    def createDirIfNonExistant(self, directory):
        if os.path.exists(directory) == False:
            self.log("Creating output directory for image.")
            os.makedirs(directory)

    """
    Process all files in a folder iff these do not have
    illegal extensions and are not NinePatch files
    """
    def resizeAllInFolder(self, inputPath):
        self.log("Processing folder: " + inputPath)

        for fileName in os.listdir(inputPath):
            # when bulk processing a folder ignore NinePatch files
            if fileName[-6:] != ".9.png":
                self.processFile(inputPath, fileName)

    """
    Process an individual file. This includes NinePatch files
    """
    def processFile(self, inputDirectory, fileName):
        # determine file extension
        filePath = os.path.join(inputDirectory, fileName)
        baseName, fileExtension = os.path.splitext(filePath)

        # only consider illegal extensions here - but process NinePatch
        if fileExtension in self.ACCEPTED_EXTENSIONS:

            for scale in self.SCALES:
                if self.EXCLUDE_SCALE != None and scale in self.EXCLUDE_SCALE:
                    continue

                self.log("Processing (" + scale + "): " + filePath)

                # get scale value
                scaleValue = self.SCALES[scale]

                # resize image
                image = Image.open(filePath)
                imageSize = image.size
                newWidth = int(round(imageSize[0] * scaleValue))
                newHeight = int(round(imageSize[1] * scaleValue))

                # be sure the with is never smaller than 1
                if newWidth < 1: newWidth = 1
                if newHeight < 1: newHeight = 1

                imageHdpi = image.resize((newWidth, newHeight), Image.ANTIALIAS)

                # determine if where we're writing to exists
                scaleDir = "../drawable-" + scale + "/"
                outputDirectory = os.path.join(inputDirectory, scaleDir)

                try:
                    self.createDirIfNonExistant(outputDirectory)
                except:
                    print "Could not create output directory: " + outputDirectory
                    return

                # save processed image
                outputFilePath = os.path.join(outputDirectory, fileName)
                try:
                    self.log("Saving: " + outputFilePath)
                    imageHdpi.save(outputFilePath)
                except:
                    print "Could not save image: " + outputFilePath


if __name__ == "__main__":
    argParser = argparse.ArgumentParser(description="Automatically resize images for Android res/")
    argParser.add_argument("--prod", default=None, action="store_true", dest="prod", help="Looks for res/drawable-xhdpi subfolder and resize all the images in that folder.")
    argParser.add_argument("--folder", default=None, dest="folderPath", help="Resizes all images in provided folder path.")
    argParser.add_argument("--file", default=None, dest="filePath", help="Resizes individual file provided by folder path.")
    argParser.add_argument("--exclude-scale", default=None, dest="scale", nargs="+", help="Excludes a scale, such as ldpi. Separate multiple scales by spaces.")
    argParser.add_argument("--silence", default=False, action="store_true", dest="option_silence", help="Silences all output.")
    argParser.add_argument("-v", default=False, action="store_true", dest="show_version", help="Shows the version.")
    args = argParser.parse_args()

    resizer = AndroidResResize()
    resizer.setVerbosity(args.option_silence)
    resizer.setExcludeScale(args.scale)

    if args.show_version:
        print resizer.VERSION
    elif args.prod:
        folderPath = os.path.join(os.getcwd(),"res/drawable-xhdpi")
        if os.path.exists(folderPath):
            resizer.resizeAllInFolder(folderPath)
            resizer.log("Done.")
        else:
            print "Couldn't find res/drawable-xhdpi from your current location."
    elif args.folderPath != None:
        resizer.resizeAllInFolder(args.folderPath)
        resizer.log("Done.")
    elif args.filePath != None:
        inputDirectory, filePath = os.path.split(args.filePath)
        resizer.processFile(inputDirectory, filePath)
        resizer.log("Done.")
    else:
        print "Must specify file or folder to process."
        print ""
        print argParser.print_help()
