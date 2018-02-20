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

import os
import sys
import platform
import shutil
import subprocess
import threading

try:
    import winreg as _winreg
except ImportError:
    import _winreg


WIN64 = '64' in platform.machine()
PYTHON64 = platform.architecture()[0] == '64bit' and WIN64

RegOpenKeyEx = _winreg.OpenKeyEx
RegEnumKey = _winreg.EnumKey
RegEnumValue = _winreg.EnumValue
RegError = _winreg.error

current_settings = dict()


def check_variable(var):
    if os.pathsep in var:
        values = []
        var = var.lower()
        for itm in var.split(os.pathsep):
            if itm and itm not in values:
                values += [itm]
        var = os.pathsep.join(values)
    return var


for k, v in os.environ.items():
    current_settings[k.lower()] = check_variable(v)


if PYTHON64:
    ARCH = "64"
else:
    ARCH = '32'

_vc_vars = None


def find_vcvars(vs_path):
    global _vc_vars

    if _vc_vars is None:
        print("Windows build setup starting.")
        vcvars = 'vcvars%s.bat' % ARCH

        event = threading.Event()

        def run():
            global _vc_vars
            for root, dirs, files in os.walk(vs_path):
                for f in files:
                    if f.lower() == vcvars:
                        _vc_vars = os.path.join(root, vcvars)
                        break
                else:
                    continue
                break
            event.set()

        t = threading.Thread(target=run)
        t.daemon = True
        sys.stdout.write('Locating {0}...'.format(vcvars))
        t.start()

        while not event.isSet():
            sys.stdout.write('.')
            event.wait(1)
        sys.stdout.write('\n')

    return _vc_vars


_vs_path = None

if WIN64:
    def get_vs_path():
        global _vs_path
        if _vs_path is None:
            handle = RegOpenKeyEx(
                _winreg.HKEY_LOCAL_MACHINE,
                r'SOFTWARE\Wow6432Node\Microsoft\VisualStudio\SxS\VS7'
            )

            max_ver = 0.0
            _vs_path = ''
            i = 0
            while True:
                try:
                    name, value, _ = RegEnumValue(handle, i)
                except RegError:
                    break

                try:
                    name = float(name)
                    if name > max_ver:
                        max_ver = name
                        _vs_path = value
                except ValueError:
                    pass

                i += 1
        return _vs_path
else:
    def get_vs_path():
        return ''


def setup_build_environment():
    vs_path = get_vs_path()
    new_settings = dict()

    if vs_path:
        vs_path = find_vcvars(os.path.join(vs_path, 'VC'))
        if vs_path:
            print("Setting up Visual Studio build environment.")
            popen = subprocess.Popen(
                '"%s" & set' % vs_path,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                stdout, stderr = popen.communicate()
                if popen.wait() == 0:
                    stdout = stdout.decode("mbcs")

                    for line in stdout.split("\n"):
                        if '=' not in line:
                            continue

                        line = line.strip()
                        k1, v1 = line.split('=', 1)
                        k1 = k.lower()

                        if (
                            k1 not in current_settings or
                            current_settings[k1] != v1
                        ):
                            new_settings[k1] = check_variable(v1)

            finally:
                popen.stdout.close()
                popen.stderr.close()

            for key, value in new_settings.items():
                os.environ[key] = value

            os.environ['MSSDK'] = vs_path
            os.environ['DISTUTILS_USE_SDK'] = '1'

        else:
            raise RuntimeError(
                'vcvars32.bat or vcvars64.bat could not be located.'
            )
    else:
        raise RuntimeError('Visual Studio could not be located.')


def copy_files(src, dst):
    try:
        os.makedirs(dst)
    except WindowsError:
        pass

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        except WindowsError:
            pass


def find_file(file_name, path):
    event = threading.Event()
    res = ['']

    def run():
        for root, dirs, files in os.walk(path):
            if (
                ((PYTHON64 and 'amd64' in root) or 'amd64' not in root) and
                file_name in files
            ):
                res[0] = os.path.join(root, file_name)
                break
        event.set()

    t = threading.Thread(target=run)
    t.daemon = True
    sys.stdout.write('Locating {0}...'.format(file_name))
    t.start()

    while not event.isSet():
        sys.stdout.write('.')
        event.wait(1)
    sys.stdout.write('\n')

    return res[0]


def find_ms_tools(debug=False, conf='Release', template=None):
    if PYTHON64:
        arch = "x64"
    else:
        arch = 'Win32'

    project_dir = os.path.abspath(r'openzwave\cpp\build\windows')
    source_dir = os.path.join(project_dir, 'vs2010')

    program_files = os.path.expandvars('%PROGRAMFILES%')

    if not program_files.endswith('(x86)'):
        program_files += ' (x86)'

    dev_env = find_file("devenv.com", get_vs_path())

    if dev_env:
        project_mapping = {
            "15.0": "2017",
            "14.0": "2015",
            "12.0": "2013",
            "11.0": "2012",
            "10.0": "2010",
            "9.0":  "2008"
        }
        for key, value in project_mapping.items():
            if key in dev_env or value in dev_env:
                project = 'vs' + value
                break
        else:
            project = 'vs2010'

        project_dir = os.path.join(project_dir, project)

        if PYTHON64:
            project_dir = os.path.join(project_dir, 'x64')

        build_path = os.path.join(project_dir, conf)

        if debug:
            print("Found arch %s" % arch)
            print("Found Visual Studios in %s" % get_vs_path())
            print("Found compilers %s for project %s" % (dev_env, project))

        if template:

            event = threading.Event()

            def run():
                template.get_openzwave()
                copy_files(
                    os.path.join(template.openzwave, 'open-zwave-master'),
                    template.openzwave
                )
                event.set()

            t = threading.Thread(target=run)
            t.daemon = True
            sys.stdout.write('Downloading openzwave...')
            t.start()

            while not event.isSet():
                event.wait(0.6)
                sys.stdout.write('.')
            sys.stdout.write('\n')

        if (
            ('2010' not in project_dir and '2008' not in project_dir) or
            PYTHON64
        ):
            print('Copying openzwave Visual Studio solution.')
            copy_files(source_dir, project_dir)

        if PYTHON64:
            print('Modifying openzwave Visual Studio solution.')

            with open(os.path.join(project_dir, 'OpenZWave.vcxproj'), 'r') as f:
                vcxproj = f.read()

            with open(os.path.join(project_dir, 'OpenZWave.sln'), 'r') as f:
                sln = f.read()

            if IMPORT_GROUP_TEMPLATE not in vcxproj:
                vcxproj.replace(
                    IMPORT_GROUP_KEY,
                    IMPORT_GROUP_TEMPLATE
                )

            if PROPERTY_GROUP_TEMPLATE not in vcxproj:
                vcxproj.replace(
                    PROPERTY_GROUP_KEY,
                    PROPERTY_GROUP_TEMPLATE
                )

            if ITEM_DEFINITION_GROUP_TEMPLATE not in vcxproj:
                vcxproj.replace(
                    ITEM_DEFINITION_GROUP_KEY,
                    ITEM_DEFINITION_GROUP_TEMPLATE
                )


            if GLOBAL_SELECTION_TEMPLATE not in sln:
                sln.replace(
                    GLOBAL_SELECTION_KEY,
                    GLOBAL_SELECTION_TEMPLATE
                )

            with open(os.path.join(project_dir, 'OpenZWave.vcxproj'), 'w') as f:
                f.write(vcxproj)

            with open(os.path.join(project_dir, 'OpenZWave.sln'), 'w') as f:
                f.write(sln)

        project_dir = os.path.join(project_dir, 'OpenZWave.sln')

        return arch, project, dev_env, build_path, project_dir

    else:
        raise RuntimeError('Unable to locate Visual Studio')

    #~ print(msbuild)
    #~ print(projects)
    #~ print(msbuild)
    #~ print(arch)


TOOLS_VERSION_KEY = r'''ToolsVersion="4.0"'''
TOOLS_VERSION_TEMPLATE = r'''ToolsVersion="{version}"'''

IMPORT_GROUP_TEMPLATE = r'''  <ImportGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="PropertySheets">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'" Label="PropertySheets">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Condition="'$(Configuration)|$(Platform)'=='DebugDLL|x64'" Label="PropertySheets">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Condition="'$(Configuration)|$(Platform)'=='ReleaseDLL|x64'" Label="PropertySheets">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <PropertyGroup Label="UserMacros" />
'''

IMPORT_GROUP_KEY = r'''  <PropertyGroup Label="UserMacros" />'''

PROPERTY_GROUP_TEMPLATE = r''' <IntDir Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">$(Configuration)\</IntDir>
    <IntDir Condition="'$(Configuration)|$(Platform)'=='DebugDLL|x64'">$(Configuration)\</IntDir>
    <IntDir Condition="'$(Configuration)|$(Platform)'=='ReleaseDLL|x64'">$(Configuration)\</IntDir>
    <IntDir Condition="'$(Configuration)|$(Platform)'=='Release|x64'">$(Configuration)\</IntDir>
    <CodeAnalysisRuleSet Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">AllRules.ruleset</CodeAnalysisRuleSet>
    <CodeAnalysisRuleSet Condition="'$(Configuration)|$(Platform)'=='DebugDLL|x64'">AllRules.ruleset</CodeAnalysisRuleSet>
    <CodeAnalysisRuleSet Condition="'$(Configuration)|$(Platform)'=='ReleaseDLL|x64'">AllRules.ruleset</CodeAnalysisRuleSet>
    <CodeAnalysisRules Condition="'$(Configuration)|$(Platform)'=='Debug|x64'" />
    <CodeAnalysisRules Condition="'$(Configuration)|$(Platform)'=='DebugDLL|x64'" />
    <CodeAnalysisRules Condition="'$(Configuration)|$(Platform)'=='ReleaseDLL|x64'" />
    <CodeAnalysisRuleAssemblies Condition="'$(Configuration)|$(Platform)'=='Debug|x64'" />
    <CodeAnalysisRuleAssemblies Condition="'$(Configuration)|$(Platform)'=='DebugDLL|x64'" />
    <CodeAnalysisRuleAssemblies Condition="'$(Configuration)|$(Platform)'=='ReleaseDLL|x64'" />
    <CodeAnalysisRuleSet Condition="'$(Configuration)|$(Platform)'=='Release|x64'">AllRules.ruleset</CodeAnalysisRuleSet>
    <CodeAnalysisRules Condition="'$(Configuration)|$(Platform)'=='Release|x64'" />
    <CodeAnalysisRuleAssemblies Condition="'$(Configuration)|$(Platform)'=='Release|x64'" />
    <TargetName Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">$(ProjectName)</TargetName>
    <TargetName Condition="'$(Configuration)|$(Platform)'=='DebugDLL|x64'">$(ProjectName)d</TargetName>
    <TargetName Condition="'$(Configuration)|$(Platform)'=='ReleaseDLL|x64'">$(ProjectName)</TargetName>
    <TargetExt Condition="'$(Configuration)|$(Platform)'=='ReleaseDLL|x64'">.dll</TargetExt>
    <TargetExt Condition="'$(Configuration)|$(Platform)'=='DebugDLL|x64'">.dll</TargetExt>
  </PropertyGroup>'''

PROPERTY_GROUP_KEY = r'''  </PropertyGroup>'''

ITEM_DEFINITION_GROUP_TEMPLATE = r'''<ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <ClCompile>
      <Optimization>Disabled</Optimization>
      <PreprocessorDefinitions>WIN32;_DEBUG;_LIB;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <BasicRuntimeChecks>EnableFastChecks</BasicRuntimeChecks>
      <RuntimeLibrary>MultiThreadedDebugDLL</RuntimeLibrary>
      <PrecompiledHeader>
      </PrecompiledHeader>
      <WarningLevel>Level3</WarningLevel>
      <DebugInformationFormat>ProgramDatabase</DebugInformationFormat>
      <AdditionalIncludeDirectories>..\..\..\src;..\..\..\tinyxml;..\..\..\hidapi\hidapi;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
    </ClCompile>
    <Lib>
      <OutputFile>$(OutDir)\$(ProjectName).lib</OutputFile>
      <AdditionalDependencies>setupapi.lib</AdditionalDependencies>
      <TargetMachine>MachineX86</TargetMachine>
    </Lib>
    <PreBuildEvent>
      <Command>del ..\winversion.cpp
CALL "$(ProjectDir)\..\GIT-VS-VERSION-GEN.bat" "$(ProjectDir)\" "..\winversion.cpp"
exit 0</Command>
    </PreBuildEvent>
    <PreBuildEvent>
      <Message>Export GIT Revision</Message>
    </PreBuildEvent>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='DebugDLL|x64'">
    <ClCompile>
      <Optimization>Disabled</Optimization>
      <PreprocessorDefinitions>WIN32;_DEBUG;_LIB;OPENZWAVE_MAKEDLL;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <BasicRuntimeChecks>EnableFastChecks</BasicRuntimeChecks>
      <RuntimeLibrary>MultiThreadedDebugDLL</RuntimeLibrary>
      <PrecompiledHeader>
      </PrecompiledHeader>
      <WarningLevel>Level3</WarningLevel>
      <DebugInformationFormat>ProgramDatabase</DebugInformationFormat>
      <DisableSpecificWarnings>4251</DisableSpecificWarnings>
      <AdditionalIncludeDirectories>..\..\..\src;..\..\..\tinyxml;..\..\..\hidapi\hidapi;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
    </ClCompile>
    <Lib>
      <OutputFile>$(OutDir)\$(ProjectName).dll</OutputFile>
      <AdditionalDependencies>setupapi.lib</AdditionalDependencies>
      <TargetMachine>MachineX86</TargetMachine>
    </Lib>
    <Link>
      <OutputFile>$(OutDir)$(TargetName)$(TargetExt)</OutputFile>
      <AdditionalDependencies>Setupapi.lib;%(AdditionalDependencies)</AdditionalDependencies>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
    <PreBuildEvent>
      <Command>del ..\winversion.cpp
CALL "$(ProjectDir)\..\GIT-VS-VERSION-GEN.bat" "$(ProjectDir)\" "..\winversion.cpp"
exit 0</Command>
    </PreBuildEvent>
    <PreBuildEvent>
      <Message>Export GIT Revision</Message>
    </PreBuildEvent>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='ReleaseDLL|x64'">
    <ClCompile>
      <Optimization>MaxSpeed</Optimization>
      <PreprocessorDefinitions>WIN32;_LIB;OPENZWAVE_MAKEDLL;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <BasicRuntimeChecks>Default</BasicRuntimeChecks>
      <RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>
      <PrecompiledHeader>
      </PrecompiledHeader>
      <WarningLevel>Level3</WarningLevel>
      <DebugInformationFormat>ProgramDatabase</DebugInformationFormat>
      <DisableSpecificWarnings>4251</DisableSpecificWarnings>
      <AdditionalIncludeDirectories>..\..\..\src;..\..\..\tinyxml;..\..\..\hidapi\hidapi;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
    </ClCompile>
    <Lib>
      <OutputFile>$(OutDir)\$(ProjectName).lib</OutputFile>
      <AdditionalDependencies>setupapi.lib</AdditionalDependencies>
      <TargetMachine>MachineX86</TargetMachine>
    </Lib>
    <Link>
      <AdditionalDependencies>Setupapi.lib;%(AdditionalDependencies)</AdditionalDependencies>
    </Link>
    <PreBuildEvent />
    <PreBuildEvent>
      <Message>Export GIT Revision</Message>
      <Command>del ..\winversion.cpp
CALL "$(ProjectDir)\..\GIT-VS-VERSION-GEN.bat" "$(ProjectDir)\" "..\winversion.cpp"
exit 0</Command>
    </PreBuildEvent>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <ClCompile>
      <Optimization>MaxSpeed</Optimization>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <PreprocessorDefinitions>WIN32;NDEBUG;_LIB;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <RuntimeLibrary>MultiThreadedDLL</RuntimeLibrary>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <PrecompiledHeader>
      </PrecompiledHeader>
      <WarningLevel>Level3</WarningLevel>
      <DebugInformationFormat>ProgramDatabase</DebugInformationFormat>
      <AdditionalIncludeDirectories>..\..\..\src;..\..\..\tinyxml;..\..\..\hidapi\hidapi;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
    </ClCompile>
    <Lib>
      <OutputFile>$(OutDir)\$(ProjectName).lib</OutputFile>
      <AdditionalDependencies>setupapi.lib</AdditionalDependencies>
    </Lib>
    <PreBuildEvent>
      <Command>del ..\winversion.cpp
CALL "$(ProjectDir)\..\GIT-VS-VERSION-GEN.bat" "$(ProjectDir)\" "..\winversion.cpp"
exit 0</Command>
    </PreBuildEvent>
    <PreBuildEvent>
      <Message>Export GIT Revision</Message>
    </PreBuildEvent>
  </ItemDefinitionGroup>
  <ItemGroup>'''

ITEM_DEFINITION_GROUP_KEY = r'''  <ItemGroup>'''

GLOBAL_SELECTION_TEMPLATE = r'''
		Debug|x64 = Debug|x64
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


GLOBAL_SELECTION_KEY = r'''	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution'''


if __name__ == '__main__' and sys.platform.startswith("win"):
    setup_build_environment()

    from pyozw_popen import Popen, PIPE

    plat, pjct, d_env, b_path, p_path = find_ms_tools(
        debug=True,
        conf='Release'
    )

    upgrade_template = (
        '"{dev_env}" '
        '"{project_path}" '
        '/Upgrade '
    )
    upgrade_command = upgrade_template.format(
        dev_env=d_env,
        project_path=p_path
    )

    Popen(upgrade_command, stdout=PIPE, stderr=PIPE)

    sys.stdout.write("Cleaning openzwave project. be patient...")

    clean_template = (
        '"{dev_env}" '
        '"{project_path}" '
        '/UseEnv '
        '/Clean '
        '"{configuration}|{platform}"'
    )

    clean_command = clean_template.format(
        dev_env=d_env,
        project_path=p_path,
        configuration=pjct,
        platform=plat
    )

    Popen(clean_command, stdout=PIPE, stderr=PIPE)

    sys.stdout.write("Building openzwave project. be patient...")

    build_template = (
        '"{dev_env}" '
        '"{project_path}" '
        '/UseEnv '
        '/Build '
        '"{configuration}|{platform}"'
    )

    build_command = build_template.format(
        dev_env=d_env,
        project_path=p_path,
        configuration=pjct,
        platform=plat
    )

    Popen(build_command, stdout=PIPE, stderr=PIPE)

    print(
        'Library built in is in %s using compiler %s for arch %s' %
        (b_path, d_env, plat)
    )
