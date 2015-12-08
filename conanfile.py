from conans import ConanFile, CMake
from conans import tools
import os

class libPNGConan(ConanFile):
    name = "libPNG"
    version = "1.6.19"
    settings = "os", "compiler", "build_type", "arch"
    exports = "libpng/*"

    options = { "static": [True, False] }
    default_options = "=False\n".join(options.keys()) + "=False"

    libpng_name = "libpng-1.6.19"
    source_tgz = "http://downloads.sourceforge.net/project/libpng/libpng16/1.6.19/libpng-1.6.19.tar.gz?r=&ts=1449592480&use_mirror=netix"

    def source(self):
        self.output.info("Downloading %s" % self.source_tgz)
        tools.download(self.source_tgz, "libpng.tar.gz")
        tools.unzip("libpng.tar.gz", ".")
        os.unlink("libpng.tar.gz")

    def config(self):
        self.requires.add("zlib/1.2.8@lasote/stable", private=False)
        self.options["zlib"].shared = False

    def build(self):
        config_options_string = ""
        if self.deps_cpp_info.include_paths:
            include_path = self.deps_cpp_info.include_paths[0]
            if self.settings.os == "Windows":
                lib_path = self.deps_cpp_info.lib_paths[0] + "/" + self.deps_cpp_info.libs[0] + ".lib"  # Concrete lib file
            else:
                lib_path = self.deps_cpp_info.lib_paths[0]  # Just path, linux will find the right file
            config_options_string += ' -DZLIB_INCLUDE_DIR="%s"' % include_path
            config_options_string += ' -DZLIB_LIBRARY="%s"' % lib_path
            self.output.warn("=====> Options: %s" % config_options_string)

        cmake = CMake(self.settings)
        self.run('cd %s && cmake -DCMAKE_INSTALL_PREFIX:PATH=../build . %s %s' % (self.libpng_name, cmake.command_line, config_options_string))
        self.run("cd %s && cmake --build . --target install %s" % (self.libpng_name, cmake.build_config))

    def package(self):
        self.copy("*.h", dst="include", src="build/include")
        self.copy("*.lib", dst="lib", src="build/lib")
        self.copy("*.a", dst="lib", src="build/lib")

        if not self.options.static:
            self.copy("*.dll", dst="bin", src="build/bin")

    def package_info(self):
        if self.options.static:
            self.cpp_info.libs = ["libpng16_static"]
        else:
            self.cpp_info.libs = ["libpng16"]
