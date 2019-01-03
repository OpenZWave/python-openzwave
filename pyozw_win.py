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
import sys
import os
import shutil
import threading
import subprocess
import pyozw_msvc
import pyozw_common
import pyozw_version

# this is some tailored code to detect an appveyor build. if it is
# then the environment is set to only use a specific compiler version.
if 'PYTHON_VERSION' in os.environ and 'PYTHON_ARCH' in os.environ:
    python_version = os.environ['PYTHON_VERSION']

    if python_version == '3.6.x':
        environment = pyozw_msvc.Environment(strict_visual_c_version=14.0)
    elif python_version == '3.4.x':
        environment = pyozw_msvc.Environment(strict_visual_c_version=10.0)
    elif python_version == '2.7.x':
        environment = pyozw_msvc.Environment(strict_visual_c_version=10.0)
    else:
        environment = pyozw_msvc.Environment(minimum_visual_c_version=10.0)
else:
    environment = pyozw_msvc.Environment(minimum_visual_c_version=10.0)


VERSION_COMMAND = 'GIT-VS-VERSION-GEN.bat --quiet . winversion.cpp'


# When running a build on linux the makefile handles the creation of the
# openzwave version file. if you build openzwave using visual studio the same
# is done. Since we are letting distutils handle the compiling of openzwave
# we need to create that version file ourselves.
# that is what this function does.

def build_version_file(openzwave):
    version_file = openzwave + "\\cpp\\build\\windows\\winversion.cpp"
    if os.path.exists(version_file):
        os.remove(version_file)

    try:
        cwd = os.path.dirname(__file__)
        if not cwd:
            cwd = os.getcwd()
    except WindowsError:
        cwd = os.getcwd()

    cwd = os.path.abspath(cwd)
    os.chdir(os.path.abspath(openzwave + '\\cpp\\build\\windows'))
    p = subprocess.Popen(VERSION_COMMAND)
    p.communicate()
    os.chdir(cwd)


class Extension(pyozw_common.Extension):
    def __init__(
        self,
        openzwave,
        flavor,
        static,
        backend
    ):
        for key, value in environment.build_environment.items():
            os.environ[key] = value

        extra_objects = []
        define_macros = []
        sources = []
        include_dirs = ['src-lib\\libopenzwave']

        libraries = []
        extra_compile_args = [
            # Enables function-level linking.
            '/Gy',
            # Creates fast code.
            '/O2',
            # Uses the __cdecl calling convention (x86 only).
            '/Gd',
            # Omits frame pointer (x86 only).
            '/Oy',
            # Generates intrinsic functions.
            '/Oi',
            # Specify floating-point behavior.
            '/fp:precise',
            # Specifies standard behavior
            '/Zc:wchar_t',
            # Specifies standard behavior
            '/Zc:forScope',
            # I cannot remember what this does. I do know it does get rid of
            # a compiler warning
            '/EHsc',
            # compiler warnings to ignore
            '/wd4996',
            '/wd4244',
            '/wd4005',
            '/wd4800',
            '/wd4351',
            '/wd4273'
        ]

        if environment.visual_c.version > 10.0:
            # these compiler flags are not valid on
            # Visual C++ version 10.0 and older

            extra_compile_args += [
                # Forces writes to the program database (PDB) file to be
                # serialized through MSPDBSRV.EXE.
                '/FS',
                # Specifies standard behavior
                '/Zc:inline'
            ]

        if pyozw_common.DEBUG_BUILD:
            define_macros += [('_DEBUG', 1)]
            libraries += ["setupapi", "msvcrtd", "ws2_32", "dnsapi"]
        else:
            libraries += ["setupapi", "msvcrt", "ws2_32", "dnsapi"]

        libraries += [environment.python.dependency.split('.')[0]]

        cpp_path = os.path.join(openzwave, 'cpp')
        src_path = os.path.join(cpp_path, 'src')
        if static:
            build_path = os.path.join(openzwave, 'build')

            # this is a really goofy thing to have to do. But distutils will
            # pitch a fit if we try to run the linker without a PyInit
            # expression. it does absolutely nothing. Decoration I guess.

            extra_objects += [
                os.path.join(build_path + '\\lib_build', 'OpenZWave.lib')
            ]

            include_dirs += [
                build_path,
                os.path.join(cpp_path, 'build', 'windows'),

            ]

        else:
            libraries += ["OpenZWave"]
            extra_compile_args += [
                src_path,
                os.path.join(src_path, 'value_classes'),
                os.path.join(src_path, 'platform'),
            ]

        pyozw_common.Extension.__init__(
            self,
            openzwave,
            flavor,
            static,
            backend,
            extra_objects=extra_objects,
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            libraries=libraries,
            extra_compile_args=extra_compile_args
        )


class Library(pyozw_common.Library):

    def __init__(self, openzwave):

        build_path = self.build_path = os.path.join(openzwave, 'build')

        build_version_file(openzwave)
        pyozw_common.build_dll_main(openzwave)

        sources = pyozw_common.get_sources(
            os.path.abspath(os.path.join(openzwave, 'cpp')),
            ignore=['unix', 'winrt', 'mac', 'linux', 'examples', 'libusb']
        )

        define_macros = [
            ('WIN32', 1),
            ('_MBCS', 1),
            ('_LIB', 1),
            ('USE_HID', 1),
            ('_MT', 1),
            ('_DLL', 1),
            ('OPENZWAVE_MAKEDLL', 1)
        ]

        if pyozw_common.DEBUG_BUILD:
            define_macros += [('DEBUG', 1)]
        else:
            define_macros += [('NDEBUG', 1)]

        if environment.platform == 'x64':
            define_macros += [('WIN64', 1)]

        library_dirs = [
            os.path.join(os.path.dirname(sys.executable), 'libs')
        ]

        libraries = ['setupapi', pyozw_common.PYTHON_LIB]
        extra_compile_args = [
            # Enables function-level linking.
            '/Gy',
            # Creates fast code.
            '/O2',
            # Uses the __cdecl calling convention (x86 only).
            '/Gd',
            # Omits frame pointer (x86 only).
            '/Oy',
            # Generates intrinsic functions.
            '/Oi',
            # Renames program database file.
            '/Fd"{0}\\lib_build\\OpenZWave.pdb"'.format(build_path),
            # Specify floating-point behavior.
            '/fp:precise',
            # Specifies standard behavior
            '/Zc:wchar_t',
            # Specifies standard behavior
            '/Zc:forScope',
            # I cannot remember what this does. I do know it does get rid of
            # a compiler warning
            '/EHsc',
            # compiler warnings to ignore
            '/wd4251',
            '/wd4244',
            '/wd4101',
            '/wd4267',
            '/wd4996',
            '/wd4351'
        ]

        if environment.visual_c.version > 10.0:
            # these compiler flags are not valid on
            # Visual C++ version 10.0 and older

            extra_compile_args += [
                # Forces writes to the program database (PDB) file to be
                # serialized through MSPDBSRV.EXE.
                '/FS',
                # Specifies standard behavior
                '/Zc:inline'
            ]

        # not used but here for completeness.
        extra_link_args = [
            '/IGNORE:4098',
            '/MACHINE:' + environment.platform.upper(),
            '/NOLOGO',
            '/SUBSYSTEM:WINDOWS'
        ]

        include_dirs = [
            openzwave + '\\cpp\\src',
            openzwave + '\\cpp\\tinyxml',
            openzwave + '\\cpp\\hidapi\\hidapi',
        ]

        pyozw_common.Library.__init__(
            self,
            openzwave,
            sources=sources,
            define_macros=define_macros,
            libraries=libraries,
            library_dirs=library_dirs,
            include_dirs=include_dirs,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args
        )

    def install(self, command_class):
        pass

    def build(self, command_class):
        if os.path.exists(
            os.path.join(self.build_path + '\\lib_build', 'OpenZWave.lib')
        ):
            return

        objects = []
        thread_event = threading.Event()

        def do(files):
            objs = command_class.compiler.compile(
                files,
                output_dir=command_class.build_temp,
                macros=self.define_macros,
                include_dirs=self.include_dirs,
                extra_preargs=self.extra_compile_args,
                debug=command_class.debug
            )

            objects.extend(objs)

            threads.remove(threading.current_thread())

            if not threads:
                thread_event.set()

        sources = self.sources[:]

        split_files = []
        num_files = int(round(len(sources) / 10))

        while sources:
            try:
                split_files += [sources[:num_files]]
                sources = sources[num_files:]
            except IndexError:
                split_files += [sources[:]]
                del sources[:]

        threads = []

        for fls in split_files:

            while len(threads) >= 8:
                thread_event.wait(0.1)

            t = threading.Thread(target=do, args=(fls,))
            t.daemon = True
            threads += [t]
            t.start()

        thread_event.wait()

        command_class.compiler.create_static_lib(
            objects,
            self.name,
            output_dir=command_class.build_clib,
            debug=command_class.debug
        )

    def clean(self, _):
        build_path = os.path.join(self.openzwave, 'build')
        try:
            shutil.rmtree(build_path)
        except OSError:
            pass


if __name__ == '__main__':
    print("Start pyozw_win")
    print(environment)

    ozw_path = os.path.abspath('openzwave')

    if not os.path.exists(ozw_path):
        pyozw_common.get_openzwave('openzwave')

    from distutils.core import setup
    from Cython.Distutils import build_ext

    import time
    start_time = time.time()

    setup(
        script_args=['build'],
        version=pyozw_version,
        name='libopenzwave',
        description='libopenzwave',
        verbose=1,
        ext_modules=[Extension(ozw_path, 'dev', True, 'cython')],
        libraries=[Library(ozw_path)],
        cmdclass=dict(
            build_clib=pyozw_common.build_clib,
            build_ext=build_ext
        ),
        options=dict(
            build_clib=dict(
                build_clib="openzwave\\build\\lib_build",
                build_temp="openzwave\\build\\lib_build\\temp",
                compiler='msvc'
            ),
            build_ext=dict(
                build_lib="openzwave\\build",
                build_temp="openzwave\\build\\temp"
            )
        )
    )
    end_time = time.time()
    print('Total build time:', end_time - start_time, 'seconds')
