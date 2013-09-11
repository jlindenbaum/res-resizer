Welcome
=======
Res Resizer is a script that allows you to automatically process resource
files for both Android and iOS projects.

For both iOS and Android you can process an individual file or an entire
folder. There are subtle differences between the way the script handles
resources for different projects.

The script will process PNG and JPG files. It ignores NinePatch files.

iOS
====
If you point the script at a folder, the script will process only images
that contain the @2x modifier in the file name. All other image files
remain untouched. This prevents us from shrinking specific files for
the 4" retina screen. The files are outputted in the same directory with
the @2x omitted from the new file name. Keep in mind this overwrites
any existing file with that file name.

Android
=======
For 0.4.0 I have eliminated outputting images for the ldpi density. The
Android documentation no longer lists this as a requirement.

Point the script at your xxhdpi drawables folder and the script will process
either an individual file, or the entire folder, and output your xhdpi, hdpi,
and mdpi resources in their respective folders. If these folders don't exist
the script will create them for you.

Android Example
===============
Point the script at "res/drawables-xxhdpi", which the script assumes contains
your xxhdpi images.
Should your folder for the lower quality images not exist, the script will
create the folders for you. You will end up with:

* res/drawables-xxhdpi/
* res/drawables-xhdpi/
* res/drawables-hdpi/
* res/drawables-mdpi/

Usage
=====

`$ chmod +x resizer.py` Makes the script runnable.

Hint: all output can be silenced by adding the `--silence` option.

iOS
----
`$./resizer.py -i --folder ~/MyProject/project/images/` resize all
images in the images folder of your project.

`$ ./resizer.py -i --file ~/MyProject/project/images/my_image.png`
resize only one specific image.


Android
-------
`$./resizer.py -a --folder ~/MyProject/res/drawables-xxhdpi` resize all
found images in xxhdpi folder. Script will output in Android style.

`$ ./resizer.py -a --file ~/MyProjects/res/drawables-xxhdpi/my_image.png`
resize specific image only.

`$ ./resizer.py -a --prod` automatically find xxhdpi folder and execute
as with --folder option. Note: --prod does not work with iOS flag.

`$ ./resizer.py --exclude-scale [mdpi|hdpi|xhdpi]` do not scale down to this density.
Exclude multiple at once: `--exclude-scale ldpi mdpi`.

Feedback & Improvements
=======================
Please, let me know what can be improved. Fork it!
