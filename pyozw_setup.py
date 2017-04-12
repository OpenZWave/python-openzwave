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
from os import name as os_name
import os, sys
import re
import shutil
import setuptools
from setuptools import setup, find_packages
from distutils.extension import Extension
from distutils import log
from distutils.command.install import install as _install
from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
from setuptools.command.develop import develop as _develop
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
import time
from platform import system as platform_system
import glob

from pyozw_version import pyozw_version

LOCAL_OPENZWAVE = 'openzwave'

SETUP_DIR = os.path.dirname(os.path.abspath(__file__))

def get_default_exts ():
    exts = { "name": "libopenzwave",
         "sources": [ ],
         "include_dirs": [ ],
         "define_macros": [ ( 'PY_LIB_VERSION', pyozw_version ) ],
         "libraries": [ ],
         "extra_objects": [ ],
         "extra_compile_args": [ ],
         "extra_link_args": [ ],
         "language": "c++"
       }
    return exts

def cython_context():
    try:
        from Cython.Distutils import build_ext
    except ImportError:
        return None
    exts = get_default_exts()
    exts['define_macros'] += [('PY_SSIZE_T_CLEAN',1)]
    exts['sources'] = ["src-lib/libopenzwave/libopenzwave.pyx"]
    return exts

def cpp_context():
    try:
        from distutils.command.build_ext import build_ext
    except ImportError:
        return None
    exts = get_default_exts()
    exts['define_macros'] += [('PY_SSIZE_T_CLEAN',1)]
    exts['sources'] = ["openzwave-embed/open-zwave-master/python-openzwave/src-lib/libopenzwave/libopenzwave.cpp"]
    exts["include_dirs"] += [ "src-lib/libopenzwave/" ]
    return exts

def pybind_context():
    exts = get_default_exts()
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

def system_context(ctx, openzwave=None, static=False):
    #System specific section
    if static:
        ctx['include_dirs'] += [ 
            "{0}/cpp/src".format(openzwave), 
            "{0}/cpp/src/value_classes".format(openzwave), 
            "{0}/cpp/src/platform".format(openzwave) ]
    if sys.platform == "win32":
        ctx['libraries'] += [ "setupapi", "msvcrt", "ws2_32", "dnsapi" ]

        if static:
            ctx['extra_objects'] = [ "{0}/cpp/build/windows/vs2010/Release/openzwave.lib".format(openzwave) ]
            ctx['include_dirs'] += [ "{0}/cpp/build/windows".format(openzwave) ]
        else:
            import pyozw_pkgconfig
            ctx['libraries'] += [ "openzwave" ]
            extra = pyozw_pkgconfig.cflags('libopenzwave')
            for ssubstitute in ['/', '/value_classes/', '/platform/', '/windows/']:
                ctx['extra_compile_args'] += [ extra.replace('//', ssubstitute) ]

    elif sys.platform == "darwin":
        ctx['extra_link_args'] += [ "-framework", "CoreFoundation", "-framework", "IOKit" ]
        ctx['extra_compile_args'] += [ "-stdlib=libc++", "-mmacosx-version-min=10.7" ]

        if static:
            ctx['extra_objects'] = [ "{0}/libopenzwave.a".format(openzwave) ]
            ctx['include_dirs'] += [ "{0}/cpp/build/mac".format(openzwave) ]
        else:
            import pyozw_pkgconfig
            ctx['libraries'] += [ "openzwave" ]
            extra = pyozw_pkgconfig.cflags('libopenzwave')
            for ssubstitute in ['/', '/value_classes/', '/platform/', '/mac/']:
                ctx['extra_compile_args'] += [ extra.replace('//', ssubstitute) ]
            
    elif sys.platform == "freebsd":
        if static:
            ctx['libraries'] += [ "usb", "stdc++",'resolv' ]
            ctx['extra_objects'] = [ "{0}/libopenzwave.a".format(openzwave) ]
            ctx['include_dirs'] += [ "{0}/cpp/build/linux".format(openzwave) ]
        else:
            import pyozw_pkgconfig
            ctx['libraries'] += [ "openzwave" ]
            extra = pyozw_pkgconfig.cflags('libopenzwave')
            for ssubstitute in ['/', '/value_classes/', '/platform/', '/linux/']:
                ctx['extra_compile_args'] += [ extra.replace('//', ssubstitute) ]
 
    elif sys.platform[:5] == "linux":
        if static:
            ctx['libraries'] += [ "udev", "stdc++",'resolv' ]
            ctx['extra_objects'] = [ "{0}/libopenzwave.a".format(openzwave) ]
            ctx['include_dirs'] += [ "{0}/cpp/build/linux".format(openzwave) ]
        else:
            import pyozw_pkgconfig
            ctx['libraries'] += [ "openzwave" ]
            extra = pyozw_pkgconfig.cflags('libopenzwave')
            for ssubstitute in ['/', '/value_classes/', '/platform/', '/linux/']:
                ctx['extra_compile_args'] += [ extra.replace('//', ssubstitute) ]
    else:
        # Unknown systemm
        raise RuntimeError("Can't detect plateform")

    return ctx

class Template(object):
    
    def __init__(self, openzwave=None, cleanopzw=False):
        self.openzwave = openzwave
        self._ctx = None
        self.cleanopzw = cleanopzw
   
    @property
    def ctx(self):
        if self._ctx is None:
            self._ctx = self.get_context()
        return self._ctx

    @property
    def build_ext(self):
        from Cython.Distutils import build_ext as _build_ext
        return _build_ext
   
    @property
    def copy_openzwave_config(self):
        return True

    @property
    def install_openzwave_so(self):
        return False

    def install_requires(self):
        return ['cython']
        
    def build(self):
        if len(self.ctx['extra_objects']) == 1 and os.path.isfile(self.ctx['extra_objects'][0]):
            log.info("Use cached build of openzwave")
            return True
        log.info("Build openzwave ... be patient ...")
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

        if sys.platform == "win32":
            proc = Popen('make', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform == "darwin":
            proc = Popen('make', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform == "freebsd":
            proc = Popen('make', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform[:5] == "linux":
            proc = Popen('make', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
        else:
            # Unknown systemm
            raise RuntimeError("Can't detect plateform")

        Thread(target=stream_watcher, name='stdout-watcher',
                args=('STDOUT', proc.stdout)).start()
        Thread(target=stream_watcher, name='stderr-watcher',
                args=('STDERR', proc.stderr)).start()

        printer = Thread(target=printer, name='printer')
        printer.start()
        while printer.is_alive():
            time.sleep(1)
        printer.join()
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

        if sys.platform == "win32":
            proc = Popen(['make', 'install'], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform == "darwin":
            proc = Popen(['make', 'install'], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform == "freebsd":
            proc = Popen(['make', 'install'], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform[:5] == "linux":
            proc = Popen(['make', 'install'], stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
        else:
            # Unknown systemm
            raise RuntimeError("Can't detect plateform")

        Thread(target=stream_watcher, name='stdout-watcher',
                args=('STDOUT', proc.stdout)).start()
        Thread(target=stream_watcher, name='stderr-watcher',
                args=('STDERR', proc.stderr)).start()

        printer = Thread(target=printer, name='printer')
        printer.start()
        while printer.is_alive():
            time.sleep(1)
        printer.join()
        return True

    def clean(self):
        #Build openzwave
        try:
            if not os.path.isfile(self.openzwave):
                return True
        except TypeError:
            return True
        log.info("Clean openzwave ... be patient ...")
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

        if sys.platform == "win32":
            proc = Popen('make clean', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform == "darwin":
            proc = Popen('make clean', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform == "freebsd clean":
            proc = Popen('make', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
                
        elif sys.platform[:5] == "linux":
            proc = Popen('make clean', stdout=PIPE, stderr=PIPE, cwd='{0}'.format(self.openzwave))
        else:
            # Unknown systemm
            raise RuntimeError("Can't detect plateform")

        Thread(target=stream_watcher, name='stdout-watcher',
                args=('STDOUT', proc.stdout)).start()
        Thread(target=stream_watcher, name='stderr-watcher',
                args=('STDERR', proc.stderr)).start()

        printer = Thread(target=printer, name='printer')
        printer.start()
        while printer.is_alive():
            time.sleep(1)
        printer.join()
        return True

    def clean_all(self):
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

    def install_minimal_dependencies(self):
        import pip
        for pyreq in install_requires():
            try:
                log.info("Install minimal dependencies {0}".format(pyreq))
                pip.main(['install', pyreq])
            except Exception:
                log.error("Fail to install minimal dependencies {0}".format(pyreq))
        
    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        #Get openzwave
        """download an archive to a specific location"""
        dest,tail = os.path.split(self.openzwave)
        dest_file = os.path.join(dest, 'open-zwave-master.zip')
        if os.path.exists(self.openzwave):
            if not self.cleanopzw:
                log.info("Already have directory %s. Use it. Use --cleanopzw to clean it.", self.openzwave)
                return self.openzwave
            else:
                log.info("Already have directory %s but remove and clean it as asked", self.openzwave)
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
        
class DevTemplate(Template):
    def __init__(self, openzwave=None, cleanopzw=False):
        Template.__init__(self, openzwave='openzwave', cleanopzw=cleanopzw)

    def get_context(self):
        opzw_dir = LOCAL_OPENZWAVE
        if LOCAL_OPENZWAVE is None:
            return None
        if not os.path.isdir(opzw_dir):
            log.error("Can't find {0}".format(opzw_dir))
            return None
        self.openzwave = opzw_dir
        ctx = cython_context()
        if ctx is None:
            log.error("Can't find cython")
            return None
        ctx = system_context(ctx, openzwave=opzw_dir, static=True)
        return ctx

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        return True

class GitTemplate(Template):
    def __init__(self, openzwave=None, cleanopzw=False):
        Template.__init__(self, openzwave=os.path.join("openzwave-git", 'open-zwave-master'), cleanopzw=cleanopzw)

    def get_context(self):
        ctx = cython_context()
        if ctx is None:
            log.error("Can't find cython")
            return None
        ctx = system_context(ctx, openzwave=self.openzwave, static=True)
        return ctx

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        return Template.get_openzwave(self, url)

    def clean_all(self):
        ret = self.clean()
        dest,tail = os.path.split(os.path.abspath(self.openzwave))
        if tail == "openzwave-git":
            try:
                log.info('Try to remove {0}'.format(self.openzwave))
                if os.path.isdir(os.path.abspath(self.openzwave)):
                    shutil.rmtree(os.path.abspath(self.openzwave))
            except Exception:
                pass
        elif tail == 'open-zwave-master':
            try:
                log.info('Try to remove {0}'.format(dest))
                if os.path.isdir(os.path.abspath(dest)):
                    shutil.rmtree(os.path.abspath(dest))
            except Exception:
                pass
        return ret

class GitSharedTemplate(GitTemplate):
    
    def get_context(self):
        ctx = cython_context()
        if ctx is None:
            log.error("Can't find cython")
            return None
        ctx = system_context(ctx, openzwave=self.openzwave, static=False)
        return ctx

    @property
    def install_openzwave_so(self):
        return True

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        return Template.get_openzwave(self, url)

    def clean_all(self):
        ret = GitTemplate.clean(self)
        #We should remove headers, so modules and configuration files
        for path in ['/usr/local/etc/openzwave', '/usr/local/include/openzwave', '/usr/local/share/doc/openzwave']:
            try:
                log.info('Try to remove {0}'.format('/usr/local/etc/openzwave'))
                shutil.rmtree(os.path.abspath(self.openzwave))
            except Exception:
                pass
        return ret

class EmbedTemplate(Template):
    def __init__(self, openzwave=None, cleanopzw=False):
        Template.__init__(self, openzwave=os.path.join("openzwave-embed", 'open-zwave-master'), cleanopzw=cleanopzw)

    @property
    def build_ext(self):
        from distutils.command.build_ext import build_ext as _build_ext
        return _build_ext

    def get_context(self):
        ctx = cpp_context()
        ctx = system_context(ctx, openzwave=self.openzwave, static=True)
        return ctx

    def install_requires(self):
        return []

    def get_openzwave(self, url='https://raw.githubusercontent.com/OpenZWave/python-openzwave/master/archives/open-zwave-master-{0}.zip'.format(pyozw_version)):
        return Template.get_openzwave(self, url)

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
        dest,tail = os.path.split(os.path.abspath(self.openzwave))
        if tail == "openzwave-embed":
            try:
                log.info('Try to remove {0}'.format(self.openzwave))
                shutil.rmtree(os.path.abspath(self.openzwave))
            except Exception:
                pass
        elif tail == 'open-zwave-master':
            try:
                log.info('Try to remove {0}'.format(dest))
                shutil.rmtree(os.path.abspath(dest))
            except Exception:
                pass
        return ret
        
class SharedTemplate(Template):
    def __init__(self, openzwave=None, cleanopzw=False):
        Template.__init__(self, openzwave=openzwave, cleanopzw=cleanopzw)

    def get_context(self):
        ctx = cython_context()
        if ctx is None:
            log.error("Can't find cython")
            return None
        ctx = system_context(ctx, static=False)
        return ctx

    def build(self):
        return True

    @property
    def copy_openzwave_config(self):
        return False

    def get_openzwave(self, url='https://codeload.github.com/OpenZWave/open-zwave/zip/master'):
        return True

def parse_template(sysargv):
    tmpl = EmbedTemplate()
    if '--dev' in sysargv:
        index = sysargv.index('--dev')
        sysargv.pop(index)
        tmpl =  DevTemplate()
    elif '--git' in sysargv:
        index = sysargv.index('--git')
        sysargv.pop(index)
        tmpl =  GitTemplate()
    elif '--git_shared' in sysargv:
        index = sysargv.index('--git_shared')
        sysargv.pop(index)
        tmpl =  GitSharedTemplate()
    elif '--embed' in sysargv:
        index = sysargv.index('--embed')
        sysargv.pop(index)
        tmpl =  EmbedTemplate()
    elif '--shared' in sysargv:
        index = sysargv.index('--shared')
        sysargv.pop(index)
        tmpl =  SharedTemplate()
    if '--cleanopzw' in sysargv:
        index = sysargv.index('--cleanopzw')
        sysargv.pop(index)
        tmpl.cleanopzw = True
    return tmpl
    
current_template = parse_template(sys.argv)

def install_requires():
    pkgs = ['six']
    if (sys.version_info > (3, 0)):
         pkgs.append('PyDispatcher>=2.0.5')
    else:
         pkgs.append('Louie>=1.1')
    pkgs += current_template.install_requires()
    #~ print('Found install_requires {0}'.format(pkgs))
    return pkgs

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

class bdist_egg(_bdist_egg):
    def run(self):
        self.run_command('build_openzwave')
        _bdist_egg.run(self)

class build_openzwave(setuptools.Command):
    description = 'download an build openzwave'
    
    user_options = [
        ('openzwave-dir=', None,
         'the source directory where openzwave sources should be stored'),
    ]
    
    def initialize_options(self):
        self.openzwave_dir = None
    
    def finalize_options(self):
        if self.openzwave_dir is None:
            if getattr(self, 'develop', False) or not getattr(self, 'install', False):
                self.openzwave_dir = current_template.openzwave
            else:
                build = self.distribution.get_command_obj('build')
                build.ensure_finalized()
                self.openzwave_dir = os.path.join(build.build_lib, current_template.openzwave)
    
    def run(self):
        current_template.install_minimal_dependencies()
        current_template.get_openzwave()
        current_template.build()
        if current_template.install_openzwave_so:
            current_template.install_so()

class openzwave_config(setuptools.Command):
    description = 'Install config files from openzwave'
    
    user_options = [
        ('install-dir=', None,
         'the installation directory where openzwave configuration should be stored'),
    ]
    
    def initialize_options(self):
        self.install_dir = None
    
    def finalize_options(self):
        if self.install_dir is None:
            install = self.distribution.get_command_obj('install')
            install.ensure_finalized()
            self.install_dir = install.install_lib
    
    def run(self):
        if self.install_dir is None:
            log.warning("Can't install ozw_config to None")
            return
        if not current_template.copy_openzwave_config:
            log.info("Don't install ozw_config for template {0}".format(current_template))
            return
        dest = os.path.join(self.install_dir, 'python_openzwave', "ozw_config")
        if not os.path.isdir(dest):
            os.makedirs(dest)
        self.copy_tree(os.path.join(current_template.openzwave,'config'), dest)
        
class build(_build):
    sub_commands = [('build_openzwave', None)] + _build.sub_commands

class bdist_wheel(_bdist_wheel):
    def run(self):
        self.run_command('build_openzwave')
        #~ self.run_command('openzwave_config')
        _bdist_wheel.run(self)

class clean(_clean):
    def run(self):
        if getattr(self, 'all', False):
            current_template.clean_all()
        else:
            current_template.clean()
        _clean.run(self)      

class develop(_develop):
    def run(self):
        build_openzwave = self.distribution.get_command_obj('build_openzwave')
        build_openzwave.develop = True
        self.run_command('build_openzwave')
        _develop.run(self)

class install(_install):
    def run(self):
        build_openzwave = self.distribution.get_command_obj('build_openzwave')
        build_openzwave.develop = True
        self.run_command('build_openzwave')
        self.run_command('openzwave_config')
        _install.run(self)

