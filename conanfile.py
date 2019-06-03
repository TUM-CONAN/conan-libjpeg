#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import CMake, ConanFile, tools

class LibxmlConan(ConanFile):
    name = "libjpeg"
    package_revision = "-r2"
    upstream_version = "9c"
    version = "{0}{1}".format(upstream_version, package_revision)
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

    def requirements(self):
        self.requires("common/1.0.0@sight/stable")

    def source(self):
        tools.get("http://ijg.org/files/jpegsrc.v%s.tar.gz" % self.upstream_version)
        os.rename("jpeg-" + self.upstream_version, self.source_subfolder)

    def build(self):
        #Import common flags and defines
        import common
        libjpeg_source_dir = os.path.join(self.source_folder, self.source_subfolder)
        shutil.move("patches/CMakeLists.txt", "%s/CMakeLists.txt" % libjpeg_source_dir)
        shutil.move("patches/jconfig.h.cmake", "%s/jconfig.h.cmake" % libjpeg_source_dir)
        shutil.move("patches/jpegdll.def", "%s/jpegdll.def" % libjpeg_source_dir)
        cmake = CMake(self)
        
        #Set common flags
        cmake.definitions["CMAKE_C_FLAGS"] = common.get_c_flags()
        cmake.definitions["CMAKE_CXX_FLAGS"] = common.get_cxx_flags()
        
        if tools.os_info.is_linux:
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = "ON"
        cmake.configure(source_folder=libjpeg_source_dir, build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
