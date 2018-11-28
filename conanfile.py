#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import CMake, ConanFile, tools

class LibxmlConan(ConanFile):
    name = "libjpeg"
    version = "9c"
    description = "Libjpeg is a widely used C library for reading and writing JPEG image files."
    generators = "cmake"
    settings =  "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = [
        "patches/CMakeLists.txt",
        "patches/jconfig.h.cmake",
        "patches/jpegdll.def"
    ]
    url = "https://git.ircad.fr/conan/conan-libjpeg"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("http://ijg.org/files/jpegsrc.v%s.tar.gz" % self.version)
        os.rename("jpeg-" + self.version, self.source_subfolder)

    def build(self):
        libjpeg_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.move("patches/CMakeLists.txt", "%s/CMakeLists.txt" % libjpeg_source_dir)
        shutil.move("patches/jconfig.h.cmake", "%s/jconfig.h.cmake" % libjpeg_source_dir)
        shutil.move("patches/jpegdll.def", "%s/jpegdll.def" % libjpeg_source_dir)
        cmake = CMake(self)
        if tools.os_info.is_linux:
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = "ON"
        cmake.configure(source_folder=libjpeg_source_dir, build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
