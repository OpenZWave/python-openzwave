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

import sys, os
import fnmatch
import platform

VC9 = 'VC9'
VC10 = 'VC10'
VC14 = 'VC14'

def get_win_config( debug=False ):
    """Retrieve needed tools to build extension
    Depend of python version
    See https://wiki.python.org/moin/WindowsCompilers
    """
    if sys.version_info >= (2,6) and sys.version_info < (3,3):
        return VC9
    elif sys.version_info >= (3,3) and sys.version_info < (3,5):
        return VC10
    elif sys.version_info >= (3,5):
        return VC14

def find_all_build_tools(name, paths):
    """Search for name recursively in paths
    """
    result = []
    for path in paths:
        for root, dirs, files in os.walk(path):
            if name in files:
                result.append(os.path.join(root, name))
    return result

def find_msbuild_tools( options, debug=False ):
    """Find MSBuild.exe
    """
    win_config = get_win_config(debug=debug)
    if win_config == VC14:
        if 'devenv' in options and '2015' in options['devenv']:
            vs_path = [
                       'c:\\Program Files (x86)\\MSBuild\\14.0',
                       'c:\\Program Files (x86)\\Microsoft Visual Studio\\2015',
                       'c:\\Program Files (x86)\\MSBuild\\15.0',
                       'c:\\Program Files (x86)\\Microsoft Visual Studio\\2017',
                       ]
        else:
            vs_path = [
                       'c:\\Program Files (x86)\\MSBuild\\15.0',
                       'c:\\Program Files (x86)\\Microsoft Visual Studio\\2017',
                       'c:\\Program Files (x86)\\MSBuild\\14.0',
                       'c:\\Program Files (x86)\\Microsoft Visual Studio\\2015',
                       ]
        if debug:
            print("Check for MSBuild.exe in %s" %vs_path)
        all_msbuild = find_all_build_tools("MSBuild.exe", vs_path)
        if debug:
            print("Found MSBuild.exe in %s" %all_msbuild)
        if options['arch'] == 'x64':
            msbuild2 = [name for name in all_msbuild if 'amd64' in name]
        if options['arch'] == 'Win32':
            msbuild2 = [name for name in all_msbuild if not 'amd64' in name]
        if debug:
            print("Found MSBuild.exe in %s" %msbuild2)
        if len(msbuild2) == 0:
            raise RuntimeError("Can't find MSBuild.exe for arch %s in %s looked in %s"%(options['arch'], all_msbuild, vs_path))
        options['msbuild'] =  msbuild2[0]

    elif win_config == VC10:
        vs_path = [
                   'c:\\Program Files (x86)\\Microsoft Visual Studio 10.0',
                   'c:\\Program Files (x86)\\Microsoft Visual Studio 11.0',
                   'c:\\Program Files (x86)\\MSBuild',
                   ]
        if debug:
            print("Check for MSBuild.exe in %s" %vs_path)
        all_msbuild = find_all_build_tools("MSBuild.exe", vs_path)
        if debug:
            print("Found MSBuild.exe in %s" %all_msbuild)
        if options['arch'] == 'x64':
            msbuild2 = [name for name in all_msbuild if 'amd64' in name]
        if options['arch'] == 'Win32':
            msbuild2 = [name for name in all_msbuild if not 'amd64' in name]
        if debug:
            print("Found MSBuild.exe in %s" %msbuild2)
        if len(msbuild2) == 0:
            raise RuntimeError("Can't find MSBuild.exe for arch %s in %s looked in %s"%(options['arch'], all_msbuild, vs_path))
        options['msbuild'] =  msbuild2[0]

    elif win_config == VC9:
        vs_path = [
                   'c:\\Program Files (x86)\\Microsoft Visual Studio 9.0',
                   'c:\\Program Files (x86)\\MSBuild',
                   ]
        if debug:
            print("Check for MSBuild.exe in %s" %vs_path)
        all_msbuild = find_all_build_tools("MSBuild.exe", vs_path)
        if debug:
            print("Found MSBuild.exe in %s" %all_msbuild)
        if options['arch'] == 'x64':
            msbuild2 = [name for name in all_msbuild if 'amd64' in name]
        if options['arch'] == 'Win32':
            msbuild2 = [name for name in all_msbuild if not 'amd64' in name]
        if debug:
            print("Found MSBuild.exe in %s" %msbuild2)
        if len(msbuild2) == 0:
            raise RuntimeError("Can't find MSBuild.exe for arch %s in %s looked in %s"%(options['arch'], all_msbuild, vs_path))
        options['msbuild'] =  msbuild2[0]
    return 'msbuild' in options

def find_devenv_tools( options, debug=False ):
    """Find devenv.exe
    """
    win_config = get_win_config(debug=debug)
    if win_config == VC14:
        vs_path = [
                   'c:\\Program Files (x86)\\Microsoft Visual Studio\\2015',
                   'c:\\Program Files (x86)\\Microsoft Visual Studio\\2017',
                   ]
        if debug:
            print("Check for devenv in %s" %vs_path)
        all_msbuild = find_all_build_tools("devenv.exe", vs_path)
        if debug:
            print("Found devenv in %s" %all_msbuild)
        if len(all_msbuild) == 0:
            raise RuntimeError("Can't find devenv in %s looked in %s"%(all_msbuild, vs_path))
        options['devenv'] =  all_msbuild[0]

    elif win_config == VC10:
        vs_path = [
                   'c:\\Program Files (x86)\\Microsoft Visual Studio 10.0',
                   'c:\\Program Files (x86)\\Microsoft Visual Studio 11.0',
                   ]
        if debug:
            print("Check for devenv.exe in %s" %vs_path)
        all_msbuild = find_all_build_tools("devenv.exe", vs_path)
        if debug:
            print("Found devenv.exe in %s" %all_msbuild)
        if len(all_msbuild) == 0:
            raise RuntimeError("Can't find devenv.exe in %s looked in %s"%( all_msbuild, vs_path ))
        options['devenv'] =  all_msbuild[0]

    elif win_config == VC9:
        #~ vs_path = ['c:\\Program Files (x86)\\Microsoft Visual Studio 9.0',
                   #~ ]
        #~ if debug:
            #~ print("Check for devenv.exe in %s" %vs_path)
        #~ all_msbuild = find_all_build_tools("devenv.exe", vs_path)
        #~ if debug:
            #~ print("Found devenv.exe in %s" %all_msbuild)
        #~ if len(all_msbuild) == 0:
            #~ raise RuntimeError("Can't find devenv.exe in %s looked in %s"%( all_msbuild, vs_path ))
        #~ options['devenv'] =  all_msbuild[0]
        options['devenv'] = None
    return 'devenv' in options

def get_vs_project( options, openzwave='openzwave', debug=False ):
    """Retrieve needed tools to build extension
    Depend of python version
    See https://wiki.python.org/moin/WindowsCompilers
    """
    win_config = get_win_config(debug=debug)
    if win_config == VC14:
        if '2015' in options['devenv']:
            options['vsproject'] = os.path.join(openzwave,'cpp','build','windows','vs2015')
        elif '2017' in options['devenv']:
            options['vsproject'] = os.path.join(openzwave,'cpp','build','windows','vs2017')
        if not ( 'vsproject' in options ):
            raise RuntimeError("Can't find devenv.exe for VS2017 / VS2015")
        import shutil
        if os.path.isdir(options['vsproject']):
            shutil.rmtree(options['vsproject'])
        shutil.copytree(os.path.join(openzwave,'cpp','build','windows','vs2010'), options['vsproject'])
        options['vsproject_upgrade'] = True
        options['vsproject_prebuild'] = False
    elif win_config == VC10:
        options['vsproject'] = os.path.join(openzwave,'cpp','build','windows','vs2010')
        options['vsproject_upgrade'] = False
        options['vsproject_prebuild'] = False
    elif win_config == VC9:
        options['vsproject'] = os.path.join(openzwave,'cpp','build','windows','vs2008')
        options['vsproject_upgrade'] = False
        options['vsproject_prebuild'] = False
    if options['arch'] == "x64" :
        options['vsproject_build'] = os.path.join(options['vsproject'], options['arch'], options['buildconf'])
        update_vs_project( options, debug=debug )
    else:
        options['vsproject_build'] = os.path.join(options['vsproject'], options['buildconf'])
    return 'vsproject' in options

def update_vs_project( options, openzwave="openzwave", debug=False, update_version=False ):
    """Retrieve needed tools to build extension
    Depend of python version
    See https://wiki.python.org/moin/WindowsCompilers
    """
    from xml.etree import ElementTree
    import copy

    ElementTree.register_namespace('', "http://schemas.microsoft.com/developer/msbuild/2003")
    if update_version:
        bversion="4.0"
        toolset='v100'
        if '2015' in options['devenv'] or ('14.0' in options['msbuild'] and not('Visual Studio' in options['msbuild']) ):
            bversion="14.0"
            toolset='v140'
        elif '2017' in options['devenv'] or ('15.0' in options['msbuild'] and not('Visual Studio' in options['msbuild']) ):
            bversion="15.0"
            toolset='v141'

    tree = ElementTree.parse(os.path.join(options['vsproject'], 'OpenZWave.vcxproj'), parser=None)
    root = tree.getroot()

    if update_version:
        root.set('ToolsVersion', bversion)

    for p in root.findall("{http://schemas.microsoft.com/developer/msbuild/2003}ItemGroup"):
        if 'Label' in p.attrib and p.attrib['Label'] == 'ProjectConfigurations':
            prjconfs = p

    newconfs = []
    for p in prjconfs:
        dupe = copy.deepcopy(p) #copy <c> node
        dupe.set('Include', dupe.attrib['Include'].replace('Win32', 'x64'))
        dupe.find('{http://schemas.microsoft.com/developer/msbuild/2003}Platform').text = 'x64'
        newconfs.append(dupe) #insert the new node
    for new in newconfs:
        prjconfs.append(new)

    newconfs = []
    prjconfs = [ p for p in root.findall("{http://schemas.microsoft.com/developer/msbuild/2003}PropertyGroup")
                    if p.get('Label') == 'Configuration']
    for p in prjconfs:
        plat = p.find('{http://schemas.microsoft.com/developer/msbuild/2003}PlatformToolset')
        if update_version:
            if plat is not None:
                plat.text = toolset
            else:
                newKid = ElementTree.Element('{http://schemas.microsoft.com/developer/msbuild/2003}PlatformToolset')
                newKid.text = toolset
                p.append(newKid)
        dupe = copy.deepcopy(p) #copy <c> node
        dupe.set('Condition', dupe.attrib['Condition'].replace('Win32', 'x64'))
        newconfs.append(dupe) #insert the new node
    for new in newconfs:
        root.append(new)

    newconfs = []
    prjconfs = [ p for p in root.findall("{http://schemas.microsoft.com/developer/msbuild/2003}ImportGroup")
                    if p.get('Condition') is not None ]
    for p in prjconfs:
        dupe = copy.deepcopy(p) #copy <c> node
        dupe.set('Condition', dupe.attrib['Condition'].replace('Win32', 'x64'))
        newconfs.append(dupe) #insert the new node
    for new in newconfs:
        root.append(new)

    newconfs = []
    prjconfs = [ p for p in root.findall("{http://schemas.microsoft.com/developer/msbuild/2003}ItemDefinitionGroup")
                    if p.get('Condition') is not None ]
    for p in prjconfs:
        dupe = copy.deepcopy(p) #copy <c> node
        dupe.set('Condition', dupe.attrib['Condition'].replace('Win32', 'x64'))
        newconfs.append(dupe) #insert the new node
    for new in newconfs:
        root.append(new)

    newconfs = []
    prj = [ p for p in root.findall("{http://schemas.microsoft.com/developer/msbuild/2003}PropertyGroup")
                    if len(p.findall("{http://schemas.microsoft.com/developer/msbuild/2003}_ProjectFileVersion"))>0 ]
    prjconfs = [ p for p in prj[0] if p.get('Condition') is not None ]
    for p in prjconfs:
        dupe = copy.deepcopy(p) #copy <c> node
        dupe.set('Condition', dupe.attrib['Condition'].replace('Win32', 'x64'))
        newconfs.append(dupe) #insert the new node
    for new in newconfs:
        prj[0].append(new)

    tree.write(os.path.join(options['vsproject'], 'OpenZWave.vcxproj'),xml_declaration=False)

    with open(os.path.join(options['vsproject'], 'OpenZWave.sln'), 'r') as f:
        sln = f.read()

    targets = [
        ('Debug|Win32','Debug|x64'),
        ('DebugDLL|Win32','DebugDLL|x64'),
        ('Release|Win32','Release|x64'),
        ('ReleaseDLL|Win32','ReleaseDLL|x64'),
        ]
    for target in targets:
        sln = sln.replace(
            '%s = %s'%(target[0], target[0]),
            '%s = %s\n\t\t%s = %s'%(target[0], target[0], target[1], target[1])
        )
    targets = [
        ('{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Debug|Win32.ActiveCfg = Debug|Win32', '{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Debug|x64.ActiveCfg = Debug|x64'),
        ('{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Debug|Win32.Build.0 = Debug|Win32', '{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Debug|x64.Build.0 = Debug|x64'),
        ('{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.DebugDLL|Win32.ActiveCfg = DebugDLL|Win32', '{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.DebugDLL|x64.ActiveCfg = DebugDLL|x64'),
        ('{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.DebugDLL|Win32.Build.0 = DebugDLL|Win32', '{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.DebugDLL|x64.Build.0 = DebugDLL|x64'),
        ('{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Release|Win32.ActiveCfg = Release|Win32', '{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Release|x64.ActiveCfg = Release|x64'),
        ('{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Release|Win32.Build.0 = Release|Win32', '{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.Release|x64.Build.0 = Release|x64'),
        ('{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.ReleaseDLL|Win32.ActiveCfg = ReleaseDLL|Win32', '{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.ReleaseDLL|x64.ActiveCfg = ReleaseDLL|x64'),
        ('{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.ReleaseDLL|Win32.Build.0 = ReleaseDLL|Win32', '{497F9828-DEC2-4C80-B9E0-AD066CCB587C}.ReleaseDLL|x64.Build.0 = ReleaseDLL|x64'),
        ]

    for target in targets:
        sln = sln.replace(
            '%s'%(target[0]),
            '%s\n\t\t%s'%(target[0], target[1])
        )

    with open(os.path.join(options['vsproject'], 'OpenZWave.sln'), 'w') as f:
        f.write(sln)
    if debug:
        print("OpenZWave project for visual studio updated" )


def get_system_context( ctx, options, openzwave="openzwave", static=False, debug=False ):

    if debug:
        print("get_system_context for windows")

    if static:
        options['buildconf'] = 'Release'
    else:
        options['buildconf'] = 'ReleaseDLL'

    if 'arch' not in options:
        options['arch'] = 'Win32'
        python_arch,_ = platform.architecture()
        if python_arch == "64bit":
            options['arch'] = "x64"
    if debug:
        print("Found arch %s" %options['arch'])

    if 'devenv' not in options:
        find_devenv_tools( options, debug=debug )
    if 'msbuild' not in options:
        find_msbuild_tools( options, debug=debug )
    if 'vsproject' not in options:
        get_vs_project( options, openzwave=openzwave, debug=debug )

    if debug:
        print("Found options %s" %options)

    ctx['libraries'] += [ "setupapi", "msvcrt", "ws2_32", "dnsapi" ]

    if static:
        ctx['extra_objects'] = [ "{0}/OpenZWave.lib".format(options['vsproject_build']) ]
        ctx['include_dirs'] += [ "{0}/cpp/build/windows".format(openzwave),
                                 "src-lib/libopenzwave",
                                 "{0}".format(options['vsproject_build']),
                                ]
    else:
        ctx['libraries'] += [ "OpenZWave" ]
        ctx['extra_compile_args'] += [
            "{0}/cpp/src".format(openzwave),
            "{0}/cpp/src/value_classes".format(openzwave),
            "{0}/cpp/src/platform".format(openzwave) ]

def get_vsproject_upgrade_command( options, debug=False ):
    if debug:
        print("get_vsproject_upgrade_command" )
    return [ options['devenv'],
            'OpenZWave.sln',
            '/upgrade',
            ]

def get_vsproject_prebuild_command( options, debug=False ):
    if debug:
        print("get_vsproject_prebuild_command" )
    return [ options['devenv'],
            '/updateconfiguration',
            '/out',
            'LogUpdateConfiguration.htm',
            ]

def get_vsproject_build_command( options, debug=False ):
    if debug:
        print("get_vsproject_build_command" )
        print(
                options['msbuild'],
                'OpenZWave.sln',
                '/t:Rebuild',
                '/p:Configuration={0}'.format(options['buildconf']),
                '/p:Platform={0}'.format(options['arch'])
            )
    return [ options['msbuild'],
            'OpenZWave.sln',
            '/t:Rebuild',
            '/p:Configuration={0}'.format(options['buildconf']),
            '/p:Platform={0}'.format(options['arch'])
            ]

def get_vsproject_devenv_build_command( options, debug=False ):
    if debug:
        print("get_vsproject_build_command" )
        print(
        options['devenv'],
            'OpenZWave.sln',
            '/Rebuild',
            '"{0}|{1}"'.format(options['buildconf'],options['arch'])
            )
    return [ options['devenv'],
            'OpenZWave.sln',
            '/Rebuild',
            '"{0}|{1}"'.format(options['buildconf'],options['arch'])
            ]

def get_vsproject_devenv_clean_command( options, debug=False ):
    if debug:
        print("get_vsproject_devenv_clean_command" )
        print(
        options['devenv'],
            'OpenZWave.sln',
            '/Clean',
            '"{0}|{1}"'.format(options['buildconf'],options['arch'])
            )
    return [ options['devenv'],
            'OpenZWave.sln',
            '/Clean',
            '"{0}|{1}"'.format(options['buildconf'],options['arch'])
            ]

if __name__ == '__main__':
    from subprocess import Popen, PIPE, call
    print("Start pyozw_win")
    ctx = { "name": "libopenzwave",
             "sources": [ ],
             "include_dirs": [ ],
             "libraries": [ ],
             "extra_objects": [ ],
             "extra_compile_args": [ ],
             "extra_link_args": [ ],
             "language": "c++",
           }
    options = dict()
    get_system_context( ctx, options, openzwave="openzwave", static=True, debug=True )

    print(options['vsproject'])

    os.system( get_vsproject_devenv_clean_command( options, debug=True ) )
    #~ proc = Popen(get_vsproject_devenv_clean_command( options, debug=True ),
                    #~ shell=True,
                    #~ stdout=PIPE, 
                    #~ stderr=PIPE, 
                    #~ cwd='{0}'.format(options['vsproject']))
    #~ for line in proc.stdout: 
        #~ print(line)
    #~ errcode = proc.returncode
    #~ for line in proc.stdout: 
        #~ print(line)

    os.system( get_vsproject_upgrade_command( options, debug=True ) )
    #~ proc = Popen(get_vsproject_upgrade_command( options, debug=True ),
                    #~ shell=True,
                    #~ stdout=PIPE, 
                    #~ stderr=PIPE, 
                    #~ cwd='{0}'.format(options['vsproject']))
    #~ for line in proc.stdout: 
        #~ print(line)
    #~ errcode = proc.returncode
    #~ for line in proc.stdout: 
        #~ print(line)

    #~ proc = Popen(get_vsproject_prebuild_command( options, debug=True  ), cwd='{0}'.format(options['vsproject']))
    #~ proc.wait()

    #~ proc = call(get_vsproject_devenv_build_command( options, debug=True  ), cwd='{0}'.format(options['vsproject']))
    #~ proc = call(get_vsproject_build_command( options, debug=True  ), cwd='{0}'.format(options['vsproject']))
    os.system( get_vsproject_build_command( options, debug=True ) )
    #~ proc = Popen(get_vsproject_build_command( options, debug=True ),
                    #~ shell=True,
                    #~ stdout=PIPE, 
                    #~ stderr=PIPE, 
                    #~ cwd='{0}'.format(options['vsproject']))
    #~ for line in proc.stdout: 
        #~ print(line)
    #~ errcode = proc.returncode
    #~ for line in proc.stdout: 
        #~ print(line)

    print('Library built in %s using compiler %s for arch %s' % (options['vsproject_build'], options['msbuild'], options['arch']))
