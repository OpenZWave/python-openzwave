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
import fnmatch
import platform
 
def find_ms_tools( debug=False, conf='Release' ):
    def find_all_build_tools(name, paths):
        result = []
        for path in paths:
            for root, dirs, files in os.walk(path):
                if name in files:
                    result.append(os.path.join(root, name))
        return result

    def find_all_vs_projects(path):
        result = []
        pattern = 'vs*'
        for root, dirs, files in os.walk(path):
            for filename in fnmatch.filter(dirs, pattern):
                result.append(filename)
        return sorted(result, reverse=True)
    project_dir = "openzwave/cpp/build/windows/"
    vs_path = ['c:/Program Files (x86)/MSBuild', 
               'c:/Program Files (x86)/Microsoft Visual Studio', 
               'c:/Program Files (x86)/Microsoft Visual Studio 14.0', 
               ]
    if debug:
        print("Check for MSBuild.exe in %s" %vs_path)
    all_msbuild = find_all_build_tools("MSBuild.exe", vs_path)
    if debug:
        print("Found MSBuild.exe in %s" %all_msbuild)
    projects = find_all_vs_projects(project_dir)
    if debug:
        print("Found projects in %s" %projects)
    #~ projects = ["vs2015", "vs2010", "vs2008"]
    arch = 'Win32'
    python_arch,_ = platform.architecture()
    if python_arch == "64bit":
        arch = "x64"
    #~ arch = "x64"
    if debug:
        print("Found arch %s" %arch)
    msbuild = []
    for project in projects:
        if project == 'vs2017':
            msbuild = [name for name in all_msbuild if '2017' in name or '\15.0' in name]
        elif project == 'vs2015':
            msbuild = [name for name in all_msbuild if '2015' in name or '\14.0' in name]
        elif project == 'vs2010':
            msbuild = [name for name in all_msbuild if '2010' in name or '\4.0' in name]
        if len(msbuild) > 0:
            break
    if debug:
        print("Found compilers %s for project %s" %(msbuild, project))
    #~ print(msbuild)
    if arch == 'x64':
        msbuild2 = [name for name in msbuild if 'amd64' in name]
        build_path = 'openzwave/cpp/build/windows/%s/x64/%s/'%(project, conf)
    if arch == 'Win32':
        msbuild2 = [name for name in msbuild if not 'amd64' in name]
        build_path = 'openzwave/cpp/build/windows/%s/%s/'%(project, conf)
    #~ print(projects)
    #~ print(msbuild)
    #~ print(arch)
    if debug:
        print("Found compilers %s for project %s and arch %s" %(msbuild, project, arch))
    if debug:
        print("Library will be built in %s" %(build_path))
    if len(msbuild2) == 0:
        raise RuntimeError("Can't find MSBuild (arch %s) in %s to build projects in %s"%(arch, vs_path, projects))
    return arch, project, msbuild[0], build_path

if __name__ == '__main__':
    from subprocess import Popen, PIPE

    conf = 'Release'
    arch, project, msbuild, build_path = find_ms_tools(debug=True, conf=conf)

    proc = Popen([ msbuild, 'OpenZWave.sln', '/t:Rebuild', '/p:Configuration=%s'%(conf), '/p:Platform=%s'%(arch) ], cwd='{0}'.format('openzwave/cpp/build/windows/%s'%project))
    proc.wait()

    print('Library built in is in %s using compiler %s for arch %s' % (build_path, msbuild, arch))
