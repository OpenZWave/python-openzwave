#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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

Build process :
- ask user what to do (zmq way in pip)
- or parametrizes it
    --dev : use local sources and cythonize way (for python-openzwave devs, ...)
    --embed : use local sources and cpp file (for third parties packagers, ...)
    --git : download openzwave from git (for geeks)
    --shared : use pkgconfig and cython (for debian devs and common users)
    --pybind : use pybind alternative (not tested)
    --auto (default) : try static, shared and cython, fails if it can't
"""
import time
import os, sys
from os import name as os_name
import re
import shutil
import setuptools
from setuptools import setup, find_packages
from distutils.extension import Extension
from distutils.spawn import find_executable
from distutils import log
from distutils.core import Command
from setuptools.command.install import install as _install
from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean
from setuptools.command.develop import develop as _develop

from platform import system as platform_system
import glob

from pyozw_version import pyozw_version

try:
    PY3 = not unicode
except NameError:
    PY3 = True

LOCAL_OPENZWAVE = os.getenv('LOCAL_OPENZWAVE', 'openzwave')

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))

class Template(object):

    def __init__(self, openzwave=None, cleanozw=False, sysargv=None, flavor="embed", backend="cython"):
        self.openzwave = openzwave
        self._ctx = None
        self.cleanozw = cleanozw
        self.flavor = flavor
        self.backend = backend
        self.sysargv = sysargv
        self.options = dict()
        self.library = []

    def get_default_exts (self):
        exts = { "name": "libopenzwave",
             "sources": [ ],
             "include_dirs": [ ],
             "define_macros": [ ( 'PY_LIB_VERSION', pyozw_version ) ],
             "libraries": [ ],
             "extra_objects": [ ],
             "extra_compile_args": [ ],
             "extra_link_args": [ ],
             "language": "c++",
           }
        return exts

    def cython_context(self):
        exts = self.get_default_exts()
        exts['define_macros'] += [('PY_SSIZE_T_CLEAN',1)]
        exts['sources'] = ["src-lib/libopenzwave/libopenzwave.pyx"]
        return exts

    def cpp_context(self):
        try:
            from distutils.command.build_ext import build_ext
        except ImportError:
            return None
        exts = self.get_default_exts()
        exts['define_macros'] += [('PY_SSIZE_T_CLEAN',1)]
        exts['sources'] = ["openzwave-embed/open-zwave-master/python-openzwave/src-lib/libopenzwave/libopenzwave.cpp"]
        exts["include_dirs"] += [ "src-lib/libopenzwave/" ]
        return exts

    def pybind_context(self):
        exts = self.get_default_exts()
        exts["sources"] = [ "src-lib/libopenzwave/LibZWaveException.cpp",
                          "src-lib/libopenzwave/Driver.cpp",
                          "src-lib/libopenzwave/Group.cpp",
                          "src-lib/libopenzwave/Log.cpp",
                          "src-lib/libopenzwave/Options.cpp",
                          "src-lib/libopenzwave/Manager.cpp",
                          "src-lib/libopenzwave/Notification.cpp",
                          "src-lib/libopenzwave/Node.cpp",
                          "src-lib/libopenzwave/Values.cpp",
                          "src-lib/libopenzwave/libopenzwave.cpp"
                        ]
        exts["include_dirs"] = [ "pybind11/include" ]
        exts['extra_compile_args'] += [ "-fvisibility=hidden" ]
        return exts

    def system_context(self, ctx, static=False):
        #System specific section
        #~ os.environ["CC"] = "gcc"
        #~ os.environ["CXX"] = "g++"
        #~ os.environ["PKG_CONFIG_PATH"] = "PKG_CONFIG_PATH:/usr/local/lib/x86_64-linux-gnu/pkgconfig/"
        log.info("Found platform {0}".format(sys.platform))
        if static:
            ctx['include_dirs'] += [
                "{0}/cpp/src".format(self.openzwave),
                "{0}/cpp/src/value_classes".format(self.openzwave),
                "{0}/cpp/src/platform".format(self.openzwave) ]

        if sys.platform.startswith("win"):
            from pyozw_win import Extension, Library

            self.library += [Library(os.path.abspath(self.openzwave))]
            self.options['build_clib'] = dict(
                build_clib="openzwave\\build\\lib_build",
                build_temp="openzwave\\build\\lib_build\\temp",
                compiler='msvc'
            )

            extension = Extension(
                os.path.abspath(self.openzwave),
                self.flavor,
                static,
                self.backend
            )

            ctx['name'] = extension.name
            ctx['extra_link_args'] = extension.extra_link_args
            ctx['language'] = extension.language
            ctx['extra_objects'] = extension.extra_objects
            ctx['sources'] = extension.sources
            ctx['include_dirs'] = extension.include_dirs
            ctx['define_macros'] = extension.define_macros
            ctx['libraries'] = extension.libraries
            ctx['extra_compile_args'] = extension.extra_compile_args

        elif sys.platform.startswith("cygwin"):
            if static:
                ctx['libraries'] += [ "udev", "stdc++",'resolv' ]
                ctx['extra_objects'] = [ "{0}/libopenzwave.a".format(self.openzwave) ]
                ctx['include_dirs'] += [ "{0}/cpp/build/linux".format(self.openzwave) ]
            else:
                import pyozw_pkgconfig
                ctx['libraries'] += [ "openzwave" ]
                extra = pyozw_pkgconfig.cflags('libopenzwave')
                if extra != '':
                    for ssubstitute in ['', 'value_classes', 'platform']:
                        ctx['extra_compile_args'] += [ os.path.normpath(os.path.join(extra, ssubstitute)) ]

        elif sys.platform.startswith("darwin") :
            ctx['extra_link_args'] += [ "-framework", "CoreFoundation", "-framework", "IOKit" ]
            ctx['extra_compile_args'] += [ "-stdlib=libc++", "-mmacosx-version-min=10.7" ]

            if static:
                ctx['extra_objects'] = [ "{0}/libopenzwave.a".format(self.openzwave) ]
                ctx['include_dirs'] += [ "{0}/cpp/build/mac".format(self.openzwave) ]
            else:
                import pyozw_pkgconfig
                ctx['libraries'] += [ "openzwave" ]
                extra = pyozw_pkgconfig.cflags('libopenzwave')
                if extra != '':
                    for ssubstitute in ['', 'value_classes', 'platform']:
                        ctx['extra_compile_args'] += [ os.path.normpath(os.path.join(extra, ssubstitute)) ]

        elif sys.platform.startswith("freebsd"):
            os.environ["CPPFLAGS"] = "-Wno-unused-private-field"
            if static:
                ctx['libraries'] += [ "usb", "stdc++" ]
                ctx['extra_objects'] = [ "{0}/libopenzwave.a".format(self.openzwave) ]
                ctx['include_dirs'] += [ "{0}/cpp/build/linux".format(self.openzwave) ]
            else:
                import pyozw_pkgconfig
                ctx['libraries'] += [ "openzwave" ]
                extra = pyozw_pkgconfig.cflags('libopenzwave')
                if extra != '':
                    for ssubstitute in ['', 'value_classes', 'platform']:
                        ctx['extra_compile_args'] += [ os.path.normpath(os.path.join(extra, ssubstitute)) ]

        elif sys.platform.startswith("sunos"):
            if static:
                ctx['libraries'] += [ "usb-1.0", "stdc++",'resolv' ]
                ctx['extra_objects'] = [ "{0}/libopenzwave.a".format(self.openzwave) ]
                ctx['include_dirs'] += [ "{0}/cpp/build/linux".format(self.openzwave) ]
            else:
                import pyozw_pkgconfig
                ctx['libraries'] += [ "openzwave" ]
                extra = pyozw_pkgconfig.cflags('libopenzwave')
                if extra != '':
                    for ssubstitute in ['', 'value_classes', 'platform']:
                        ctx['extra_compile_args'] += [ os.path.normpath(os.path.join(extra, ssubstitute)) ]

        elif sys.platform.startswith("linux"):
            if static:
                ctx['libraries'] += [ "udev", "stdc++",'resolv' ]
                ctx['extra_objects'] = [ "{0}/libopenzwave.a".format(self.openzwave) ]
                ctx['include_dirs'] += [ "{0}/cpp/build/linux".format(self.openzwave) ]
            else:
                import pyozw_pkgconfig
                ctx['libraries'] += [ "openzwave" ]
                extra = pyozw_pkgconfig.cflags('libopenzwave')
                if extra != '':
                    for ssubstitute in ['', 'value_classes', 'platform']:
                        ctx['extra_compile_args'] += [ os.path.normpath(os.path.join(extra, ssubstitute)) ]

        else:
            # Unknown systemm
            raise RuntimeError("Can't detect platform {0}".format(sys.platform))

        return ctx

    @property
    def ctx(self):
        if self._ctx is None:
            if 'install' in sys.argv or 'develop' in sys.argv or 'bdist_egg' in sys.argv:
                current_template.install_minimal_dependencies()
            self._ctx = self.get_context()
            self.finalize_context(self._ctx)
        return self._ctx

    @property
    def build_ext(self):
        if 'install' in sys.argv or 'develop' in sys.argv or 'bdist_egg' in sys.argv:
            current_template.install_minimal_dependencies()
        from Cython.Distutils import build_ext as _build_ext

        class BuildExt(_build_ext):
            def build_extension(self, ext):
                ext_path = self.get_ext_fullpath(ext.name)
                if 'bdist_wheel' in sys.argv:
                    if not os.path.exists(ext_path):
                        _build_ext.build_extension(self, ext)
                else:
                    _build_ext.build_extension(self, ext)

        return BuildExt

    @property
    def copy_openzwave_config(self):
        return True

    @property
    def install_openzwave_so(self):
        return False

    def finalize_context(self, ctx):
        self.clean_cython()
        if self.flavor:
            ctx['define_macros'] += [('PY_LIB_FLAVOR', self.flavor.replace('--flavor=',''))]
        else:
            ctx['define_macros'] += [('PY_LIB_FLAVOR', "embed")]
        if self.backend:
            ctx['define_macros'] += [('PY_LIB_BACKEND', self.backend)]
        else:
            ctx['define_macros'] += [('PY_LIB_BACKEND', "cython")]
        return ctx

    def install_requires(self):
        return ['Cython']

    def build_requires(self):
        return ['Cython']

    def build(self):
        if len(self.ctx['extra_objects']) == 1 and os.path.isfile(self.ctx['extra_objects'][0]):
            log.info("Use cached build of openzwave")
            return True
        from subprocess import Popen, PIPE
        from threading import Thread
        try:
            from Queue import Queue, Empty
        except ImportError:
            from queue import Queue, Empty

        io_q = Queue()

        def stream_watcher(identifier, stream):
            # fixes subprocess output lag issue when using python 2.x

            if PY3:
                dummy_return = b''
            else:
                dummy_return = ''

            for line in iter(stream.readline, dummy_return):
                if line:
                    io_q.put((identifier, line))

            if not stream.closed:
                stream.close()

        def printer():
            while True:
                try:
                    # Block for 1 second.
                    item = io_q.get(True, 1)
                except Empty:
                    # No output in either streams for a second. Are we done?
                    if proc.poll() is not None:
                        break
                else:
                    identifier, line = item
                    log.debug(identifier + ':', line)
                    if identifier == 'STDERR':
                        sys.stderr.write('{0}\n'.format(line))
                        log.error('{0}\n'.format(line))

        if sys.platform.startswith("win"):
            return True

        elif sys.platform.startswith("cygwin"):
            log.info("Build openzwave ... be patient ...")
            proc = Popen('make', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("darwin"):
            log.info("Build openzwave ... be patient ...")
            proc = Popen('make', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("freebsd"):
            log.info("Build openzwave ... be patient ...")
            proc = Popen('gmake', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("sunos"):
            log.info("Build openzwave ... be patient ...")
            # fixed command issues to Popen
            proc = Popen(['make', 'PREFIX=/opt/local'], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("linux"):
            log.info("Build openzwave ... be patient ...")
            proc = Popen('make', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        else:
            # Unknown systemm
            raise RuntimeError("Can't detect plateform {0}".format(sys.platform))

        Thread(target=stream_watcher, name='stdout-watcher',
                args=('STDOUT', proc.stdout)).start()
        Thread(target=stream_watcher, name='stderr-watcher',
                args=('STDERR', proc.stderr)).start()

        tprinter = Thread(target=printer, name='printer')
        tprinter.start()
        while tprinter.is_alive():
            time.sleep(1)
        tprinter.join()

        return True

    def install_so(self):
        log.info("Install openzwave so ... be patient ...")
        from subprocess import Popen, PIPE
        from threading import Thread
        try:
            from Queue import Queue, Empty
        except ImportError:
            from queue import Queue, Empty

        io_q = Queue()

        def stream_watcher(identifier, stream):

            for line in stream:
                io_q.put((identifier, line))

            if not stream.closed:
                stream.close()

        def printer():
            while True:
                try:
                    # Block for 1 second.
                    item = io_q.get(True, 1)
                except Empty:
                    # No output in either streams for a second. Are we done?
                    if proc.poll() is not None:
                        break
                else:
                    identifier, line = item
                    log.debug(identifier + ':', line)
                    if identifier == 'STDERR':
                        sys.stderr.write('{0}\n'.format(line))
                        log.error('{0}\n'.format(line))
        if sys.platform.startswith("win"):
            return True

        elif sys.platform.startswith("cygwin"):
            proc = Popen([ 'make', 'install' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("darwin"):
            proc = Popen([ 'make', 'install' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("freebsd"):
            proc = Popen([ 'gmake', 'install' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("sunos"):
            proc = Popen([ 'make', 'PREFIX=/opt/local', 'install' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("linux"):
            proc = Popen([ 'make', 'install' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        else:
            # Unknown systemm
            raise RuntimeError("Can't detect plateform {0}".format(sys.platform))

        Thread(target=stream_watcher, name='stdout-watcher',
                args=('STDOUT', proc.stdout)).start()
        Thread(target=stream_watcher, name='stderr-watcher',
                args=('STDERR', proc.stderr)).start()

        tprinter = Thread(target=printer, name='printer')
        tprinter.start()
        while tprinter.is_alive():
            time.sleep(1)
        tprinter.join()

        if sys.platform.startswith("win"):
            return True

        elif sys.platform.startswith("cygwin"):
            import pyozw_pkgconfig
            ldpath = pyozw_pkgconfig.libs_only_l('libopenzwave')[2:]
            log.info("ldconfig openzwave in {0} so ... be patient ...".format(ldpath))
            proc = Popen([ 'ldconfig', ldpath ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("darwin"):
            import pyozw_pkgconfig
            ldpath = pyozw_pkgconfig.libs_only_l('libopenzwave')[2:]
            log.info("ldconfig openzwave in {0} so ... be patient ...".format(ldpath))
            proc = Popen([ 'ldconfig', ldpath ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("freebsd"):
            import pyozw_pkgconfig
            ldpath = pyozw_pkgconfig.libs_only_l('libopenzwave')[2:]
            log.info("ldconfig openzwave in {0} so ... be patient ...".format(ldpath))
            proc = Popen([ 'ldconfig', ldpath ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("sunos"):
            import pyozw_pkgconfig
            ldpath = pyozw_pkgconfig.libs_only_l('libopenzwave')[2:]
            log.info("ldconfig openzwave in {0} so ... be patient ...".format(ldpath))
            proc = Popen([ 'ldconfig', ldpath ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("linux"):
            import pyozw_pkgconfig
            ldpath = pyozw_pkgconfig.libs_only_l('libopenzwave')[2:]
            log.info("ldconfig openzwave in {0} so ... be patient ...".format(ldpath))
            proc = Popen([ 'ldconfig', ldpath ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        else:
            # Unknown systemm
            raise RuntimeError("Can't detect plateform {0}".format(sys.platform))

        Thread(target=stream_watcher, name='stdout-watcher',
                args=('STDOUT', proc.stdout)).start()
        Thread(target=stream_watcher, name='stderr-watcher',
                args=('STDERR', proc.stderr)).start()

        tprinter = Thread(target=printer, name='printer')
        tprinter.start()
        while tprinter.is_alive():
            time.sleep(1)
        tprinter.join()
        time.sleep(2.5)
        log.info("Openzwave so installed and loaded")
        tprinter = None
        return True

    def clean(self):
        #Build openzwave
        try:
            if not os.path.isdir(self.openzwave):
                return True
        except TypeError:
            return True
        log.info("Clean openzwave in %s ... be patient ..." % (self.openzwave) )
        from subprocess import Popen, PIPE
        from threading import Thread
        try:
            from Queue import Queue, Empty
        except ImportError:
            from queue import Queue, Empty

        io_q = Queue()

        def stream_watcher(identifier, stream):

            for line in stream:
                io_q.put((identifier, line))

            if not stream.closed:
                stream.close()

        def printer():
            while True:
                try:
                    # Block for 1 second.
                    item = io_q.get(True, 1)
                except Empty:
                    # No output in either streams for a second. Are we done?
                    if proc.poll() is not None:
                        break
                else:
                    identifier, line = item
                    log.debug(identifier + ':', line)
                    if identifier == 'STDERR':
                        sys.stderr.write('{0}\n'.format(line))
                        log.error('{0}\n'.format(line))
        proc = None
        if sys.platform.startswith("win"):
            log.info("Clean openzwave project ... be patient ...")
            self.library[0].clean(None)
            return True

        elif sys.platform.startswith("cygwin"):
            proc = Popen([ 'make', 'clean' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("darwin"):
            proc = Popen([ 'make', 'clean' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("freebsd"):
            proc = Popen([ 'gmake', 'clean' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("sunos"):
            proc = Popen([ 'make', 'PREFIX=/opt/local', 'clean' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        elif sys.platform.startswith("linux"):
            proc = Popen([ 'make', 'clean' ], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))

        else:
            # Unknown systemm
            raise RuntimeError("Can't detect plateform {0}".format(sys.platform))

        if proc is not None:
            Thread(target=stream_watcher, name='stdout-watcher',
                    args=('STDOUT', proc.stdout)).start()
            Thread(target=stream_watcher, name='stderr-watcher',
                    args=('STDERR', proc.stderr)).start()

            tprinter = Thread(target=printer, name='printer')
            tprinter.start()
            while tprinter.is_alive():
                time.sleep(1)
            tprinter.join()
        return True

    def clean_all(self):
        log.info("Clean-all openzwave ... be patient ...")
        try:
            from pkg_resources import resource_filename
            dirn = resource_filename('python_openzwave.ozw_config', '__init__.py')
            dirn = os.path.dirname(dirn)
        except ImportError:
            dirn = None
        if dirn is None or (dirn is not None and not os.path.isfile(os.path.join(dirn,'device_classes.xml'))):
            #At first, check in /etc/openzwave
            return self.clean()
        import shutil
        for f in os.listdir(dirn):
            if f not in ['__init__.py', '__init__.pyc']:
                if os.path.isfile(os.path.join(dirn, f)):
                    os.remove(os.path.join(dirn, f))
                elif os.path.isdir(os.path.join(dirn, f)):
                    shutil.rmtree(os.path.join(dirn, f))
        return self.clean()

    def check_minimal_config(self):
        if sys.platform.startswith("win"):
            from pyozw_win import environment
            log.info(str(environment))
            log.info("Found cython : {0}".format(find_executable("cython")))
        else:
            log.info("Found g++ : {0}".format(find_executable("g++")))
            log.info("Found gcc : {0}".format(find_executable("gcc")))
            log.info("Found make : {0}".format(find_executable("make")))
            log.info("Found gmake : {0}".format(find_executable("gmake")))
            log.info("Found cython : {0}".format(find_executable("cython")))
            exe = find_executable("pkg-config")
            log.info("Found pkg-config : {0}".format(exe))
            if exe is not None:
                import pyozw_pkgconfig
                for lib in self.ctx['libraries'] + ['yaml-0.1', 'libopenzwave', 'python', 'python2', 'python3']:
                    log.info("Found library {0} : {1}".format(lib, pyozw_pkgconfig.exists(lib)))

    def install_minimal_dependencies(self):
        if len(self.build_requires()) == 0:
            return

        try:
            from pip import main
            from pip.utils import get_installed_distributions
        except ImportError:
            from pip._internal import main
            from pip._internal.utils.misc import get_installed_distributions

        try:
            log.info("Get installed packages")
            try:
                packages = get_installed_distributions()
            except Exception:
                packages = []
            for pyreq in self.build_requires():
                if pyreq not in packages:
                    try:
                        log.info("Install minimal dependencies {0}".format(pyreq))
                        main(['install', pyreq])
                    except Exception:
                        log.warn("Fail to install minimal dependencies {0}".format(pyreq))
                else:
                    log.info("Minimal dependencies already installed {0}".format(pyreq))
        except Exception:
            log.warn("Can't get package list from pip.")

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        #Get openzwave
        """download an archive to a specific location"""
        dest,tail = os.path.split(self.openzwave)
        dest_file = os.path.join(dest, 'open-zwave.zip')
        if os.path.exists(self.openzwave):
            if not self.cleanozw:
                #~ log.info("Already have directory %s. Use it. Use --cleanozw to clean it.", self.openzwave)
                return self.openzwave
            else:
                #~ log.info("Already have directory %s but remove and clean it as asked", self.openzwave)
                self.clean_all()
                try:
                    os.remove(dest_file)
                except Exception:
                    pass
        log.info("fetching {0} into {1} for version {2}".format(url, dest_file, pyozw_version))
        if not os.path.exists(dest):
            os.makedirs(dest)
        try:
            # py2
            from urllib2 import urlopen
        except ImportError:
            # py3
            from urllib.request import urlopen
        req = urlopen(url)
        with open(dest_file, 'wb') as f:
            f.write(req.read())
        import zipfile
        zip_ref = zipfile.ZipFile(dest_file, 'r')
        zip_ref.extractall(dest)
        zip_ref.close()
        return self.openzwave

    def clean_openzwave_so(self):
        for path in ['/usr/local/etc/openzwave', '/usr/local/include/openzwave', '/usr/local/share/doc/openzwave']:
            try:
                log.info('Try to remove {0}'.format('/usr/local/etc/openzwave'))
                shutil.rmtree(self.openzwave)
            except Exception:
                pass
        return True

    def clean_cython(self):
        try:
            os.remove('src-lib/libopenzwave/libopenzwave.cpp')
        except Exception:
            pass

class DevTemplate(Template):

    def __init__(self, **args):
        Template.__init__(self, **args)

    def get_context(self):
        opzw_dir = LOCAL_OPENZWAVE
        if LOCAL_OPENZWAVE is None:
            if sys.platform.startswith("win"):
                opzw_dir = 'openzwave'
            else:
                return None

        if not os.path.isdir(opzw_dir):
            if sys.platform.startswith("win"):
                from pyozw_common import get_openzwave
                get_openzwave(opzw_dir)
            else:
                return None
        self.openzwave = opzw_dir
        ctx = self.cython_context()
        ctx = self.system_context(ctx, static=True)
        return ctx

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        return True

class GitTemplate(Template):

    def __init__(self, **args):
        Template.__init__(self, openzwave=os.path.join("openzwave-git", 'open-zwave-master'), **args)

    def get_context(self):
        ctx = self.cython_context()
        ctx = self.system_context(ctx, static=True)
        return ctx

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        return Template.get_openzwave(self, url)

    def clean_all(self):
        ret = self.clean()
        dest,tail = os.path.split(self.openzwave)
        if tail == "openzwave-git":
            try:
                log.info('Try to remove {0}'.format(self.openzwave))
                if os.path.isdir(self.openzwave):
                    shutil.rmtree(self.openzwave)
            except Exception:
                pass
        elif tail == 'open-zwave-master':
            try:
                log.info('Try to remove {0}'.format(dest))
                if os.path.isdir(dest):
                    shutil.rmtree(dest)
            except Exception:
                pass
        return ret

class GitSharedTemplate(GitTemplate):

    def get_context(self):
        ctx = self.cython_context()
        ctx = self.system_context(ctx, static=False)
        while '' in ctx['extra_compile_args']:
            ctx['extra_compile_args'].remove('')
        extra = '-I/usr/local/include/openzwave//'
        for ssubstitute in ['/', '/value_classes/', '/platform/']:
            incl = extra.replace('//', ssubstitute)
            if not incl in ctx['extra_compile_args']:
                ctx['extra_compile_args'] += [ incl ]
        return ctx

    @property
    def copy_openzwave_config(self):
        return sys.platform.startswith("win")

    @property
    def install_openzwave_so(self):
        return True

    def clean(self):
        self.clean_openzwave_so()
        return GitTemplate.clean(self)

class OzwdevTemplate(GitTemplate):

    def __init__(self, **args):
        Template.__init__(self, openzwave=os.path.join("openzwave-git", 'open-zwave-Dev'), **args)

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/Dev'):
        return Template.get_openzwave(self, url)

class OzwdevSharedTemplate(GitSharedTemplate):

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/Dev'):
        return Template.get_openzwave(self, url)

class EmbedTemplate(Template):

    def __init__(self, backend='cpp', **args):
        Template.__init__(self, openzwave=os.path.join("openzwave-embed", 'open-zwave-master'), backend=backend, **args)

    @property
    def build_ext(self):
        if 'install' in sys.argv or 'develop' in sys.argv:
            current_template.check_minimal_config()
            current_template.install_minimal_dependencies()
        from distutils.command.build_ext import build_ext as _build_ext
        return _build_ext

    def get_context(self):
        ctx = self.cpp_context()
        ctx = self.system_context(ctx, static=True)
        return ctx

    def install_requires(self):
        return []

    def build_requires(self):
        return []

    def get_openzwave(self, url='https://raw.githubusercontent.com/OpenZWave/python-openzwave/master/archives/open-zwave-master-{0}.zip'.format(pyozw_version)):
        ret =  Template.get_openzwave(self, url)
        shutil.copyfile(os.path.join(self.openzwave,'python-openzwave','openzwave.vers.cpp'), os.path.join(self.openzwave,'cpp','src','vers.cpp'))
        return ret

    def clean(self):
        ret = Template.clean(self)
        try:
            log.info('Try to copy {0}'.format(os.path.join(self.openzwave,'python-openzwave','openzwave.vers.cpp')))
            shutil.copyfile(os.path.join(self.openzwave,'python-openzwave','openzwave.vers.cpp'), os.path.join(self.openzwave,'cpp','src','vers.cpp'))
        except Exception:
            pass
        return ret

    def clean_all(self):
        ret = self.clean()
        dest,tail = os.path.split(self.openzwave)
        if tail == "openzwave-embed":
            try:
                log.info('Try to remove {0}'.format(self.openzwave))
                shutil.rmtree(self.openzwave)
            except Exception:
                pass
        elif tail == 'open-zwave-master':
            try:
                log.info('Try to remove {0}'.format(dest))
                shutil.rmtree(dest)
            except Exception:
                pass
        return ret

class EmbedSharedTemplate(EmbedTemplate):

    def get_context(self):
        ctx = self.cpp_context()
        ctx = self.system_context(ctx, static=False)
        while '' in ctx['extra_compile_args']:
            ctx['extra_compile_args'].remove('')
        extra = '-I/usr/local/include/openzwave//'
        for ssubstitute in ['/', '/value_classes/', '/platform/']:
            incl = extra.replace('//', ssubstitute)
            if not incl in ctx['extra_compile_args']:
                ctx['extra_compile_args'] += [ incl ]
        return ctx

    def clean(self):
        self.clean_openzwave_so()
        return EmbedTemplate.clean(self)

    @property
    def copy_openzwave_config(self):
        return False

    @property
    def install_openzwave_so(self):
        return True

class SharedTemplate(Template):
    def __init__(self,  **args):
        Template.__init__(self, **args)

    def get_context(self):
        ctx = self.cython_context()
        ctx = self.system_context(ctx, static=False)
        return ctx

    def build(self):
        return True

    @property
    def copy_openzwave_config(self):
        return sys.platform.startswith("win")

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        return True

def parse_template(sysargv):
    tmpl = None
    flavor = None
    if '--flavor=dev' in sysargv:
        index = sysargv.index('--flavor=dev')
        flavor = sysargv.pop(index)
        tmpl =  DevTemplate(sysargv=sysargv)
    elif '--flavor=git' in sysargv:
        index = sysargv.index('--flavor=git')
        flavor = sysargv.pop(index)
        tmpl =  GitTemplate(sysargv=sysargv)
    elif '--flavor=git_shared' in sysargv:
        index = sysargv.index('--flavor=git_shared')
        flavor = sysargv.pop(index)
        tmpl =  GitSharedTemplate(sysargv=sysargv)
    elif '--flavor=ozwdev' in sysargv:
        index = sysargv.index('--flavor=ozwdev')
        flavor = sysargv.pop(index)
        tmpl =  OzwdevTemplate(sysargv=sysargv)
    elif '--flavor=ozwdev_shared' in sysargv:
        index = sysargv.index('--flavor=ozwdev_shared')
        flavor = sysargv.pop(index)
        tmpl =  OzwdevSharedTemplate(sysargv=sysargv)
    elif '--flavor=embed' in sysargv:
        index = sysargv.index('--flavor=embed')
        flavor = sysargv.pop(index)
        tmpl =  EmbedTemplate(sysargv=sysargv)
    elif '--flavor=embed_shared' in sysargv:
        index = sysargv.index('--flavor=embed_shared')
        flavor = sysargv.pop(index)
        tmpl =  EmbedSharedTemplate(sysargv=sysargv)
    elif '--flavor=shared' in sysargv:
        index = sysargv.index('--flavor=shared')
        flavor = sysargv.pop(index)
        tmpl =  SharedTemplate(sysargv=sysargv)
    if tmpl is None:
        flavor = 'embed'
        try:
            import pyozw_pkgconfig
            if pyozw_pkgconfig.exists('libopenzwave'):
                flavor = 'shared'
        except:
            log.info("Can't find pkg-config")
        #Default template
        if flavor == 'embed':
            log.info("Use embeded package of openzwave")
            tmpl = EmbedTemplate(sysargv=sysargv)
        elif flavor == 'shared':
            log.info("Use precompiled library openzwave")
            tmpl =  SharedTemplate(sysargv=sysargv)
    tmpl.flavor = flavor
    if '--cleanozw' in sysargv:
        index = sysargv.index('--cleanozw')
        sysargv.pop(index)
        tmpl.cleanozw = True
    log.info('sysargv', sysargv)
    print('sysargv', sysargv)
    log.info("Found SETUP_DIR : {0}".format(SETUP_DIR))
    print("Found SETUP_DIR : {0}".format(SETUP_DIR))
    return tmpl

current_template = parse_template(sys.argv)

def install_requires():
    return current_template.install_requires()

def build_requires():
    return current_template.build_requires()

def get_dirs(base):
    return [x for x in glob.iglob(os.path.join( base, '*')) if os.path.isdir(x) ]

def data_files_config(target, source, pattern):
    ret = list()
    tup = list()
    tup.append(target)
    tup.append(glob.glob(os.path.join(source,pattern)))
    ret.append(tup)
    dirs = get_dirs(source)
    if len(dirs):
        for d in dirs:
            rd = d.replace(source+os.sep, "", 1)
            ret.extend(data_files_config(os.path.join(target,rd), \
                os.path.join(source,rd), pattern))
    return ret


class build_openzwave(setuptools.Command):
    description = 'download and build openzwave'

    user_options = [
        ('openzwave-dir=', None,
         'the source directory where openzwave sources should be stored'),
        ('flavor=', None,
         'the flavor of python_openzwave to install'),
    ]

    def initialize_options(self):
        self.openzwave_dir = None
        self.flavor = None

    def finalize_options(self):
        if self.openzwave_dir is None:
            if getattr(self, 'develop', False) or not getattr(self, 'install', False):
                self.openzwave_dir = current_template.openzwave
            else:
                build = self.distribution.get_command_obj('build')
                build.ensure_finalized()
                self.openzwave_dir = os.path.join(build.build_lib, current_template.openzwave)
        if sys.platform.startswith('win'):
            build_clib = self.distribution.get_command_obj('build_clib')
            build_clib.ensure_finalized()
        self.flavor = current_template.flavor

    def run(self):
        current_template.check_minimal_config()
        current_template.get_openzwave()

        if sys.platform.startswith('win'):
            if 'bdist_wheel' not in sys.argv:
                current_template.clean()

        else:
            current_template.clean()

        self.run_command('build_clib')
        current_template.build()
        if current_template.install_openzwave_so:
            current_template.install_so()


class build(_build):
    sub_commands = [('build_openzwave', None)] + _build.sub_commands


from setuptools.command.bdist_egg import bdist_egg as _bdist_egg


class bdist_egg(_bdist_egg):

    def run(self):
        build_openzwave = self.distribution.get_command_obj('build_openzwave')
        build_openzwave.develop = True
        self.run_command('build_openzwave')
        _bdist_egg.run(self)


class bdist_wheel(Command):
    description = 'Create a wheel.'

    user_options = [
        ('bdist-dir=', None, 'temporary install path'),
    ]

    def initialize_options(self):
        options = self.distribution.get_option_dict('bdist_wheel')
        self.bdist_dir = options['bdist_dir'][1]

    def finalize_options(self):
        install_options = dict(install_lib=('setup script', self.bdist_dir))
        self.distribution.command_options['install'] = install_options

    def run(self):
        if not os.path.exists(self.bdist_dir):
            os.makedirs(self.bdist_dir)

        self.run_command('install')

        log.info('Collecting wheel data.')

        wheel_dir = os.path.join(self.bdist_dir, 'wheel')

        if not os.path.exists(wheel_dir):
            os.mkdir(wheel_dir)

        for f in os.listdir(self.bdist_dir):
            if f.startswith('python_openzwave'):
                tag = f[:-4].split('-', 2)[-1]
                install_dir = os.path.join(self.bdist_dir, f)
                dist_info = os.path.join(
                    wheel_dir,
                    f.replace(tag, '')[:-5] + '.dist-info'
                )
                break
        else:
            raise RuntimeError(
                'Unable to locate python-openzwave temporary installation.'
            )

        tag_ver = tag.split('-')[0]
        new_tag_ver = tag_ver.replace('py', 'cp')
        new_tag_ver = new_tag_ver + '-' + new_tag_ver + 'm'
        new_tag_ver = new_tag_ver.replace('.', '')

        dist_directory = os.path.join(self.bdist_dir, '..', '..', 'dist')
        dist_directory = os.path.abspath(dist_directory)
        if not os.path.exists(dist_directory):
            os.mkdir(dist_directory)

        log.info('Creating wheel dist-info.')

        license_ = os.path.join(self.bdist_dir, '..', '..', 'COPYRIGHT.txt')
        pkg_info = os.path.join(install_dir, 'EGG-INFO', 'PKG-INFO')
        requires = os.path.join(install_dir, 'EGG-INFO', 'requires.txt')
        top_level = os.path.join(install_dir, 'EGG-INFO', 'top_level.txt')
        entry_points = os.path.join(install_dir, 'EGG-INFO', 'entry_points.txt')

        wheel = (
            'Wheel-Version: 1.0\n'
            'Generator: bdist_wheel (0.33.1)\n'
            'Root-Is-Purelib: false\n'
            'Tag: '
        )

        wheel += new_tag_ver

        with open(pkg_info, 'r') as f:
            pkg_info = f.read()

        with open(requires, 'r') as f:
            requires = f.read()

        with open(top_level, 'r') as f:
            top_level = f.read()

        with open(entry_points, 'r') as f:
            entry_points = f.read()

        with open(license_, 'r') as f:
            license_ = f.read()

        pkg_info = pkg_info.rstrip()

        requires_dist = None
        for line in requires.split('\n'):
            if not line.strip():
                continue

            if line.startswith('['):
                requires_dist = line[2:-1]
            else:
                for oper in ('>=', '<=', '=='):
                    if oper in line:
                        line, ver = line.split(oper)
                        line += ' (' + oper + ver + ')'
                        break

                pkg_info += '\nRequires-Dist: ' + line
                if requires_dist is not None:
                    pkg_info += '; (' + requires_dist + ')'
                    requires_dist = None

        beg, description = pkg_info.split('Description: ')
        description, end = description.split('\n', 1)
        metadata = beg + end
        metadata += '\n\n' + description

        import hashlib
        import base64

        record = []

        def get_file_hash(path):
            dirs = []

            for src in os.listdir(path):
                src = os.path.join(path, src)

                if 'EGG-INFO' in src:
                    continue
                if '__pycache__' in src:
                    continue

                if src.endswith('.pyc'):
                    continue
                if src.endswith('.pyo'):
                    continue

                if os.path.isdir(src):
                    dirs += [src]
                    continue

                sha256_hash = hashlib.sha256()
                # Read and update hash string value in blocks of 4K
                byte_count = 0
                pth = src.replace(install_dir, '')[1:]
                dst = os.path.join(wheel_dir, pth)

                dst_dir = os.path.split(dst)[0]

                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)

                dst = open(dst, 'wb')

                with open(src, "rb") as sha_f:

                    for byte_block in iter(lambda: sha_f.read(4096), b""):
                        sha256_hash.update(byte_block)
                        byte_count += len(byte_block)
                        dst.write(byte_block)

                add_sha(src, byte_count, sha256_hash.hexdigest())

                dst.close()

            for d in dirs:
                get_file_hash(d)

        def add_sha(src, byte_count, hex_digest):
            if PY3:
                hex_digest = hex_digest.encode()

            sha_256 = base64.urlsafe_b64encode(hex_digest)

            if PY3:
                sha_256 = sha_256.decode()

            record.append(
                '{path},sha256={sha_256},{byte_count}'.format(
                    path=src.replace(install_dir, '')[1:],
                    sha_256=sha_256.replace('=', ''),
                    byte_count=byte_count
                )
            )

        log.info('Hashing wheel files.')

        get_file_hash(install_dir)

        if not os.path.exists(dist_info):
            os.mkdir(dist_info)

        with open(os.path.join(dist_info, 'top_level.txt'), 'w') as f:
            f.write(top_level)

        with open(os.path.join(dist_info, 'entry_points.txt'), 'w') as f:
            f.write(entry_points)

        with open(os.path.join(dist_info, 'LICENSE'), 'w') as f:
            f.write(license_)

        with open(os.path.join(dist_info, 'METADATA'), 'w') as f:
            f.write(metadata)

        with open(os.path.join(dist_info, 'WHEEL'), 'w') as f:
            f.write(wheel)

        if PY3:
            top_level = top_level.encode()
            entry_points = entry_points.encode()
            license_ = license_.encode()
            metadata = metadata.encode()
            wheel = wheel.encode()

        add_sha(
            os.path.join(dist_info, 'top_level.txt').replace(wheel_dir, '')[1:],
            len(top_level),
            hashlib.sha256(top_level).hexdigest()
        )
        add_sha(
            os.path.join(dist_info, 'entry_points.txt').replace(wheel_dir, '')[1:],
            len(entry_points),
            hashlib.sha256(entry_points).hexdigest()
        )
        add_sha(
            os.path.join(dist_info, 'LICENSE').replace(wheel_dir, '')[1:],
            len(license_),
            hashlib.sha256(license_).hexdigest()
        )
        add_sha(
            os.path.join(dist_info, 'METADATA').replace(wheel_dir, '')[1:],
            len(metadata),
            hashlib.sha256(metadata).hexdigest()
        )
        add_sha(
            os.path.join(dist_info, 'WHEEL').replace(wheel_dir, '')[1:],
            len(wheel),
            hashlib.sha256(wheel).hexdigest()
        )

        record.append(
            os.path.join(dist_info, 'RECORD').replace(wheel_dir, '')[1:] +
            ',,'
        )

        with open(os.path.join(dist_info, 'RECORD'), 'w') as f:
            f.write('\n'.join(record))

        import zipfile

        for wheel_file in os.listdir(dist_directory):
            if (
                wheel_file.startswith('python_openzwave') and
                wheel_file.endswith('egg')
            ):
                break
        else:
            raise RuntimeError(
                'Unable to locate egg file to create wheel from.'
            )

        wheel_file = wheel_file.replace(tag.split('-', 1)[0], new_tag_ver)[:-3]
        wheel_file = os.path.join(dist_directory, wheel_file + 'whl')

        log.info('Writing wheel file: ' + wheel_file)

        cwd = os.getcwd()
        os.chdir(wheel_dir)

        zip_file = zipfile.ZipFile(wheel_file, 'w', zipfile.ZIP_DEFLATED)
        for root, dirs, files in os.walk(wheel_dir):
            for f in files:
                f = os.path.relpath(os.path.join(root, f))
                zip_file.write(f)

        zip_file.close()

        os.chdir(cwd)


class clean(_clean):
    def run(self):
        if getattr(self, 'all', False):
            current_template.clean_all()
        else:
            current_template.clean()
        _clean.run(self)


class develop(_develop):
    description = 'Develop python_openzwave'

    user_options = _develop.user_options + [
        ('flavor=', None, 'the flavor of python_openzwave to install'),
    ]

    def initialize_options(self):
        self.flavor = None
        return _develop.initialize_options(self)

    def finalize_options(self):
        if self.flavor is None:
            self.flavor = current_template.flavor
        log.info('flavor {0}'.format(self.flavor))
        return _develop.finalize_options(self)

    def run(self):
        #In case of --uninstall, it will build openzwave to remove it ... stupid.
        #In develop mode, build is done by the makefile
        #~ build_openzwave = self.distribution.get_command_obj('build_openzwave')
        #~ build_openzwave.develop = True
        #~ self.run_command('build_openzwave')
        _develop.run(self)


class install(_install):
    description = 'Install python_openzwave'

    user_options = _install.user_options + [
        ('flavor=', None, 'the flavor of python_openzwave to install'),
    ]

    def initialize_options(self):
        self.flavor = None
        return _install.initialize_options(self)

    def finalize_options(self):
        if self.flavor is None:
            self.flavor = current_template.flavor
        log.info('flavor {0}'.format(self.flavor))
        return _install.finalize_options(self)

    def run(self):
        # here we are going to check to see if python_openzwave is already
        # installed.

        # if it is already installed we want to backup the config files so we
        # can iterate over them and check them against the ones being
        # installed. we do not want to remove any config files that may have
        # been updatedby the user. or any they may have created.

        from pkg_resources import resource_filename
        import tempfile

        python_path = os.path.dirname(sys.executable)

        try:
            config_path = resource_filename(
                'python_openzwave.ozw_config',
                '__init__.py'
            )
            config_path = os.path.dirname(config_path)
        except:
            temp_dir = None
        else:
            temp_dir = os.path.join(tempfile.mkdtemp(), 'config')
            shutil.copytree(config_path, temp_dir)

        build_ozw = self.distribution.get_command_obj('build_openzwave')
        build_ozw.develop = True

        self.run_command('build_openzwave')

        easy_install = self.distribution.get_command_class('easy_install')

        cmd = easy_install(
            self.distribution, args="x", root=self.root, record=self.record,
        )
        cmd.ensure_finalized()  # finalize before bdist_egg munges install cmd
        cmd.always_copy_from = '.'  # make sure local-dir eggs get installed

        # pick up setup-dir .egg files only: no .egg-info
        cmd.package_index.scan(glob.glob('*.egg'))

        self.run_command('bdist_egg')
        args = [self.distribution.get_command_obj('bdist_egg').egg_output]

        if setuptools.bootstrap_install_from:
            # Bootstrap self-installation of setuptools
            args.insert(0, setuptools.bootstrap_install_from)

        cmd.args = args

        cmd.run()
        setuptools.bootstrap_install_from = None

        install_path = cmd.local_index['python-openzwave'][0].location
        dst = os.path.join(install_path, 'python_openzwave', "ozw_config")

        if temp_dir is not None:
            shutil.rmtree(dst)
            shutil.copytree(temp_dir, dst)
            shutil.rmtree(temp_dir)

        if current_template.copy_openzwave_config:

            def get_newer_config_file(old, new):
                new_revision = new.split(b'Revision="', 1)[-1]
                old_revision = old.split(b'Revision="', 1)[-1]

                new_revision = new_revision.split(b'"', 1)[0]
                old_revision = old_revision.split(b'"', 1)[0]

                if new_revision.isdigit() and old_revision.isdigit():
                    if int(new_revision) > int(old_revision):
                        return new
                    elif int(new_revision) < int(old_revision):
                        return old

                if len(new) > len(old):
                    return new

                return old

            src = os.path.join(current_template.openzwave, 'config')

            log.info(
                "Install ozw_config for template {0}".format(current_template)
            )

            def check_config(root):
                head = root
                tail = []
                while head and head != src:
                    head, t = os.path.split(head)
                    tail.insert(0, t)

                if tail:
                    new_root = os.path.join(dst, *tail)
                else:
                    new_root = dst

                files = os.listdir(root)

                for f in files:
                    old_f = os.path.join(new_root, f)
                    new_f = os.path.join(root, f)

                    if os.path.isdir(new_f):
                        if not os.path.exists(old_f):
                            log.info(
                                'Creating directory: ' +
                                old_f.replace(python_path, '')
                            )
                            os.mkdir(old_f)

                        check_config(new_f)
                    else:
                        with open(new_f, 'rb') as tmp_f:
                            new_data = tmp_f.read()

                        if new_f.endswith('.xml') and os.path.isfile(old_f):
                            with open(old_f, 'rb') as tmp_f:
                                old_data = tmp_f.read()

                            if old_data == new_data:
                                log.info(
                                    'No update needed: ' +
                                    old_f.replace(python_path, '')
                                )
                                continue

                            data = get_newer_config_file(
                                old_data,
                                new_data
                            )

                            if data != old_data:
                                log.info(
                                    'Copying file: ' +
                                    new_f +
                                    ' ---> ' +
                                    old_f.replace(python_path, '')
                                )
                            else:
                                log.info(
                                    'Keeping existing file: ' +
                                    old_f.replace(python_path, '')
                                )
                                continue
                        else:
                            log.info(
                                'Copying file: ' +
                                new_f +
                                ' ---> ' +
                                old_f.replace(python_path, '')
                            )

                        with open(old_f, 'wb') as tmp_f:
                            tmp_f.write(new_data)

            check_config(src)

        else:
            log.info(
                "Don't install ozw_config for template {0}".format(
                    current_template
                )
            )

        log.info('\nFinished!\n')

