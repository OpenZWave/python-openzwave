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

pyozw_msvc

This tool is used to create an identical build environment to what is created
when building a Visual Studio project or using any of the vcvars and vsvars
batch files. There is a similar tool included with SetupTools and it is called
msvc. The setup tools version is not complete and it is also error prone. It
does not make an identical build environment.
"""


from __future__ import print_function
import os
import sys
import ctypes

from ctypes.wintypes import (
    BOOL,
    DWORD,
    LPCVOID,
    LPCWSTR,
    LPVOID,
    UINT,
    INT
)

try:
    _winreg = __import__('winreg')
except ImportError:
    _winreg = __import__('_winreg')


POINTER = ctypes.POINTER
CHAR = INT
PUINT = POINTER(UINT)
LPDWORD = POINTER(DWORD)


_version = ctypes.windll.version

_GetFileVersionInfoSize = _version.GetFileVersionInfoSizeW
_GetFileVersionInfoSize.restype = DWORD
_GetFileVersionInfoSize.argtypes = [LPCWSTR, LPDWORD]

_GetFileVersionInfo = _version.GetFileVersionInfoW
_GetFileVersionInfo.restype = BOOL
_GetFileVersionInfo.argtypes = [LPCWSTR, DWORD, DWORD, LPVOID]

_VerQueryValue = _version.VerQueryValueW
_VerQueryValue.restype = BOOL
_VerQueryValue.argtypes = [LPCVOID, LPCWSTR, POINTER(LPVOID), PUINT]


# noinspection PyPep8Naming
class VS_FIXEDFILEINFO(ctypes.Structure):
    _fields_ = [
        ("dwSignature", DWORD),  # will be 0xFEEF04BD
        ("dwStrucVersion", DWORD),
        ("dwFileVersionMS", DWORD),
        ("dwFileVersionLS", DWORD),
        ("dwProductVersionMS", DWORD),
        ("dwProductVersionLS", DWORD),
        ("dwFileFlagsMask", DWORD),
        ("dwFileFlags", DWORD),
        ("dwFileOS", DWORD),
        ("dwFileType", DWORD),
        ("dwFileSubtype", DWORD),
        ("dwFileDateMS", DWORD),
        ("dwFileDateLS", DWORD)
    ]


def _get_file_version(filename):
    dw_len = _GetFileVersionInfoSize(filename, None)
    if not dw_len:
        raise ctypes.WinError()

    lp_data = (CHAR * dw_len)()
    if not _GetFileVersionInfo(filename, 0, ctypes.sizeof(lp_data), lp_data):
        raise ctypes.WinError()

    u_len = UINT()
    lpffi = POINTER(VS_FIXEDFILEINFO)()
    lplp_buffer = ctypes.cast(ctypes.pointer(lpffi), POINTER(LPVOID))
    if not _VerQueryValue(lp_data, "\\", lplp_buffer, ctypes.byref(u_len)):
        raise ctypes.WinError()

    ffi = lpffi.contents
    return (
        ffi.dwFileVersionMS >> 16,
        ffi.dwFileVersionMS & 0xFFFF,
        ffi.dwFileVersionLS >> 16,
        ffi.dwFileVersionLS & 0xFFFF,
    )


def _get_reg_value(path, key):
    d = _read_reg_values(path)
    if key in d:
        return d[key]

    return ''


def _read_reg_keys(key):
    if isinstance(key, tuple):
        root = key[0]
        key = key[1]
    else:
        root = _winreg.HKEY_LOCAL_MACHINE
        key = 'SOFTWARE\\Wow6432Node\\Microsoft\\' + key

    try:
        handle = _winreg.OpenKeyEx(root, key)
    except _winreg.error:
        return []
    res = []

    for i in range(_winreg.QueryInfoKey(handle)[0]):
        res += [_winreg.EnumKey(handle, i)]

    return res


def _read_reg_values(key):
    if isinstance(key, tuple):
        root = key[0]
        key = key[1]
    else:
        root = _winreg.HKEY_LOCAL_MACHINE
        key = 'SOFTWARE\\Wow6432Node\\Microsoft\\' + key

    try:
        handle = _winreg.OpenKeyEx(root, key)
    except _winreg.error:
        return {}
    res = {}
    for i in range(_winreg.QueryInfoKey(handle)[1]):
        name, value, _ = _winreg.EnumValue(handle, i)
        res[_convert_mbcs(name)] = _convert_mbcs(value)

    return res


def _convert_mbcs(s):
    dec = getattr(s, "decode", None)
    if dec is not None:
        try:
            s = dec("mbcs")
        except UnicodeError:
            pass
    return s

# I have separated the environment into several classes
# Environment - the main environment class.
# the environment class is what is going to get used. this handles all of the
# non specific bits of the environment. all of the rest of the classes are
# brought together in the environment to form a complete build environment.

# NETInfo - Any .NET related environment settings

# WindowsSDKInfo - Any Windows SDK environment settings

# VisualStudioInfo - Any VisualStudios environment settings (if applicable)

# VisualCInfo - Any VisualC environment settings

# PythonInfo - This class really isnt for environment settings as such.
# It is more of a convenience class. it will get things like a list of the
# includes specific to the python build. the architecture of the version of
# python that is running stuff along those lines.


class PythonInfo(object):

    @property
    def architecture(self):
        return 'x64' if sys.maxsize > 2 ** 32 else 'x86'

    @property
    def version(self):
        return '.'.join(str(ver) for ver in sys.version_info)

    @property
    def dependency(self):
        return 'Python%d%d.lib' % sys.version_info[:2]

    @property
    def includes(self):
        python_path = os.path.dirname(sys.executable)
        python_include = os.path.join(python_path, 'include')

        python_includes = [python_include]
        for root, dirs, files in os.walk(python_include):
            for d in dirs:
                python_includes += [os.path.join(root, d)]
        return python_includes

    @property
    def libraries(self):
        python_path = os.path.dirname(sys.executable)
        python_lib = os.path.join(python_path, 'libs')

        python_libs = [python_lib]
        for root, dirs, files in os.walk(python_lib):
            for d in dirs:
                python_libs += [os.path.join(root, d)]
        return python_libs


python_info = PythonInfo()


class VisualCInfo(object):

    def __init__(self, platform, strict_version, minimum_version):
        self.platform = platform
        self.strict_version = strict_version
        self.minimum_version = minimum_version
        self.__installed_versions = None

    @property
    def f_sharp_path(self):

        reg_path = (
            _winreg.HKEY_LOCAL_MACHINE,
            'SOFTWARE\Wow6432Node\Microsoft\\VisualStudio\\'
            '{0:.1f}\\Setup\\F#'.format(self.version)
        )

        f_sharp_path = _get_reg_value(reg_path, 'ProductDir')
        if f_sharp_path and os.path.exists(f_sharp_path):
            return f_sharp_path

        path = r'C:\Program Files (x86)\Microsoft SDKs\F#'
        if os.path.exists(path):
            versions = os.listdir(path)
            max_ver = 0.0
            found_version = ''

            for version in versions:
                try:
                    ver = float(version)
                except ValueError:
                    continue

                if ver > max_ver:
                    max_ver = ver
                    found_version = version

            f_sharp_path = os.path.join(
                path,
                found_version,
                'Framework',
                'v' + found_version
            )

            if os.path.exists(f_sharp_path):
                return f_sharp_path

    @property
    def ide_install_directory(self):
        directory = self.install_directory
        ide_directory = os.path.abspath(os.path.join(directory, '..'))

        ide_directory = os.path.join(ide_directory, 'Common7', 'IDE', 'VC')
        if os.path.exists(ide_directory):
            return ide_directory

    @property
    def install_directory(self):
        """
        Visual C path
        :return: Visual C path
        """
        return self._installed_c_paths[self.version]['base']

    @property
    def _installed_c_paths(self):

        if self.__installed_versions is None:
            self.__installed_versions = {}

            reg_path = (
                _winreg.HKEY_CLASSES_ROOT,
                'Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache'
            )

            paths = []

            for key in _read_reg_values(reg_path):
                if 'cl.exe' in key:
                    value = _get_reg_value(reg_path, key)
                    if 'C++ Compiler Driver' in value:
                        paths += [key]

            for path in paths:
                if not os.path.exists(path):
                    continue

                if '\\VC\\bin' in path:
                    version = path.split('\\VC\\bin')[0]
                else:
                    version = path.split('\\bin\\Host')[0]

                version = os.path.split(version)[1]
                version = version.replace(
                    'Microsoft Visual Studio',
                    ''
                ).strip()
                base_version = float(int(version.split('.')[0]))

                base_path = path.split('\\VC\\')[0] + '\\VC'
                if os.path.exists(os.path.join(base_path, 'include')):
                    vc_root = base_path
                else:
                    vc_root = path.split('\\bin\\')[0]

                self.__installed_versions[version] = dict(
                    base=base_path,
                    root=vc_root
                )
                self.__installed_versions[base_version] = dict(
                    base=base_path,
                    root=vc_root
                )

            reg_path = (
                _winreg.HKEY_LOCAL_MACHINE,
                'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VS7'
            )

            for key in _read_reg_values(reg_path):
                try:
                    version = float(key)
                except ValueError:
                    continue

                path = _get_reg_value(reg_path, key)

                if (
                    (
                        os.path.exists(path) and
                        version not in self.__installed_versions
                    ) or version == 15.0
                ):

                    if version == 15.0:
                        version = 14.0

                    if not os.path.split(path)[1] == 'VC':
                        path = os.path.join(path, 'VC')

                    self.__installed_versions[version] = dict(
                        base=path,
                        root=path
                    )
                    self.__installed_versions[key] = dict(
                        base=path,
                        root=path
                    )
        return self.__installed_versions

    @property
    def version(self):
        """
        Visual C version

        Sometimes when building extension in python the version of the compiler
        that was used to compile Python has to also be used to compile an
        extension. I have this system set so it will automatically pick the
        most recent compiler installation. this can be overridden in 2 ways.
        The first way being that the compiler version that built Python has to
        be used. The second way is you can set a minimum compiler version to
        use.

        :return: found Visual C version
        """

        py_version = sys.version_info[:2]
        if py_version in ((2, 6), (2, 7), (3, 0), (3, 1), (3, 2)):
            min_visual_c_version = 9.0

        elif py_version in ((3, 3), (3, 4)):
            min_visual_c_version = 10.0

        elif py_version in ((3, 5), (3, 6), (3, 7)):
            min_visual_c_version = 14.0
        else:
            raise RuntimeError(
                'This library does not support '
                'python version %d.%d' % py_version
            )

        max_version = 0.0

        if self.strict_version is not None:
            if self.strict_version < min_visual_c_version:
                raise RuntimeError(
                    'The set minimum compiler version is lower then the '
                    'required compiler version for Python'
                )
            if self.strict_version not in self._installed_c_paths:
                raise RuntimeError(
                    'No Compatible Visual C version found.'
                )
            return self.strict_version

        elif self.minimum_version is not None:
            for version in self._installed_c_paths:
                if not isinstance(version, float):
                    continue

                if version >= self.minimum_version:
                    max_version = max(max_version, version)

        else:
            for version in self._installed_c_paths:
                if not isinstance(version, float):
                    continue

                if version >= min_visual_c_version:
                    max_version = max(max_version, version)

        if max_version == 0:
            raise RuntimeError(
                'No Compatible Visual C\\C++ version found.'
            )

        return max_version

    @property
    def tools_version(self):
        version = os.path.split(self.tools_install_directory)[1]
        if not version.split('.')[-1].isdigit():
            version = str(self.version)

        return version

    @property
    def toolset_version(self):
        """
        The platform toolset gets written to the solution file. this instructs
        the compiler to use the matching MSVCPxxx.dll file.
        :return: one of the following
            Visual C  Visual Studio  Returned Value
            VC 15.0 - VS 2017:       v141
            VC 14.0 - VS 2015:       v140
            VC 12.0 - VS 2013:       v120
            VC 11.0 - VS 2012:       v110
            VC 10.0 - VS 2010:       v100
            VC  9.0 - VS 2008:       v90

        """
        toolsets = {
            15.0: 'v141',
            14.0: 'v140',
            12.0: 'v120',
            11.0: 'v110',
            10.0: 'v100',
            9.0:  'v90'
        }

        return toolsets[self.version]

    @property
    def msvc_dll_version(self):
        msvc_dll_path = self.msvc_dll_path
        if msvc_dll_path:
            for f in os.listdir(msvc_dll_path):
                if f.endswith('dll'):
                    version = _get_file_version(os.path.join(msvc_dll_path, f))
                    return '.'.join(str(ver) for ver in version)

    @property
    def msvc_dll_path(self):
        x64 = self.platform == 'x64'
        folder_names = (
            'Microsoft.VC{0}.CRT'.format(self.toolset_version[1:]),
        )
        if self.toolset_version == 'v140':
            folder_names += ('Microsoft.VC141.CRT',)

        redist_path = self.tools_redist_directory

        for root, dirs, files in os.walk(redist_path):
            def pass_directory():
                for item in ('onecore', 'arm', 'spectre'):
                    if item in root.lower():
                        return True
                return False

            if pass_directory():
                continue

            for folder_name in folder_names:
                if folder_name in dirs:
                    if x64 and ('amd64' in root or 'x64' in root):
                        return os.path.join(root, folder_name)
                    elif (
                        not x64 and
                        'amd64' not in root
                        and 'x64' not in root
                    ):
                        return os.path.join(root, folder_name)

    @property
    def tools_redist_directory(self):
        tools_install_path = self.tools_install_directory
        if 'MSVC' in tools_install_path:
            redist_path = tools_install_path.replace('Tools', 'Redist')
            if 'BuildTools' in tools_install_path:
                redist_path = redist_path.replace('BuildRedist', 'BuildTools')
        else:
            redist_path = os.path.join(tools_install_path, 'Redist')

        if not os.path.exists(redist_path):
            redist_path = os.path.split(redist_path)[0]
            max_ver = (0, 0, 0)
            for f in os.listdir(redist_path):
                if os.path.isdir(os.path.join(redist_path, f)):
                    try:
                        ver = tuple(int(ver) for ver in f.split('.'))
                    except ValueError:
                        continue
                    if ver > max_ver:
                        max_ver = ver
            if max_ver != (0, 0, 0):
                return os.path.join(
                    redist_path,
                    '.'.join(str(ver) for ver in max_ver)
                )
            else:
                return ''

        else:
            return redist_path

    @property
    def tools_install_directory(self):
        """
        Visual C compiler tools path.
        :return: Path to the compiler tools
        """
        vc_version = self.version
        if vc_version >= 14.0:
            vc_tools_path = self._installed_c_paths[vc_version]['root']
        else:
            vc_tools_path = self._installed_c_paths[vc_version]['base']

        lib_path = os.path.join(vc_tools_path, 'lib')

        if not os.path.exists(lib_path):
            tools_path = os.path.join(vc_tools_path, 'Tools', 'MSVC')

            if os.path.exists(tools_path):
                versions = os.listdir(tools_path)
                max_version = (0, 0, 0)
                found_version = ''

                for version in versions:
                    try:
                        ver = tuple(
                            int(vr) for vr in version.split('.')
                        )
                    except ValueError:
                        continue

                    if ver > max_version:
                        max_version = ver
                        found_version = version

                vc_tools_path = os.path.join(
                    tools_path,
                    found_version
                )

        return vc_tools_path

    @property
    def msbuild_version(self):
        """
        MSBuild versions are specific to the Visual C version
        :return: MSBuild version, 3.5, 4.0, 12, 14, 15
        """
        vc_version = self.version
        if vc_version == 9.0:
            return 3.5
        if vc_version in (10.0, 11.0):
            return 4.0
        else:
            return vc_version

    @property
    def msbuild_path(self):
        program_files = os.environ.get(
            'ProgramFiles(x86)',
            'C:\\Program Files (x86)'
        )

        ms_build_path = os.path.join(
            program_files,
            'MSBuild',
            '{0:.1f}'.format(self.version),
            'bin'
        )

        if self.platform == 'x64':
            if os.path.exists(os.path.join(ms_build_path, 'x64')):
                ms_build_path = os.path.join(ms_build_path, 'x64')
            else:
                ms_build_path = os.path.join(ms_build_path, 'amd64')

        elif os.path.exists(os.path.join(ms_build_path, 'x86')):
            ms_build_path = os.path.join(ms_build_path, 'x86')

        if os.path.exists(ms_build_path):
            return ms_build_path

    @property
    def html_help_path(self):

        reg_path = (
            _winreg.HKEY_LOCAL_MACHINE,
            'SOFTWARE\\Wow6432Node\\Microsoft\Windows\\'
            'CurrentVersion\\App Paths\\hhw.exe'
        )

        html_help_path = _get_reg_value(reg_path, 'Path')
        if html_help_path and os.path.exists(html_help_path):
            return html_help_path

        if os.path.exists(r'C:\Program Files (x86)\HTML Help Workshop'):
            return r'C:\Program Files (x86)\HTML Help Workshop'

    @property
    def path(self):
        tools_path = self.tools_install_directory
        base_path = os.path.join(tools_path, 'bin')

        path = []

        f_sharp_path = self.f_sharp_path
        msbuild_path = self.msbuild_path

        if self.platform == 'x64':
            perf_tools_path = os.path.join(
                self.tools_install_directory,
                'Team Tools',
                'Performance Toolsx64'
            )
        else:
            perf_tools_path = os.path.join(
                self.tools_install_directory,
                'Team Tools',
                'Performance Tools'
            )

        if msbuild_path is not None:
            path += [msbuild_path]

        if os.path.exists(perf_tools_path):
            path += [perf_tools_path]

        if f_sharp_path is not None:
            path += [f_sharp_path]

        html_help_path = self.html_help_path
        if html_help_path is not None:
            path += [html_help_path]

        bin_path = os.path.join(
            base_path,
            'Host' + self.platform,
            self.platform
        )

        if not os.path.exists(bin_path):
            if self.platform == 'x64':
                bin_path = os.path.join(base_path, 'x64')

                if not os.path.exists(bin_path):
                    bin_path = os.path.join(base_path, 'amd64')

            else:
                bin_path = os.path.join(base_path, 'x86')
                if not os.path.exists(bin_path):
                    bin_path = base_path

        if os.path.exists(bin_path):
            path += [bin_path]

        return path

    @property
    def atlmfc_lib_path(self):
        atlmfc_path = self.atlmfc_path
        if not atlmfc_path:
            return

        atlmfc = os.path.join(atlmfc_path, 'lib')
        if self.platform == 'x64':
            atlmfc_path = os.path.join(atlmfc, 'x64')
            if not os.path.exists(atlmfc_path):
                atlmfc_path = os.path.join(atlmfc, 'amd64')
        else:
            atlmfc_path = os.path.join(atlmfc, 'x86')
            if not os.path.exists(atlmfc_path):
                atlmfc_path = atlmfc

        if os.path.exists(atlmfc_path):
            return atlmfc_path

    @property
    def lib(self):
        tools_path = self.tools_install_directory
        path = os.path.join(tools_path, 'lib')

        if self.platform == 'x64':
            lib_path = os.path.join(path, 'x64')
            if not os.path.exists(lib_path):
                lib_path = os.path.join(path, 'amd64')

        else:
            lib_path = os.path.join(path, 'x86')

            if not os.path.exists(lib_path):
                lib_path = path

        lib = []
        if os.path.exists(lib_path):
            lib += [lib_path]

        atlmfc_path = self.atlmfc_lib_path
        if atlmfc_path is not None:
            lib += [atlmfc_path]

        return lib

    @property
    def lib_path(self):
        tools_path = self.tools_install_directory
        path = os.path.join(tools_path, 'lib')

        if self.platform == 'x64':
            lib = os.path.join(path, 'x64')
            if not os.path.exists(lib):
                lib = os.path.join(path, 'amd64')
        else:
            lib = os.path.join(path, 'x86')
            if not os.path.exists(lib):
                lib = path

        references_path = os.path.join(lib, 'store', 'references')

        lib_path = []
        if os.path.exists(lib):
            lib_path += [lib]

        atlmfc_path = self.atlmfc_lib_path

        if atlmfc_path is not None:
            lib_path += [atlmfc_path]

        if os.path.exists(references_path):
            lib_path += [references_path]

        return lib_path
# LIB:
    #     C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC\lib
    #     C:\Program Files (x86)\Microsoft SDKs\Windows\v7.1A\lib
    @property
    def atlmfc_path(self):
        tools_path = self.tools_install_directory
        atlmfc_path = os.path.join(tools_path, 'ATLMFC')

        if os.path.exists(atlmfc_path):
            return atlmfc_path

    @property
    def atlmfc_include_path(self):
        atlmfc_path = self.atlmfc_path
        if atlmfc_path:
            atlmfc_path = os.path.join(atlmfc_path, 'include')
            if os.path.exists(atlmfc_path):
                return atlmfc_path

    @property
    def include(self):
        tools_path = self.tools_install_directory
        include_path = os.path.join(tools_path, 'include')
        atlmfc_path = self.atlmfc_include_path

        include = []
        if os.path.exists(include_path):
            include += [include_path]

        if atlmfc_path is not None:
            include += [atlmfc_path]
        return include

    def __iter__(self):
        ide_install_directory = self.ide_install_directory
        tools_install_directory = self.tools_install_directory
        install_directory = self.install_directory

        if ide_install_directory:
            ide_install_directory += '\\'

        if tools_install_directory:
            tools_install_directory += '\\'

        if install_directory:
            install_directory += '\\'

        env = dict(
            VCIDEInstallDir=ide_install_directory,
            VCToolsVersion=self.tools_version,
            VCToolsInstallDir=tools_install_directory,
            VCINSTALLDIR=install_directory,
            VCToolsRedistDir=self.tools_redist_directory,
            Path=self.path,
            LIB=self.lib,
            Include=self.include,
            LIBPATH=self.lib_path,
            FSHARPINSTALLDIR=self.f_sharp_path
        )

        for key, value in env.items():
            if value is not None and value:
                if isinstance(value, list):
                    value = os.pathsep.join(value)
                yield key, str(value)


class VisualStudioInfo(object):

    def __init__(self, c_info):
        self.c_info = c_info

    @property
    def install_directory(self):
        return os.path.abspath(
            os.path.join(self.c_info.install_directory, '..')
        )

    @property
    def dev_env_directory(self):
        return os.path.join(self.install_directory, 'Common7', 'IDE')

    @property
    def common_tools(self):
        return os.path.join(self.install_directory, 'Common7', 'Tools')

    @property
    def path(self):

        path = [self.dev_env_directory, self.common_tools]

        collection_tools_dir = _get_reg_value(
            'VisualStudio\\VSPerf',
            'CollectionToolsDir'
        )
        if collection_tools_dir and os.path.exists(collection_tools_dir):
            path += [collection_tools_dir]

        vs_ide_path = self.dev_env_directory

        test_window_path = os.path.join(
            vs_ide_path,
            'CommonExtensions',
            'Microsoft',
            'TestWindow'
        )

        vs_tdb_path = os.path.join(
            vs_ide_path,
            'VSTSDB',
            'Deploy'
        )

        if os.path.exists(vs_tdb_path):
            path += [vs_tdb_path]

        if os.path.exists(test_window_path):
            path += [test_window_path]

        return path

    @property
    def version(self):
        return self.c_info.version

    def __iter__(self):
        install_directory = self.install_directory
        dev_env_directory = self.dev_env_directory

        if install_directory:
            install_directory += '\\'

        if dev_env_directory:
            dev_env_directory += '\\'

        env = dict(
            Path=self.path,
            VSINSTALLDIR=install_directory,
            DevEnvDir=dev_env_directory,
            VisualStudioVersion=self.version
        )

        env['VS{0:.0f}0COMNTOOLS'.format(self.c_info.version)] = (
            self.common_tools
        )
        for key, value in env.items():
            if value is not None and value:
                if isinstance(value, list):
                    value = os.pathsep.join(value)
                yield key, str(value)


class WindowsSDKInfo(object):

    def __init__(self, platform, vc_version):
        self.platform = platform
        self.vc_version = vc_version

    @property
    def extension_sdk_directory(self):
        version = self.version
        if version.startswith('10'):
            version = '10.0'

        sdk_path = _get_reg_value(
            'Microsoft SDKs\\Windows\\v' + version,
            'InstallationFolder'
        )

        if sdk_path:
            sdk_path = sdk_path.replace(
                'Windows Kits',
                'Microsoft SDKs\\Windows Kits'
            )
            extension_path = os.path.join(sdk_path[:-1], 'ExtensionSDKs')
            if os.path.exists(extension_path):

                return extension_path

    @property
    def lib_version(self):
        return self.sdk_version

    @property
    def ver_bin_path(self):
        bin_path = self.bin_path[:-1]
        ver_bin_path = os.path.join(bin_path, self.version)
        if os.path.exists(ver_bin_path):
            return ver_bin_path
        else:
            return bin_path

    @property
    def mssdk(self):
        return self.directory

    @property
    def ucrt_version(self):
        return self.sdk_version[:-1]

    @property
    def ucrt_sdk_directory(self):
        directory = self.directory
        if directory:
            return directory + '\\'

    @property
    def bin_path(self):
        directory = self.directory
        if directory:
            bin_path = os.path.join(
                self.directory,
                'bin'
            )

            return bin_path + '\\'

    @property
    def lib(self):
        directory = self.directory
        if not directory:
            return []

        version = self.version
        lib = []

        base_lib = os.path.join(
            directory,
            'lib',
            version,
        )
        if not os.path.exists(base_lib):
            base_lib = os.path.join(
                directory,
                'lib'
            )

        if os.path.exists(base_lib):
            if self.platform == 'x64':
                if os.path.exists(os.path.join(base_lib, 'x64')):
                    lib += [os.path.join(base_lib, 'x64')]

                ucrt = os.path.join(base_lib, 'ucrt', self.platform)
                um = os.path.join(base_lib, 'um', self.platform)
                if not os.path.exists(ucrt):
                    ucrt = os.path.join(base_lib, 'ucrt', 'amd64')

                if not os.path.exists(um):
                    um = os.path.join(base_lib, 'um', 'amd64')

            else:
                lib += [base_lib]
                ucrt = os.path.join(base_lib, 'ucrt', self.platform)
                um = os.path.join(base_lib, 'um', self.platform)

                if not os.path.exists(ucrt):
                    ucrt = os.path.join(base_lib, 'ucrt')

                if not os.path.exists(um):
                    um = os.path.join(base_lib, 'um')

            if os.path.exists(ucrt):
                lib += [ucrt]

            if os.path.exists(um):
                lib += [um]

        return lib

    @property
    def path(self):
        path = []
        ver_bin_path = self.ver_bin_path

        if not ver_bin_path:
            return []

        if self.platform == 'x64':
            bin_path = os.path.join(ver_bin_path, 'x64')
            if not os.path.exists(bin_path):
                bin_path = os.path.join(ver_bin_path, 'amd64')
        else:
            bin_path = os.path.join(ver_bin_path, 'x86')

            if not os.path.exists(bin_path):
                bin_path = ver_bin_path

        if os.path.exists(bin_path):
            path += [bin_path]

        type_script_path = self.type_script_path
        if type_script_path is not None:
            path += [type_script_path]

        return path

    @property
    def type_script_path(self):
        program_files = os.environ.get(
            'ProgramFiles(x86)',
            'C:\\Program Files (x86)'
        )
        type_script_path = os.path.join(
            program_files,
            'Microsoft SDKs',
            'TypeScript'
        )

        if os.path.exists(type_script_path):
            max_ver = 0.0
            for version in os.listdir(type_script_path):
                try:
                    version = float(version)
                except ValueError:
                    continue
                max_ver = max(max_ver, version)

            type_script_path = os.path.join(type_script_path, str(max_ver))

            if os.path.exists(type_script_path):
                return type_script_path

    @property
    def include(self):
        directory = self.directory
        if not directory:
            return []

        include_path = os.path.join(directory, 'include', self.version)
        if not os.path.exists(include_path):
            include_path = os.path.split(include_path)[0]

        includes = [include_path]

        for path in ('ucrt', 'cppwinrt', 'shared', 'um', 'winrt'):
            pth = os.path.join(include_path, path)
            if os.path.exists(pth):
                includes += [pth]

        gl_include = os.path.join(include_path, 'gl')

        if os.path.exists(gl_include):
            includes += [gl_include]

        return includes

    @property
    def lib_path(self):
        return self.sdk_lib_path

    @property
    def sdk_lib_path(self):
        directory = self.directory
        version = self.version

        if not directory:
            return []

        union_meta_data = os.path.join(
            directory,
            'UnionMetadata',
            version
        )
        references = os.path.join(
            directory,
            'References',
            version
        )

        lib_path = []

        if os.path.exists(union_meta_data):
            lib_path += [union_meta_data]

        if os.path.exists(references):
            lib_path += [references]

        return lib_path

    @property
    def windows_sdks(self):
        """
        Windows SDK versions that are compatible with Visual C
        :return: compatible Windows SDK versions
        """
        ver = self.vc_version
        if ver <= 9.0:
            return '7.0', '6.1', '6.0a'
        elif ver == 10.0:
            return '7.1a', '7.1', '7.0a'
        elif ver == 11.0:
            return '8.0', '8.0a'
        elif ver == 12.0:
            return '8.1', '8.1a'
        elif ver >= 14.0:
            return '10.0', '8.1'

    @property
    def version(self):
        """
        This is used in the solution file to tell the compiler what SDK to use.
        We obtain a list of compatible Windows SDK versions for the
        Visual C version. We check and see if any  of the compatible SDK's are
        installed and if so we return that version.

        :return: Installed Windows SDK version
        """
        for sdk in self.windows_sdks:
            sdk_version = _get_reg_value(
                'Microsoft SDKs\\Windows\\v' + sdk,
                'ProductVersion'
            )
            if sdk == '10.0':
                return sdk_version + '.0'
            else:
                return sdk

        raise RuntimeError(
            'Unable to locate suitable SDK %s' % (self.windows_sdks,)
        )

    @property
    def sdk_version(self):
        """
        This is almost identical to target_platform. Except it returns the
        actual version of the Windows SDK not the truncated version.

        :return: actual Windows SDK version
        """
        for sdk in self.windows_sdks:
            sdk_version = _get_reg_value(
                'Microsoft SDKs\\Windows\\v' + sdk,
                'ProductVersion'
            )
            return sdk_version + '.0' + '\\'

        raise RuntimeError(
            'Unable to locate suitable SDK %s' % (self.windows_sdks,)
        )

    @property
    def directory(self):
        """
        Path to the Windows SDK version that has been found.
        :return: Windows SDK path
        """
        for sdk in self.windows_sdks:
            sdk_installation_folder = _get_reg_value(
                'Microsoft SDKs\\Windows\\v' + sdk,
                'InstallationFolder'
            )
            if sdk_installation_folder:
                return sdk_installation_folder[:-1]
        raise RuntimeError(
            'Unable to locate suitable SDK %s' % (self.windows_sdks,)
        )

    def __iter__(self):

        ver_bin_path = self.ver_bin_path
        directory = self.directory

        if ver_bin_path:
            ver_bin_path += '\\'

        if directory:
            directory += '\\'

        env = dict(
            LIB=self.lib,
            Path=self.path,
            LIBPATH=self.lib_path,
            Include=self.include,
            UniversalCRTSdkDir=self.ucrt_sdk_directory,
            ExtensionSdkDir=self.extension_sdk_directory,
            WindowsSdkVerBinPath=ver_bin_path,
            UCRTVersion=self.ucrt_version,
            WindowsSDKLibVersion=self.lib_version,
            WindowsSDKVersion=self.sdk_version,
            WindowsSdkDir=directory,
            WindowsLibPath=self.lib_path,
            WindowsSdkBinPath=self.bin_path,
            DISTUTILS_USE_SDK=1,
            MSSDK=self.directory
        )

        for key, value in env.items():
            if value is not None and value:
                if isinstance(value, list):
                    value = os.pathsep.join(value)
                yield key, str(value)


class NETInfo(object):

    def __init__(self, platform, vc_version, sdk_version):
        self.platform = platform
        self.vc_version = vc_version
        self.sdk_version = sdk_version

    @property
    def version(self):
        """
        .NET Version
        :return: returns the version associated with the architecture
        """
        if self.platform == 'x64':
            return self.version_64
        else:
            return self.version_32

    @property
    def version_32(self):
        """
        .NET 32bit framework version
        :return: x86 .NET framework version
        """

        target_frameworks = {
            15.0: ('4.7*', '4.6*', '4.5*', '4.0*', '3.5*', '3.0*', '2.0*'),
            14.0: ('4.6*', '4.5*', '4.0*', '3.5*', '3.0*', '2.0*'),
            12.0: ('4.5*', '4.0*', '3.5*', '3.0*', '2.0*'),
            11.0: ('4.5*', '4.0*', '3.5*', '3.0*', '2.0*'),
            10.0: ('4.0*', '3.5*', '3.0*', '2.0*'),
            9.0:  ('3.5*', '3.0*', '2.0*')
        }

        target_framework = _get_reg_value(
            'VisualStudio\\SxS\\VC7',
            'FrameworkVer32'
        )

        if not target_framework:
            import fnmatch

            versions = list(
                key for key in _read_reg_keys('.NETFramework\\')
                if key.startswith('v')
            )

            target_frameworks = target_frameworks[self.vc_version]
            for version in versions:
                for target_framework in target_frameworks:
                    if fnmatch.fnmatch(version, 'v' + target_framework):
                        target_framework = version
                        break
                else:
                    continue

                break
            else:
                raise RuntimeError(
                    'No Suitable .NET Framework found %s' %
                    (target_frameworks,)
                )
        return target_framework

    @property
    def version_64(self):
        """
        .NET 64bit framework version
        :return: x64 .NET framework version
        """
        target_framework = _get_reg_value(
            'VisualStudio\\SxS\\VC7',
            'FrameworkVer64'
        )
        if not target_framework:
            target_framework = self.version_32

        return target_framework

    @property
    def directory(self):
        if self.platform == 'x64':
            framework_path = os.path.join(
                self.directory_64,
                self.version_64
            )
        else:
            framework_path = os.path.join(
                self.directory_32,
                self.version_32
            )

        return framework_path

    @property
    def directory_32(self):
        """
        .NET 32bit path
        :return: path to x86 .NET
        """
        directory = _get_reg_value(
            'VisualStudio\\SxS\\VC7\\',
            'FrameworkDir32'
        )

        if directory is None:
            return os.path.join(
                os.environ.get('WINDIR', r'C:\Windows'),
                'Microsoft.NET',
                'Framework'
            )

        return directory[:-1]

    @property
    def directory_64(self):
        """
        .NET 64bit path
        :return: path to x64 .NET
        """
        guess_fw = os.path.join(
            os.environ.get('WINDIR', r'C:\Windows'),
            'Microsoft.NET',
            'Framework64'
        )

        return (
            _get_reg_value('VisualStudio\\SxS\\VC7\\', 'FrameworkDir64') or
            guess_fw
        )

    @property
    def preferred_bitness(self):
        return '32' if self.platform == 'x86' else '64'

    @property
    def _net_fx_versions(self):
        import fnmatch

        framework = self.version[1:].split('.')[:2]
        net_fx_key = (
            'WinSDK-NetFx{framework}Tools-{platform}'
        ).format(
            framework=''.join(framework),
            platform=self.platform
        )
        ver = self.vc_version

        if ver in (9.0, 10.0, 11.0, 12.0):
            key = 'Microsoft SDKs\\Windows\\v{0}\\{1}'.format(
                self.sdk_version,
                net_fx_key
            )

            if self.sdk_version in ('6.0A', '6.1'):
                key = key.replace(net_fx_key, 'WinSDKNetFxTools')

            keys = (key,)

        elif ver in (14.0, 15.0):
            keys = (

                'Microsoft SDKs\\NETFXSDK\\4.6*\\' + net_fx_key,
                'Microsoft SDKs\\Windows\\v8.1\\' + net_fx_key
            )
            if ver == 15.0:
                keys = (
                           'Microsoft SDKs\\NETFXSDK\\4.7*\\' + net_fx_key,
                       ) + keys

        else:
            raise RuntimeError(
                'This package does not support VC version ' + str(ver)
            )

        for key in keys:
            if '*' in key:
                for fx_ver in _read_reg_keys('Microsoft SDKs\\NETFXSDK'):
                    fx_ver = 'Microsoft SDKs\\NETFXSDK\\{0}\\{1}'.format(
                        fx_ver,
                        net_fx_key
                    )

                    if fnmatch.fnmatch(fx_ver, key):
                        yield fx_ver
            else:
                val = _get_reg_value(
                    key + '\\',
                    'InstallationFolder'
                )
                if val:
                    yield key

    @property
    def netfx_sdk_directory(self):

        for key in self._net_fx_versions:
            net_fx_path = _get_reg_value(
                key.rsplit('\\', 1)[0],
                'KitsInstallationFolder'
             )

            if net_fx_path and os.path.exists(net_fx_path):
                return net_fx_path

    @property
    def net_fx_tools_directory(self):
        for key in self._net_fx_versions:
            net_fx_path = _get_reg_value(key, 'InstallationFolder')

            if net_fx_path and os.path.exists(net_fx_path):
                return net_fx_path

    @property
    def add(self):
        return '__DOTNET_ADD_{0}BIT'.format(self.preferred_bitness)

    @property
    def net_tools(self):
        if self.vc_version <= 10.0:
            include32 = True
            include64 = self.platform == 'x64'
        else:
            include32 = self.platform == 'x86'
            include64 = self.platform == 'x64'

        tools = []
        if include32:
            tools += [
                os.path.join(self.directory_32, self.version_32)
            ]
        if include64:
            tools += [
                os.path.join(self.directory_64, self.version_64)
            ]

        return tools

    @property
    def executable_path_x64(self):
        tools_directory = self.net_fx_tools_directory
        if not tools_directory:
            return

        if 'NETFX' in tools_directory:
            if 'x64' in tools_directory:
                return tools_directory
            else:
                tools_directory = os.path.join(tools_directory, 'x64')
                if os.path.exists(tools_directory):
                    return tools_directory

    @property
    def executable_path_x86(self):
        tools_directory = self.net_fx_tools_directory
        if not tools_directory:
            return

        if 'NETFX' in tools_directory:
            if 'x64' in tools_directory:
                return (
                    os.path.split(os.path.split(tools_directory)[0])[0] + '\\'
                )
            else:
                return tools_directory
        return None

    @property
    def lib(self):
        sdk_directory = self.netfx_sdk_directory
        if not sdk_directory:
            return []

        sdk_directory = os.path.join(sdk_directory, 'lib', 'um')

        if self.platform == 'x64':
            lib_dir = os.path.join(sdk_directory, 'x64')
            if not os.path.exists(lib_dir):
                lib_dir = os.path.join(sdk_directory, 'amd64')
        else:
            lib_dir = os.path.join(sdk_directory, 'x86')
            if not os.path.exists(lib_dir):
                lib_dir = sdk_directory

        if os.path.exists(lib_dir):
            return [lib_dir]

        return []

    @property
    def path(self):
        path = self.lib_path
        net_fx_tools = self.net_fx_tools_directory
        if net_fx_tools:
            path += [net_fx_tools]

        return path

    @property
    def lib_path(self):
        directory = self.directory

        if directory and os.path.exists(directory):
            return [directory]

        return []

    @property
    def include(self):
        net_fx_tools = self.net_fx_tools_directory

        if net_fx_tools:
            net_fx_tools = os.path.join(
                net_fx_tools,
                'include',
                'um'
            )
            if os.path.exists(net_fx_tools):
                return [net_fx_tools]

        return []

    def __iter__(self):

        directory = self.directory
        if directory:
            directory += '\\'

        env = dict(
            WindowsSDK_ExecutablePath_x64=self.executable_path_x64,
            WindowsSDK_ExecutablePath_x86=self.executable_path_x86,
            LIB=self.lib,
            Path=self.path,
            LIBPATH=self.lib_path,
            Include=self.include,
            __DOTNET_PREFERRED_BITNESS=self.preferred_bitness,
            FrameworkDir=directory,
            FrameworkVersion=self.version,
            NETFXSDKDir=self.netfx_sdk_directory,
        )

        env[self.add] = '1'
        if self.platform == 'x64':
            directory_64 = self.directory_64

            if directory_64:
                directory_64 += '\\'

            env['FrameworkDIR64'] = directory_64
            env['FrameworkVersion64'] = self.version_64
        else:
            directory_32 = self.directory_32
            if directory_32:
                directory_32 += '\\'

            env['FrameworkDIR32'] = directory_32
            env['FrameworkVersion32'] = self.version_32

        framework = env['FrameworkVersion'][1:].split('.')[:2]
        framework_version_key = (
            'Framework{framework}Version'.format(framework=''.join(framework))
        )
        env[framework_version_key] = 'v' + '.'.join(framework)

        for key, value in env.items():
            if value is not None and value:
                if isinstance(value, list):
                    value = os.pathsep.join(value)
                yield key, str(value)


class Environment(object):

    def __init__(
        self,
        strict_visual_c_version=None,
        minimum_visual_c_version=None,
    ):

        self.visual_c = VisualCInfo(
            self.platform,
            strict_visual_c_version,
            minimum_visual_c_version
        )

        self.visual_studio = VisualStudioInfo(
            self.visual_c
        )

        self.windows_sdk = WindowsSDKInfo(
            self.platform,
            self.visual_c.version
        )

        self.dot_net = NETInfo(
            self.platform,
            self.visual_c.version,
            self.windows_sdk.version
        )

        self.python = PythonInfo()

    @property
    def machine_architecture(self):
        import platform
        return 'x64' if '64' in platform.machine() else 'x86'

    @property
    def platform(self):
        """
        :return: x86 or x64
        """
        import platform

        win_64 = self.machine_architecture == 'x64'
        python_64 = platform.architecture()[0] == '64bit' and win_64

        return 'x64' if python_64 else 'x86'

    @property
    def configuration(self):
        """
        Build configuration
        :return: one of ReleaseDLL, DebugDLL
        """

        if os.path.splitext(sys.executable)[0].endswith('_d'):
            config = 'Debug'
        else:
            config = 'Release'

        return config

    def __iter__(self):
        for item in self.build_environment.items():
            yield item

    @property
    def build_environment(self):
        """
        This would be the work horse. This is where all of the gathered
        information is put into a single container and returned.
        The information is then added to os.environ in order to allow the
        build process to run properly.

        List of environment variables generated:
        PATH
        LIBPATH
        LIB
        INCLUDE
        Platform
        FrameworkDir
        FrameworkVersion
        FrameworkDIR32
        FrameworkVersion32
        FrameworkDIR64
        FrameworkVersion64
        VCToolsRedistDir
        VCINSTALLDIR
        VCToolsInstallDir
        VCToolsVersion
        WindowsLibPath
        WindowsSdkDir
        WindowsSDKVersion
        WindowsSdkBinPath
        WindowsSdkVerBinPath
        WindowsSDKLibVersion
        __DOTNET_ADD_32BIT
        __DOTNET_ADD_64BIT
        __DOTNET_PREFERRED_BITNESS
        Framework{framework version}Version
        NETFXSDKDir
        UniversalCRTSdkDir
        UCRTVersion
        ExtensionSdkDir

        These last 2 are set to ensure that distuils uses these environment
        variables when compiling libopenzwave.pyd
        MSSDK
        DISTUTILS_USE_SDK

        :return: dict of environment variables
        """
        path = os.environ.get('Path', '')

        env = dict(
            __VSCMD_PREINIT_PATH=path,
            Platform=self.platform,
        )

        def update_env(cls):
            for key, value in cls:
                if key in env:
                    env[key] += ';' + value
                else:
                    env[key] = value

        update_env(self.visual_c)
        update_env(self.visual_studio)
        update_env(self.windows_sdk)
        update_env(self.dot_net)

        env['Path'] += ';' + path

        return env

    def __str__(self):
        template = (
            'Machine architecture: {machine_architecture}\n'
            'Build architecture: {architecture}\n'
            '\n'
            '== Windows SDK ================================================\n'
            '   version:     {target_platform}\n'
            '   sdk version: {windows_sdk_version}\n'
            '   path:        {target_platform_path}\n'
            '\n'
            '   -- Universal CRT -------------------------------------------\n'
            '      path: {ucrt_sdk_directory}\n'
            '   -- ATLMFC --------------------------------------------------\n'
            '      path:         {atlmfc_path}\n'
            '      include path: {atlmfc_include_path}\n'
            '      lib path:     {atlmfc_lib_path}\n'
            '\n'
            '== Extension SDK ==============================================\n'
            '   path: {extension_sdk_directory}\n'
            '\n'
            '== TypeScript =================================================\n'
            '   path: {type_script_path}\n'
            '\n'
            '== HTML Help ==================================================\n'
            '   path: {html_help_path}\n'
            '\n'
            '== .NET =======================================================\n'
            '   version:    {target_framework}\n'
            '\n'
            '   -- x86 -----------------------------------------------------\n'
            '      version: {framework_version_32}\n'
            '      path:    {framework_dir_32}\n'
            '   -- x64 -----------------------------------------------------\n'
            '      version: {framework_version_64}\n'
            '      path:    {framework_dir_64}\n'
            '   -- NETFX ---------------------------------------------------\n'
            '      path:         {net_fx_tools_directory}\n'
            '      x86 exe path: {executable_path_x86}\n'
            '      x64 exe path: {executable_path_x64}\n'
            '\n'
            '== Visual C ===================================================\n'
            '   version: {visual_c_version}\n'
            '   path:    {visual_c_path}\n'
            '\n'
            '   -- Tools ---------------------------------------------------\n'
            '      version:     {tools_version}\n'
            '      path:        {tools_install_path}\n'
            '      redist path: {vc_tools_redist_path}\n'
            '   -- F# ------------------------------------------------------\n'
            '      path: {f_sharp_path}\n'
            '   -- DLL -----------------------------------------------------\n'
            '      version: {platform_toolset}-{msvc_dll_version}\n'
            '      path:    {msvc_dll_path}\n'
            '\n'
            '== MSBuild ====================================================\n'
            '   version: {msbuild_version}\n'
            '   path:    {msbuild_path}\n'
            '\n'
            '== Python =====================================================\n'
            '  version: {py_version}\n'
            '  architecture: {py_architecture}\n'
            '  library: {py_dependency}\n'
            '  libs: {py_libraries}\n'
            '  includes: {py_includes}\n'
            '\n'
        )
        return template.format(
            machine_architecture=self.machine_architecture,
            architecture=self.platform,
            target_platform=self.windows_sdk.version,
            windows_sdk_version=self.windows_sdk.sdk_version,
            target_platform_path=self.windows_sdk.directory,
            target_framework=self.dot_net.version,
            framework_version_32=self.dot_net.version_32,
            framework_dir_32=self.dot_net.directory_32,
            framework_version_64=self.dot_net.version_64,
            framework_dir_64=self.dot_net.directory_64,
            visual_c_version=self.visual_c.version,
            visual_c_path=self.visual_c.install_directory,
            tools_version=self.visual_c.tools_version,
            tools_install_path=self.visual_c.tools_install_directory,
            vc_tools_redist_path=self.visual_c.tools_redist_directory,
            platform_toolset=self.visual_c.toolset_version,
            msvc_dll_version=self.visual_c.msvc_dll_version,
            msvc_dll_path=self.visual_c.msvc_dll_path,
            msbuild_version=self.visual_c.msbuild_version,
            msbuild_path=self.visual_c.msbuild_path,
            py_version=self.python.version,
            py_architecture=self.python.architecture,
            py_dependency=self.python.dependency,
            py_libraries=self.python.libraries,
            py_includes=self.python.includes,
            f_sharp_path=self.visual_c.f_sharp_path,
            html_help_path=self.visual_c.html_help_path,
            atlmfc_lib_path=self.visual_c.atlmfc_lib_path,
            atlmfc_include_path=self.visual_c.atlmfc_include_path,
            atlmfc_path=self.visual_c.atlmfc_path,
            extension_sdk_directory=self.windows_sdk.extension_sdk_directory,
            ucrt_sdk_directory=self.windows_sdk.ucrt_sdk_directory,
            type_script_path=self.windows_sdk.type_script_path,
            net_fx_tools_directory=self.dot_net.net_fx_tools_directory,
            executable_path_x64=self.dot_net.executable_path_x64,
            executable_path_x86=self.dot_net.executable_path_x86,
        )


if __name__ == '__main__':
    e = Environment()
    print(e)
    print('\n\n')
    for k, v in e:
        if os.pathsep in v:
            print(k + ':')
            for itm in v.split(os.pathsep):
                print('   ', itm)
        else:
            print(k + ':', v)
        print()
