arc-analyse
===========

ARC(`Android Runtime for Chrome`) Analyse

Since ARC is still under developing, we have to analyse it by ourself, and  under the law, of cource.

Basic Architecture 
==========

`_platform_specific/nacl_${arch}/`:

* libEGL_translator.so
* libGLESv1_enc.so
* libGLESv2_enc.so
* libGLES_V2_translator.so
* libGLES_CM_translator.so

These library seems like `OpenGL ES` hardware emulation for Android Emulator, in `$ANDROID/sdk/emulator/opengl`



Tools
=====

fs-extract.py <readonly_fs_image.img> <output-directory>

* A tool to extract files from `readonly_fs_image.img`

