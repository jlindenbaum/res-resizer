Welcome
====
Android Res Resize is a script that allows you to automatically process
your Android project's xhdpi drawables into hdpi, mdpi, and ldpi resources.

You can process an entire xhdpi folder or an individual image.

Note: It's always assumed you point this script at an xhdpi folder or image.

The script will go over the provided path (or current working directory)
and scale every PNG and JPG to hdpi, mdpi, and ldpi images.

The script also sorts the scaled images into their appropriate drawables
folders.

Example
====
Point the script at "res/drawables-xhdpi", which the script assumes contains
your xhdpi images.
Should your folder for the lower quality images not exist, the script
will create the folders for you. You will end up with:

* res/drawables-xhdpi/
* res/drawables-hdpi/
* res/drawables-mdpi/
* res/drawables-ldpi/

Usage
====

`$ chmod +x android-res-resize.py` Makes the script runnable.

`$./android-res-resize.py --folder ~/MyProject/res/drawables-xhdpi` resize all
found images in xhdpi folder.

`$ ./android-res-resize.py --file ~/MyProjects/res/drawables-xhdpi/my_image.png`
resize specific image only.

`$ ./android-res-resize.py --prod` automatically find xhdpi folder and execute
as with --folder option.

`$ ./android-res-resize.py --exclude-scale [ldpi|mdpi|hdpi]` do not scale down to this density. Exclude multiple at once: --exclude-scale ldpi, mdpi.

Hint: all output can be silenced by adding the `--silence` option.

Feedback & Improvements
====
Please, let me know what can be improved. Fork it!
