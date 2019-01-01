# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API
.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>
License : GPL(v3)
**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.
"""
from __future__ import print_function
import os
import sys
import shutil
import threading
import subprocess
import distutils.core
import distutils.command.build_clib
import distutils.dir_util
import distutils.errors
import pyozw_version


# read further down as to what this is for
DLL_MAIN = '''

void PyInit_OpenZwave() {}

'''

# this is an easy macro to tell if a debugging version of python is what is
# running if it is what is running then we want to build a debugging version
# of openzwave. the use of this will allow you to set any preprocessor
# macros to build a debugging version of openzwave

DEBUG_BUILD = os.path.splitext(sys.executable)[0].endswith('_d')

# when building openzwave with distutils you will need to include the
# python library file in the list of libraries. creates that filename for ya.
PYTHON_LIB = (
    'python%s%s' % (sys.hexversion >> 24, (sys.hexversion >> 16) & 0xff)
)

# this is a thread lock for printing. I use 10 threads in the windows
# compilation of openzwave to compile it. it speeds up the build process a lot.
# but we do not want to get the output all jumbled up so before printing
# anything from the output buffer we use this lock before we print the
# output buffer to stdout or stderr. we iterate over the output buffer line
# by line so if this lock is not in place the lines that get printed would be
# out of order.
print_lock = threading.Lock()


# in order to have distutils handle the building of openzwave there has to be
# a call to PyInit so we create a cpp file and place the call in it. The call
# actually does nothing except allow openzwave to be built.
def build_dll_main(openzwave):
    dll_main_path = openzwave + '\\cpp\\dllmain.cpp'
    with open(dll_main_path, 'w') as f:
        f.write(DLL_MAIN)


# if you did decice to have distutils handle the building of openzwave you
# will need to generate a list of the source files this the function to do that
# you pass it the location of the source files and also a list of
# directories/files that you want to ignore (ie: for windows we want to
# ignore the linux and mac folders
def get_sources(src_path, ignore):
    found = []
    for src_f in os.listdir(src_path):
        src = os.path.join(src_path, src_f)
        if os.path.isdir(src):
            if src_f.lower() in ignore:
                continue

            found += get_sources(src, ignore)
        elif src_f.endswith('.c') or src_f.endswith('.cpp'):
            found += [src]
    return found


# This is a much cleaner version of the download openzwave. it does not write
# anything to the disk except the extracted zip contents. There is no
# "temporary" zip file written first.
def get_openzwave(opzw_dir):
    url = 'https://codeload.github.com/OpenZWave/open-zwave/zip/master'

    print(
        "fetching {0} into "
        "{1} for version {2}".format(url, opzw_dir, pyozw_version)
    )

    import io
    import zipfile

    try:
        from urllib2 import urlopen  # py2
    except ImportError:
        from urllib.request import urlopen  # py3

    response = urlopen(url)
    dst_file = io.BytesIO(response.read())

    dst_file.seek(0)
    zip_ref = zipfile.ZipFile(dst_file, 'r')
    dst = os.path.split(opzw_dir)[0]
    zip_ref.extractall(dst)
    zip_ref.close()
    dst_file.close()

    dst = os.path.join(dst, zip_ref.namelist()[0])

    if dst != opzw_dir:
        os.rename(dst, opzw_dir)


class Extension(distutils.core.Extension):
    # right now you use a dictionary in which you add the various information
    # to. and this is very hard to follow. in the end you then pass the
    # dictionary to the parent class of this class. You can trim down on the
    # hard to follow dictionary use and simply place the code that pertains
    # to a specific OS into a subclass of this class and just pass an instance
    # of that class directly to setup() this works pretty much the same as
    # the Library class. you would add a subclass of this class and a subclass
    # of the Library class to a file that is specific to that OS.

    def __init__(
        self,
        openzwave,
        flavor,
        static,
        backend,
        extra_objects,
        sources,
        include_dirs,
        define_macros,
        libraries,
        extra_compile_args
    ):

        # if you look at the contents of the method you will see that it
        # sets all of the various build settings that are common to all of
        # the OS's it also handles the backend type being cpp or cython. I
        # know there was code added for pybind i have not been able to
        # locate where it is actually used.
        name = 'libopenzwave'
        language = 'c++'

        define_macros += [
            ('PY_LIB_VERSION', pyozw_version.pyozw_version),
            ('PY_LIB_FLAVOR', flavor),
            ('PY_LIB_BACKEND', backend),
            ('CYTHON_FAST_PYCCALL', 1),
            ('_MT', 1),
            ('_DLL', 1)
        ]

        if backend == 'cython':
            define_macros += [('PY_SSIZE_T_CLEAN', 1)]
            sources += ["src-lib/libopenzwave/libopenzwave.pyx"]

        elif backend == 'cpp':
            define_macros += [('PY_SSIZE_T_CLEAN', 1)]
            sources += [
                "openzwave-embed/open-zwave-master/"
                "python-openzwave/src-lib/libopenzwave/libopenzwave.cpp"
            ]
            include_dirs += ["src-lib/libopenzwave"]

        cpp_path = os.path.join(openzwave, 'cpp')
        src_path = os.path.join(cpp_path, 'src')

        if static:
            include_dirs += [
                src_path,
                os.path.join(src_path, 'value_classes'),
                os.path.join(src_path, 'platform')
            ]

        distutils.core.Extension.__init__(
            self,
            name=name,
            language=language,
            extra_objects=extra_objects,
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            libraries=libraries,
            extra_compile_args=extra_compile_args
        )


class Library(object):

    def __init__(
        self,
        openzwave,
        sources=[],
        define_macros=[],
        libraries=[],
        library_dirs=[],
        include_dirs=[],
        extra_compile_args=[],
        extra_link_args=[]
    ):
        self.openzwave = openzwave
        self.name = 'OpenZwave'
        self.sources = sources
        self.define_macros = define_macros
        self.libraries = libraries
        self.library_dirs = library_dirs
        self.include_dirs = include_dirs
        self.extra_compile_args = extra_compile_args
        self.extra_link_args = extra_link_args

    def clean_openzwave(self):
        distutils.command.build_clib.log.info(
            'Removing {0}'.format(self.openzwave)
        )
        try:
            shutil.rmtree(self.openzwave)
            distutils.command.build_clib.log.info(
                'Successfully removed {0}'.format(self.openzwave)
            )
        except OSError:
            distutils.command.build_clib.log.error(
                'Failed to remove {0}'.format(self.openzwave)
            )
        return True

    def clean_cython(self):
        try:
            os.remove('src-lib/libopenzwave/libopenzwave.cpp')
        except Exception:
            pass

    @property
    def so_path(self):
        import pyozw_pkgconfig
        ldpath = pyozw_pkgconfig.libs_only_l('libopenzwave')[2:]

        distutils.command.build_clib.log.info(
            "Running ldconfig on {0}... be patient ...".format(ldpath)
        )

        return ldpath

    # these next 3 methods you would override accordingly. If you check in
    # pyozw_win you will see the use of these methods
    def clean(self, command_class):
        distutils.command.build_clib.log.info(
            "Clean OpenZwave in {0} ... be patient ...".format(
                self.openzwave
            )
        )

    def build(self, _):
        raise NotImplementedError

    def install(self, _):
        raise NotImplementedError


class build_clib(distutils.command.build_clib.build_clib):
    # I have created this class in a manner that will allow it to be used
    # commonly between the different OS's if you look in pyozw_win you will
    # find a subclass of this class. It will show how to setup the build
    # process for the other OS's. You can if you want to have distutils
    # handle all of the building of openzwave as i did for Windows. You will
    # need to set all of the proper compiler arguments. If you do not want to
    # do that then all you would need to do is call spawn with the proper
    # "make" to build it. either way this is a more streamlined mechanism.
    # it also allows you to easily maintain the code because the code for a
    # specific OS is all grouped together.

    def build_libraries(self, libraries):
        self.compiler.spawn = self.spawn
        self.compiler.mkpath = self.mkpath

        for lib in self.original_libraries:
            if self.build_type == 'install':
                distutils.command.build_clib.log.info(
                    "Install OpenZwave... be patient ..."
                )
                lib.install(self)
                distutils.command.build_clib.log.info(
                    "OpenZwave installed and loaded."
                )
            else:
                distutils.command.build_clib.log.info(
                    "building '{0}' library".format(lib.name)
                )
                lib.build(self)

    # we override this method because the original method only known how to
    # process a dict for the library information. I opted to use a class as
    # this is far easier to deal with when adding or changing any of the values
    # so here we create the dict from the class that is wanted by build_clib.
    def finalize_options(self):
        libraries = self.distribution.libraries
        self.original_libraries = libraries
        self.build_type = sys.argv[0].lower()
        converted_libraries = []

        for lib in libraries:
            build_info = dict(
                sources=lib.sources,
                macros=lib.define_macros,
                include_dirs=lib.include_dirs,
            )

            converted_libraries += [(lib.name, build_info)]

        self.distribution.libraries = converted_libraries

        distutils.command.build_clib.build_clib.finalize_options(self)

    # we override the compilers mkpath so we can inject the verbose option.
    # the compilers version does not allow for setting of a verbose level
    # and distutils.dir_util.mkpath defaults to a verbose level of 1 which
    # which prints out each and every directory it makes. This congests the
    # output unnecessarily.
    def mkpath(self, name, mode=0o777):
        distutils.dir_util.mkpath(
            name,
            mode,
            dry_run=self.compiler.dry_run,
            verbose=0
        )

    # this is the workhorse of the build process. it is a mechanism i use to
    # buffer the output from subprocess.Popen and allows me to grab one line
    # at a time as it becomes available. This eliminates any jumping or long
    # pauses in information being written to the screen. This is far simpler
    # then creating additional threads and using queue to pass information off
    # to another thread to print the output. there is also no stalling the
    # thread to wait for output.
    @staticmethod
    def spawn(cmd, search_path=1, level=1, cwd=None):
        if sys.version_info[0] > 2:
            dummy_return = b''
            line_endings = [b'.cpp', b'.c']
        else:
            dummy_return = ''
            line_endings = ['.cpp', '.c']

        if cwd is None:

            p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd
            )

        while p.poll() is None:
            with print_lock:
                for line in iter(p.stdout.readline, dummy_return):
                    line = line.strip()
                    if line:
                        if sys.platform.startswith('win'):
                            for ending in line_endings:
                                if line.endswith(ending):
                                    if sys.version_info[0] > 2:
                                        line = b'compiling ' + line + b'...'
                                    else:
                                        line = 'compiling ' + line + '...'
                                    break
                        if sys.version_info[0] > 2:
                            sys.stdout.write(line.decode('utf-8') + '\n')
                        else:
                            sys.stdout.write(line + '\n')

                for line in iter(p.stderr.readline, dummy_return):
                    line = line.strip()
                    if line:
                        if sys.version_info[0] > 2:
                            sys.stderr.write(line.decode('utf-8') + '\n')
                        else:
                            sys.stderr.write(line + '\n')

        if not p.stdout.closed:
            p.stdout.close()

        if not p.stderr.closed:
            p.stderr.close()

