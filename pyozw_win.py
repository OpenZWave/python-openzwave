# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
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

import sys
import os
import platform
import shutil
from pyozw_version import pyozw_version

try:
    _winreg = __import__('_winreg')
except ImportError:
    _winreg = __import__('winreg')


from subprocess import Popen, PIPE

# this is simply to show that you can build using only VS2017 as a requirement.
VS2017_VCVARSALL = r'"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsall.bat"'

WIN64 = '64' in platform.machine()
PYTHON64 = platform.architecture()[0] == '64bit' and WIN64
ARCH = 'x64' if PYTHON64 else 'x86'


try:
    PY3 = not unicode
except NameError:
    PY3 = True

TOOLSETS = {
    15.0: ['v141', '15.0'],  # vs2017
    14.0: ['v140', '14.0'],  # vs2015
    10.0: ['v100', '4.0'],  # vs2010
    4.0:  ['v90', '4.0'],  # vs2008
}


def setup_build_env_2017():
    proc = Popen(
        VS2017_VCVARSALL + ' ' + ARCH + ' && set',
        shell=True,
        stdout=PIPE,
        stderr=PIPE
    )

    test_env = {}
    for line in proc.stdout:
        if PY3:
            line = line.decode("utf-8")

        if '=' in line:
            key, value = line.split('=', 1)
            test_env[key.strip()] = value.strip()

    for key, value in list(test_env.items()):
        if str(os.environ.get(key, None)) != value:
            os.environ[key] = value

    os.environ['DISTUTILS_USE_SDK'] = '1'


# comment this line to run normally.
setup_build_env_2017()


def _get_reg_value(path, key):
    d = _read_reg_values(path)
    if key in d:
        return d[key]
    return ''


def _read_reg_keys(key):
    try:
        handle = _winreg.OpenKeyEx(
            _winreg.HKEY_LOCAL_MACHINE,
            'SOFTWARE\\Wow6432Node\\Microsoft\\' + key
        )
    except _winreg.error:
        return []
    res = []

    for i in range(_winreg.QueryInfoKey(handle)[0]):
        res += [_winreg.EnumKey(handle, i)]

    return res


def _read_reg_values(key):
    try:
        handle = _winreg.OpenKeyEx(
            _winreg.HKEY_LOCAL_MACHINE,
            'SOFTWARE\\Wow6432Node\\Microsoft\\' + key
        )
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


def get_environment():
    from setuptools.msvc import (
        msvc9_query_vcvarsall,
        EnvironmentInfo,
        msvc14_get_vc_env
    )

    py_version = sys.version_info[:2]

    if py_version >= (3, 5):
        env = msvc14_get_vc_env(ARCH)
        msbuild_version = 14.0
        env_info = EnvironmentInfo(ARCH)
        msbuild_path = _find_file(
            'MSBuild.exe',
            env_info.MSBuild[0]
        )[0]

        sdks = ('10.0', '8.1', '8.1A', '8.0', '8.0A')
        solution_dest = 'vs2015'

    elif (3, 5) > py_version >= (3, 3):
        env = msvc9_query_vcvarsall(10.0, ARCH)
        msbuild_version = 4.0
        msbuild_path = _get_reg_value(
            'MSBuild\\4.0',
            'MSBuildOverrideTasksPath'
        )

        if msbuild_path:
            msbuild_path = _find_file(
                'MSBuild.exe',
                msbuild_path
            )[0]

        sdks = ('7.1', '7.0A')
        solution_dest = 'vs2010'

    elif (3, 3) > py_version >= (2, 6):
        env = msvc9_query_vcvarsall(9.0, ARCH)
        msbuild_version = 4.0
        msbuild_path = _get_reg_value(
            'MSBuild\\4.0',
            'MSBuildOverrideTasksPath'
        )

        if msbuild_path:
            msbuild_path = _find_file(
                'MSBuild.exe',
                msbuild_path
            )[0]

        sdks = ('6.1', '6.1A', '6.0A')
        solution_dest = 'vs2008'

    else:
        raise RuntimeError(
            'This library does not support python versions < 2.6'
        )

    for sdk in sdks:
        sdk_version = _get_reg_value(
            'Microsoft SDKs\\Windows\\v' + sdk,
            'ProductVersion'
        )
        if sdk_version:
            sdk_installation_folder = _get_reg_value(
                'Microsoft SDKs\\Windows\\v' + sdk,
                'InstallationFolder'
            )
            target_platform = sdk_version
            os.environ['WindowsSdkDir'] = sdk_installation_folder
            break
    else:
        raise RuntimeError('Unable to locate suitable SDK %s' % (sdks,))

    platform_toolset, tools_version = TOOLSETS[msbuild_version]

    return (
        env,
        msbuild_version,
        msbuild_path,
        sdk_installation_folder,
        target_platform,
        platform_toolset,
        tools_version,
        solution_dest
    )


def _find_file(file_name, path):
    res = []

    for root, dirs, files in os.walk(path):
        if (
            ((PYTHON64 and 'amd64' in root) or 'amd64' not in root) and
            file_name in files
        ):
            res.append(os.path.join(root, file_name))
    return res


def setup_build_environment(openzwave, build_type):
    if 'DISTUTILS_USE_SDK' in os.environ:
        target_platform = os.environ['WINDOWSSDKVERSION'].replace('\\', '')

        if 'VS150COMNTOOLS' in os.environ:
            msbuild_version = 15.0
            solution_dest = 'vs2017'

        elif 'VS140COMNTOOLS' in os.environ:
            msbuild_version = 14.0
            solution_dest = 'vs2015'
        else:
            raise RuntimeError

        msbuild_path = _find_file('MSBuild.exe', os.environ['VSINSTALLDIR'])[0]
        platform_toolset, tools_version = TOOLSETS[msbuild_version]
        sdk_installation_folder = os.environ['WINDOWSSDKVERBINPATH']
        os.environ['MSSDK'] = sdk_installation_folder

    else:
        (
            env,
            msbuild_version,
            msbuild_path,
            sdk_installation_folder,
            target_platform,
            platform_toolset,
            tools_version,
            solution_dest
        ) = get_environment()

        if 'WINDOWSSDKVERBINPATH' in env:
            sdk_installation_folder = env['WINDOWSSDKVERBINPATH']

        env['MSSDK'] = sdk_installation_folder
        env['DISTUTILS_USE_SDK'] = '1'

        for key, value in env.items():
            os.environ[key] = value

        if 'VS150COMNTOOLS' in os.environ and msbuild_version == 14.0:
            platform_toolset = 'v141'
            tools_version = '15.0'
            msbuild_version = 15.0
            solution_dest = 'vs2017'

        if 'WINDOWSSDKLIBVERSION' in os.environ:
            target_platform = (
                os.environ['WINDOWSSDKLIBVERSION'].replace('\\', '')
            )

    if not msbuild_path:
        raise RuntimeError(
            'Unable to locate MSBuild to compile OpenZWave'
        )

    project_base_path = os.path.abspath(
        os.path.join(
            openzwave,
            'cpp',
            'build',
            'windows'
        )
    )

    project_path = os.path.join(project_base_path, solution_dest)

    if PYTHON64:
        build_path = os.path.join(project_path, 'x64', build_type)
    else:
        build_path = os.path.join(project_path, build_type)

    if not os.path.exists(project_path):
        shutil.copytree(
            os.path.join(project_base_path, 'vs2010'),
            project_path
        )

    print('Updating VS solution please wait.')

    if update_vs_project(
        os.path.join(project_path, 'OpenZWave.vcxproj'),
        tools_version,
        platform_toolset,
        target_platform
    ):
        with open(os.path.join(project_path, 'OpenZWave.sln'), 'r') as f:
            sln = str(f.read()).replace('\r', '')

        if GLOBAL_SELECTION_TEMPLATE not in sln:
            sln = sln.replace(
                GLOBAL_SELECTION_KEY,
                GLOBAL_SELECTION_TEMPLATE
            )

        with open(os.path.join(project_path, 'OpenZWave.sln'), 'w') as f:
            f.write(sln)

    solution_path = os.path.join(project_path, 'OpenZWave.sln')

    return (
        solution_path,
        build_path,
        msbuild_path,
        msbuild_version,
        target_platform,
        platform_toolset,
        tools_version,
        sdk_installation_folder
    )


def update_vs_project(path, tools_version, platform_toolset, target_platform):
    from xml.etree import ElementTree

    vcxproj_xmlns = 'http://schemas.microsoft.com/developer/msbuild/2003'
    ElementTree.register_namespace('', vcxproj_xmlns)

    with open(path, 'r') as f:
        vcxproj = f.read()

    # the original xml file contains some characters that the xml parser
    # does not like, these are non human readable characters and they do not
    # need to exist. So we remove them.
    for char in (187, 191, 239):
        vcxproj = vcxproj.replace(chr(char), '')

    root = ElementTree.fromstring(vcxproj)

    vcxproj_xmlns = '{' + vcxproj_xmlns + '}'

    # there are only 3 things that need to get changed once the solution has
    # been fully updated. the tools version, the platform teeolset
    # and the windows target platform. if a cached version of openzwave is used
    # there is no need to create a whole new solution. so what we do is we set
    # an attribute in the root of the xml to inform us if the file has been
    # upgraded already.

    root.attrib['ToolsVersion'] = tools_version

    for node in root.findall(vcxproj_xmlns + 'PropertyGroup'):
        if (
            'Label' in node.attrib and
            node.attrib['Label'] == 'Configuration'
        ):
            for sub_node in node:
                if (
                    sub_node.tag.replace(vcxproj_xmlns, '') ==
                    'PlatformToolset'
                ):
                    sub_node.text = platform_toolset
                    break
            else:
                sub_node = ElementTree.Element('PlatformToolset')
                sub_node.text = platform_toolset
                node.append(sub_node)

    for node in root.findall(vcxproj_xmlns + 'PropertyGroup'):
        if 'Label' in node.attrib and node.attrib['Label'] == 'Globals':
            for sub_node in node:
                if (
                    sub_node.tag.replace(vcxproj_xmlns, '') ==
                    'WindowsTargetPlatformVersion'
                ):
                    sub_node.text = target_platform
                    break
            else:
                sub_node = ElementTree.Element('WindowsTargetPlatformVersion')
                sub_node.text = target_platform
                node.append(sub_node)

    # this function is the core of upgrading the solution. It burrows down
    # into a node through each layer and makes a copy. this copy gets modified
    # to become an x64 version. the copy gets returned and then added to the
    # xml file

    def iter_node(old_node):
        new_node = ElementTree.Element(old_node.tag)
        if old_node.text is not None:
            new_node.text = old_node.text.replace('Win32', 'x64')

        for key, value in old_node.attrib.items():
            new_node.attrib[key] = value.replace('Win32', 'x64')
        for old_sub_node in old_node:
            new_node.append(iter_node(old_sub_node))
        return new_node

    # here is the testing to se if the file has been updated before.
    if 'PythonOpenZWave' not in root.attrib:
        update = True
        root.attrib['PythonOpenZWave'] = 'True'
        i = 0

        for node in root[:]:
            tag = node.tag.replace(vcxproj_xmlns, '')

            if (
                tag == 'ItemGroup' and
                'Label' in node.attrib and
                node.attrib['Label'] == 'ProjectConfigurations'
            ):
                for sub_item in node[:]:
                    node.append(iter_node(sub_item))

            if (
                tag == 'PropertyGroup' and
                'Label' in node.attrib and
                node.attrib['Label'] == 'Configuration'
            ):
                root.insert(i, iter_node(node))
                i += 1

            if (
                tag == 'ImportGroup' and
                'Label' in node.attrib and
                node.attrib['Label'] == 'PropertySheets'
            ):
                root.insert(i, iter_node(node))
                i += 1

            if (
                tag == 'PropertyGroup' and
                not node.attrib.keys()
            ):
                j = 0
                for sub_item in node[:]:
                    if (
                        sub_item.tag.replace(vcxproj_xmlns, '') !=
                        '_ProjectFileVersion'
                    ):
                        node.insert(j, iter_node(sub_item))
                    j += 1

            if tag == 'ItemDefinitionGroup':
                root.insert(i, iter_node(node))
                i += 1
            i += 1
    else:
        update = False

    with open(path, 'w')as f:
        f.write(xml_tostring(root, vcxproj_xmlns))

    # we return if the file was updated or not. this is a flag that tells up
    # if we need to update the sln file.
    return update


# this is a custom xml writer. it recursively iterates through an
# ElementTree object creating a formatted string that is as close as i can
# get it to what Visual Studio creates. I did this for consistency as well
# as ease of bug testing

def xml_tostring(node, xmlns, indent=''):
    tag = node.tag.replace(xmlns, '')
    no_text = node.text is None or not node.text.strip()

    if indent:
        output = ''
    else:
        output = '<?xml version="1.0" encoding="utf-8"?>\n'
        if xmlns:
            node.attrib['xmlns'] = xmlns.replace('{', '').replace('}', '')

    if no_text and not list(node) and not node.attrib.keys():
        output += '{0}<{1} />\n'.format(indent, tag)
    else:
        output += '{0}<{1}'.format(indent, tag)

        for key in sorted(node.attrib.keys()):
            output += ' {0}="{1}"'.format(key, str(node.attrib[key]))

        if not list(node) and no_text:
            output += ' />\n'
        elif not no_text and not list(node):
            output += '>{0}</{1}>\n'.format(node.text, tag)
        elif list(node) and no_text:
            output += '>\n'
            for item in node:
                output += xml_tostring(item, xmlns, indent + '  ')
            output += '{0}</{1}>\n'.format(indent, tag)
        else:
            output += '>\n  {0}{1}\n'.format(indent, node.text)
            for item in node:
                output += xml_tostring(item, xmlns, indent + '  ')
            output += '{0}</{1}>\n'.format(indent, tag)
    return output


# because we no longer use devenv in favor of msbuild there are only 2 commands
# needed.
# one for clean and the other to build
def get_clean_command(msbuild_path, solution_path, build_type, arch, **_):
    clean_template = (
        '"{msbuild_path}" '
        '"{solution_path}" '
        '/property:Configuration={build_type} '
        '/property:Platform={arch} '
        '/t:Clean '
    )
    clean_command = clean_template.format(
        msbuild_path=msbuild_path,
        solution_path=solution_path,
        build_type=build_type,
        arch=arch
    )

    return clean_command


def get_build_command(msbuild_path, solution_path, build_type, arch, **_):
    build_template = (
        '"{msbuild_path}" '
        '"{solution_path}" '
        '/property:Configuration={build_type} '
        '/property:Platform={arch} '
        '/t:Build'
    )

    build_command = build_template.format(
        msbuild_path=msbuild_path,
        solution_path=solution_path,
        build_type=build_type,
        arch=arch
    )

    return build_command


def get_system_context(
    ctx,
    options,
    openzwave="openzwave",
    static=False,
    debug=False
):


    if debug:
        print("get_system_context for windows")

    # one feature i added is building a debugging version, this is only going
    # to happen if sys.executable ends with _d which identifies that the python
    # interpreter is a debugging build.

    if static:
        if os.path.splitext(sys.executable)[0].endswith('_d'):
            options['build_type'] = 'Debug'
            ctx['define_macros'] += [('_DEBUG', 1)]
            ctx['libraries'] += ["setupapi", "msvcrtd", "ws2_32", "dnsapi"]
        else:
            options['build_type'] = 'Release'
            ctx['libraries'] += ["setupapi", "msvcrt", "ws2_32", "dnsapi"]
    else:
        if os.path.splitext(sys.executable)[0].endswith('_d'):
            options['build_type'] = 'DebugDLL'
            ctx['define_macros'] += [('_DEBUG', 1)]
            ctx['libraries'] += ["setupapi", "msvcrtd", "ws2_32", "dnsapi"]
        else:
            options['build_type'] = 'ReleaseDLL'
            ctx['libraries'] += ["setupapi", "msvcrt", "ws2_32", "dnsapi"]

    if PYTHON64:
        options['arch'] = "x64"
    else:
        options['arch'] = 'Win32'

    (
        solution_path,
        build_path,
        msbuild_path,
        msbuild_version,
        target_platform,
        platform_toolset,
        tools_version,
        sdk_installation_folder
    ) = setup_build_environment(openzwave, options['build_type'])

    options['msbuild_path'] = msbuild_path
    options['solution_path'] = solution_path
    options['build_path'] = build_path
    options['msbuild_version'] = msbuild_version
    options['target_platform'] = target_platform
    options['platform_toolset'] = platform_toolset
    options['tools_version'] = tools_version
    options['sdk_installation_folder'] = sdk_installation_folder

    if debug:
        print('Platform: %s' % target_platform)
        print('Platform architecture %s' % ARCH)
        print('Platform toolset: %s' % platform_toolset)
        print('MSBuild path: %s' % msbuild_path)
        print('MSBuild version: %0.1f' % msbuild_version)
        print('MSBuild tools version: %s' % tools_version)
        print('SDK installation path: %s' % sdk_installation_folder)
        print("Found options %s" % options)

    cpp_path = os.path.join(openzwave, 'cpp')
    src_path = os.path.join(cpp_path, 'src')

    if static:
        ctx['extra_objects'] = [os.path.join(build_path, 'OpenZWave.lib')]

        ctx['include_dirs'] += [
            src_path,
            os.path.join(src_path, 'value_classes'),
            os.path.join(src_path, 'platform'),
            os.path.join(cpp_path, 'build', 'windows'),
            build_path,
        ]
    else:
        ctx['libraries'] += ["OpenZWave"]

        ctx['extra_compile_args'] += [
            src_path,
            os.path.join(src_path, 'value_classes'),
            os.path.join(src_path, 'platform'),
        ]

    ctx['define_macros'] += [
        ('CYTHON_FAST_PYCCALL', 1),
        ('_MT', 1),
        ('_DLL', 1)
    ]


GLOBAL_SELECTION_TEMPLATE = '''		Debug|x64 = Debug|x64
		DebugDLL|x64 = DebugDLL|x64
		Release|x64 = Release|x64
		ReleaseDLL|x64 = ReleaseDLL|x64
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Debug|x64.ActiveCfg = Debug|x64
		{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Debug|x64.Build.0 = Debug|x64
		{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.DebugDLL|x64.ActiveCfg = DebugDLL|x64
		{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.DebugDLL|x64.Build.0 = DebugDLL|x64
		{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Release|x64.ActiveCfg = Release|x64
		{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Release|x64.Build.0 = Release|x64
		{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.ReleaseDLL|x64.ActiveCfg = ReleaseDLL|x64
		{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.ReleaseDLL|x64.Build.0 = ReleaseDLL|x64'''


GLOBAL_SELECTION_KEY = '''	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution'''


def get_openzwave(opzw_dir):
    url = 'https://codeload.github.com/OpenZWave/open-zwave/zip/master'

    from io import BytesIO
    try:
        from urllib2 import urlopen
    except ImportError:
        from urllib.request import urlopen

    import zipfile

    base_path = os.path.dirname(__file__)

    print('Downloading openzwave...')

    req = urlopen(url)
    dest_file = BytesIO(req.read())
    dest_file.seek(0)

    zip_ref = zipfile.ZipFile(dest_file, 'r')
    zip_ref.extractall(base_path)
    zip_ref.close()
    dest_file.close()

    os.rename(
        os.path.join(base_path, zip_ref.namelist()[0]),
        opzw_dir
    )


if __name__ == '__main__':
    from subprocess import Popen, PIPE
    from setuptools import setup
    from distutils.extension import Extension

    print("Start pyozw_win")

    ctx = dict(
        name='libopenzwave',
        sources=['src-lib\\libopenzwave\\libopenzwave.pyx'],
        include_dirs=['src-lib\\libopenzwave'],
        define_macros=[
            ('PY_LIB_VERSION', pyozw_version),
            ('PY_SSIZE_T_CLEAN', 1),
            ('PY_LIB_FLAVOR', 'dev'),
            ('PY_LIB_BACKEND', 'cython')
        ],
        libraries=[],
        extra_objects=[],
        extra_compile_args=[],
        extra_link_args=[],
        language='c++'
    )

    ozw_path = os.path.abspath('openzwave')

    if not os.path.exists(ozw_path):
        get_openzwave('openzwave')

    options = dict()

    get_system_context(
        ctx,
        options,
        openzwave=ozw_path,
        static=True,
        debug=True
    )

    clean = get_clean_command(**options)
    build = get_build_command(**options)

    def run(command):
        print('Running command:', command)
        proc = Popen(
            command,
            shell=True,
            stdout=PIPE,
            stderr=PIPE,
            cwd=os.path.split(options['solution_path'])[0],
        )

        if PY3:
            dummy_return = b''
        else:
            dummy_return = ''

        for line in iter(proc.stdout.readline, dummy_return):
            if line and PY3:
                sys.stdout.write(line.decode("utf-8"))
            elif line:
                sys.stdout.write(line)

        errcode = proc.returncode
        print('\n\nerrcode', errcode, '\n\n')

        for line in iter(proc.stderr.readline, dummy_return):
            if line and PY3:
                sys.stdout.write(line.decode("utf-8"))
            elif line:
                sys.stdout.write(line)

    # run(clean)
    # run(build)

    print(
        'Library built in %s using compiler %s for arch %s' %
        (options['build_path'], options['msbuild_path'], options['arch'])
    )

    setup(
        script_args=['build_ext'],
        version=pyozw_version,
        name='libopenzwave',
        description='libopenzwave',
        verbose=1,
        ext_modules=[Extension(**ctx)],
    )
