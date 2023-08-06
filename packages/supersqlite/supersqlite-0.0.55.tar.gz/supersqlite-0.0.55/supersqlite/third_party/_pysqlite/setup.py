#-*- coding: ISO-8859-1 -*-
# setup.py: the distutils script
#
# Copyright (C) 2004-2015 Gerhard H�ring <gh@ghaering.de>
#
# This file is part of pysqlite.
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import sys
# BEGIN PLASTICITY COMMENT OUT
# if sys.version_info[0] > 2:
#     print("pysqlite is not supported on Python 3. When using Python 3, use the sqlite3 module from the standard library.")
#     sys.exit(1)
# elif sys.version_info[:2] != (2, 7):
#     print("Only Python 2.7 is supported.")
#     sys.exit(1)
# END PLASTICITY COMMENT OUT

'''
BEGIN CUSTOM PLASTICITY OS COMMANDS
'''
from multiprocessing import Process
from subprocess import Popen, PIPE
def system_with_status_and_output(
        command, attach_env=True, should_silence_err=False,
        exit_with_error_message=None, _stdout=PIPE):
    """Runs a system command with various options and returns
    the status of the command and the output of the command.
    """
    if should_silence_err:
        stderr = open(os.devnull, 'wb')
    else:
        stderr = None
    envd = {}
    if attach_env:
        envd = dict(os.environ)
    child = Popen(
        args=command, stdout=_stdout, stderr=stderr, shell=True, env=envd)
    output = child.communicate()[0][:-1]
    status = child.returncode
    if status != 0 and exit_with_error_message is not None:
        exit(exit_with_error_message)
    return [status, output]


def system_with_output(
        command, attach_env=True, should_silence_err=False,
        exit_with_error_message=None):
    """Runs a system command with various options and returns
    the output of the command.
    """
    return system_with_status_and_output(
        command, attach_env, should_silence_err, exit_with_error_message)[1]
'''
END CUSTOM PLASTICITY OS COMMANDS
'''

import glob
import os
import re
import shutil

from distutils.core import setup, Extension, Command
from distutils.command.build import build
from distutils.command.build_ext import build_ext

import cross_bdist_wininst

# If you need to change anything, it should be enough to change setup.cfg.

sqlite = "sqlite"

# BEGIN PLASTICITY
import sys
if sys.version_info >= (3, 0):
    s_folder = 'src3'
else:
    s_folder = 'src2'

# END PLASTICITY

PYSQLITE_EXPERIMENTAL = False

sources = [s_folder+"/module.c", s_folder+"/connection.c", s_folder+"/cursor.c", s_folder+"/cache.c",
           s_folder+"/microprotocols.c", s_folder+"/prepare_protocol.c", s_folder+"/statement.c",
           s_folder+"/util.c", s_folder+"/row.c"] # PLASTICITY

if PYSQLITE_EXPERIMENTAL:
    sources.append(s_folder+"/backup.c") # PLASTICITY

include_dirs = []
library_dirs = []
libraries = []
runtime_library_dirs = []
extra_objects = []
define_macros = []

long_description = \
"""Python interface to SQLite 3

pysqlite is an interface to the SQLite 3.x embedded relational database engine.
It is almost fully compliant with the Python database API version 2.0 also
exposes the unique features of SQLite."""

if sys.platform != "win32":
    define_macros.append(('MODULE_NAME', '"pysqlite2.dbapi2"'))
else:
    define_macros.append(('MODULE_NAME', '\\"pysqlite2.dbapi2\\"'))

class TestRunner(Command):
    description = "Runs the unit tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_dir = "build/lib.linux-x86_64-%i.%i" % sys.version_info[:2]
        sys.path.append(build_dir)
        from pysqlite2 import test
        result = test.test()
        if result.errors or result.failures:
            sys.exit(1)

class DocBuilder(Command):
    description = "Builds the documentation"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            shutil.rmtree("build/doc")
        except OSError:
            pass
        os.makedirs("build/doc")
        rc = os.system("sphinx-build doc/sphinx build/doc")
        if rc != 0:
            sys.stdout.write("Is sphinx installed? If not, try 'sudo pip sphinx'.\n")

class AmalgamationBuilder(build):
    description = "Build a statically built pysqlite using the amalgamtion."

    def __init__(self, *args, **kwargs):
        MyBuildExt.amalgamation = True
        build.__init__(self, *args, **kwargs)

class MyBuildExt(build_ext):
    amalgamation = False

    def _pkgconfig(self, flag, package):
        status, output = system_with_status_and_output("pkg-config %s %s" % (flag, package)) # PLASTICITY
        return output

    def _pkgconfig_include_dirs(self, package):
        return [x.strip() for x in 
                self._pkgconfig("--cflags-only-I",
                                package).replace("-I", " ").split()]

    def _pkgconfig_library_dirs(self, package):
        return [x.strip() for x in 
                self._pkgconfig("--libs-only-L",
                                package).replace("-L", " ").split()]


    def build_extension(self, ext):
        if self.amalgamation:
            ext.sources.append("sqlite3.c")
            ext.sources.append("icu.cpp") # PLASTICITY
        try:
            raise Exception("skip") # PLASTICITY
            ext.include_dirs = self._pkgconfig_include_dirs("sqlite3")
            ext.library_dirs = self._pkgconfig_library_dirs("sqlite3")
        except: # Plasticity
            pass # no pkg_config installed
        build_ext.build_extension(self, ext)

    def __setattr__(self, k, v):
        # Make sure we don't link against the SQLite library, no matter what setup.cfg says
        if self.amalgamation and k == "libraries":
            v = None
        self.__dict__[k] = v

'''
BEGIN CUSTOM PLASTICITY INSTALL COMMANDS
'''
from sys import platform

from distutils.command.install import install # PLASTICITY

class CustomInstallCommand(install):
    def run_build_static(self):
        self.run_command('build_static')

    def run_build_process(self):
        p = Process(target=self.run_build_static)
        p.start()
        p.join()
        return p.exitcode

    def run(self):
        # Hail mary try to install all python development libraries / headers for the user
        # across all platforms
        exitcodes = []
        exitcodes.append(self.run_build_process())
        best_exitcode = min(exitcodes)
        if best_exitcode > 0:
            print("Error building SQLite!")
            sys.exit(1)
        install.run(self)

'''
END CUSTOM PLASTICITY INSTALL COMMANDS 
'''

# BEGIN PLASTICITY
SQLITE3 = "../sqlite3"
include_plasticity = [SQLITE3] 
ICU = SQLITE3 + '/icu'
include_plasticity.append(ICU)
# END PLASTICITY

def get_setup_args():

    PYSQLITE_VERSION = None

    version_re = re.compile('#define PYSQLITE_VERSION "(.*)"')
    # f = open(os.path.join("src", "module.h")) # PLASTICITY COMMENT OUT
    import codecs # PLASTICITY
    f = codecs.open(os.path.join(s_folder, "module.h"), "r",encoding='utf-8', errors='ignore') # PLASTICITY
    for line in f:
        match = version_re.match(line)
        if match:
            PYSQLITE_VERSION = match.groups()[0]
            PYSQLITE_MINOR_VERSION = ".".join(PYSQLITE_VERSION.split('.')[:2])
            break
    f.close()

    if not PYSQLITE_VERSION:
        sys.stdout.write("Fatal error: PYSQLITE_VERSION could not be detected!\n")
        sys.exit(1)

    data_files = [("pysqlite2-doc",
                        glob.glob("doc/*.html") \
                      + glob.glob("doc/*.txt") \
                      + glob.glob("doc/*.css")),
                   ("pysqlite2-doc/code",
                        glob.glob("doc/code/*.py"))]

    py_modules = ["sqlite"]
    setup_args = dict(
            name = "pysqlite",
            version = PYSQLITE_VERSION,
            description = "DB-API 2.0 interface for SQLite 3.x",
            long_description=long_description,
            author = "Gerhard Haering",
            author_email = "gh@ghaering.de",
            license = "zlib/libpng license",
            platforms = "ALL",
            url = "http://github.com/ghaering/pysqlite",

            # Description of the modules and packages in the distribution
            package_dir = {"pysqlite2": "lib"},
            packages = ["pysqlite2"],
            scripts=[],

            ext_modules = [Extension( name="pysqlite2._sqlite",
                                      sources=sources,
                                      include_dirs=include_dirs + include_plasticity, # PLASTICITY
                                      library_dirs=library_dirs,
                                      runtime_library_dirs=runtime_library_dirs,
                                      libraries=libraries + (["user32", "Advapi32"] if sys.platform == "win32" else []), # PLASTICITY
                                      extra_objects=extra_objects,
                                      define_macros=define_macros,
                                      extra_compile_args=["-O4", "-std=c++11"], # PLASTICITY
                                      extra_link_args=["-flto"], # PLASTICITY
                                      )],
            classifiers = [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: zlib/libpng License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Programming Language :: C",
            "Programming Language :: Python :: 2 :: Only",
            "Topic :: Database :: Database Engines/Servers",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
            cmdclass = {"build_docs": DocBuilder}
            )

    setup_args["cmdclass"].update({
        "build_docs": DocBuilder,
        "test": TestRunner,
        "build_ext": MyBuildExt,
        "build_static": AmalgamationBuilder,
        "install": CustomInstallCommand, # PLASTICITY
        "bdist_wheel": CustomInstallCommand, # PLASTICITY
        "cross_bdist_wininst": cross_bdist_wininst.bdist_wininst
    })
    return setup_args

def main():
    setup(**get_setup_args())

if __name__ == "__main__":
    main()
