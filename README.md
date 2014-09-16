arc-analyse
===========

ARC(`Android Runtime for Chrome`) Analyse

ARC source codes live in https://chromium.googlesource.com/arc/arc/

Basic Architecture 
==================

Most files in `_platform_specific/nacl_${arch}/` should be in `/system/lib/` for Android.

`_platform_specific/nacl_${arch}/`:

* arc_nacl_x86_64.nexe

The main program which build up the Android runtime.

* dalvikvm.so
* dexopt.so

These libraries should be wrappers for `dalvikvm` and `dexopt`.

* libEGL_translator.so
* libGLESv1_enc.so
* libGLESv2_enc.so
* libGLES_V2_translator.so
* libGLES_CM_translator.so
* libOpenglRender.so
* libOpenglSystemCommon.so
* lib_renderControl_enc.so

These libraries seem like `OpenGL ES` hardware emulation for Android Emulator, in `$ANDROID/sdk/emulator/opengl/`

* readonly_fs_image.img

This is the filesystem image for Android, which can be extracted by `fs-extract.py`.



Tools
=====

`fs-extract.py <readonly_fs_image.img> <output-directory>`

* A tool to extract files from `readonly_fs_image.img`

