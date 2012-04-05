
"""
	Version 0.1 alpha
	(c) 2011 Johannes Lindenbaum
	
	License: Do what you want, give credit where credit is due
"""

import argparse
import os
import Image


class AndroidResResize:
	
	SCALES = {
		'hdpi': 0.75,
		'mdpi': 0.5,
		'ldpi': 0.5 * 0.75,
	}
	
	
	ACCEPTED_EXTENSIONS = ['.png']
	
	# OUTPUT_DIR = [
	# 	'hdpi': '/Users/johannes/Desktop/test/drawable-hdpi/'
	# ]
	
	def resizeAllInFolder(self, path):
		print "Processing folder " + path
		
		# TODO - determine trailing slash in path
		
		for fileName in os.listdir(path):
			fullPath = path + fileName
			baseName, fileExtension = os.path.splitext(path + fileName)
			#print baseName + " -- " + fileExtension
			
			if fileExtension in self.ACCEPTED_EXTENSIONS:
				
				for scale in self.SCALES:
					print "Processing (" + scale + "): " + fullPath
					scaleValue = self.SCALES[scale]
					
					image = Image.open(fullPath)
					imageSize = image.size
					newWidth = int(round(imageSize[0] * scaleValue))
					newHeight = int(round(imageSize[1] * scaleValue))
					imageHdpi = image.resize((newWidth, newHeight), Image.ANTIALIAS)
					# TODO - determine file path exists
					imageHdpi.save("/Users/johannes/Desktop/testimg/drawable-" + scale + "/" + fileName)
		

if __name__ == "__main__":
	print "Initializing..."
	
	argParser = argparse.ArgumentParser(description="Automatically resize images for Android res/")
	argParser.add_argument("--folder", default=None, required=True, dest="folderPath")
	args = argParser.parse_args()
	
	resizer = AndroidResResize()
	resizer.resizeAllInFolder(args.folderPath)
	
	print "Done..."
