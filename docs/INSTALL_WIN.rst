:orphan:

======================================
Installing python-openzwave on Windows
======================================

Install Microsoft Visual Studio
=======================

This package uses Visual Studio to build openzwave code.


Install python libraries
========================

You need git to clone the repository and python (32 bits or 64 bits). Add it to your PATH.

Install dependencies :

 - for python 2.7 :

    .. code-block:: bash

        (venvX) pip install Cython six Louie

 - for python 3 :

    .. code-block:: bash

        (venvX) pip install Cython six PyDispatcher

clone repositories
==================

Clone python-openzwave:


.. code-block:: bash

    git clone https://github.com/OpenZWave/python-openzwave.git


Windows Kit/SDK
===============

My reccomendation is

VS 2017 use the latest Windows 10 SDK
VS 2015 use the latest Windows 8.1 SDK

and so on and so forth


Python-openzwave
================

The build system is automatic. 
It will build openzwave as 32/64bit depending on what version of Python and Windows is running.

Build and install python-openzwave :

    .. code-block:: bash

        python setup.py install --flavor=dev

    .. code-block:: bash

                Windows build setup starting.
        Locating vcvars32.bat....
        Setting up Visual Studio build environment.
        ImportError in : from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
        ('sysargv', ['setup.py', 'install'])
        NameError in : class bdist_wheel(_bdist_wheel) - Use bdist_egg instead
        <pyozw_setup.DevTemplate object at 0x0342EFB0>
        Requirement already satisfied: Cython in c:\python27clean\lib\site-packages
        Locating devenv.com....
        Downloading openzwave.........
        Copying openzwave Visual Studio solution.
        ...
        ['six', 'Louie>=1.1', 'Cython']
        Requirement already satisfied: Cython in c:\python27clean\lib\site-packages
        running install
        flavor --flavor=dev
        running build_openzwave
        Found devenv.exe : C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\IDE\devenv.com
        Found arch : Win32
        Found Visual Studio project : vs2017
        Found build path : C:\Users\Administrator\Desktop\New folder (56)\python-openzwave-master\openzwave\cpp\build\windows\vs2017\Release
        Upgrading openzwave project. be patient..............
        
        Cleaning openzwave project. be patient........
        
        Building openzwave project. be patient.....................................
        
        running openzwave_config
        Install ozw_config for template <pyozw_setup.DevTemplate object at 0x0342EFB0>
        ...
        running build
        running build_py
        running build_ext
        cythoning src-lib/libopenzwave/libopenzwave.pyx to src-lib/libopenzwave\libopenzwave.cpp
        building 'libopenzwave' extension
        ...
        Generating code
        Finished generating code
        running install_lib
        copying build\lib.win32-2.7\libopenzwave.pyd -> c:\python27clean\Lib\site-packages
        copying build\lib.win32-2.7\python_openzwave\ozw_config\__init__.py -> c:\python27clean\Lib\site-packages\python_openzwave\ozw_config
        byte-compiling c:\python27clean\Lib\site-packages\python_openzwave\ozw_config\__init__.py to __init__.pyc
        running install_egg_info
        running egg_info
        writing requirements to python_openzwave.egg-info\requires.txt
        writing python_openzwave.egg-info\PKG-INFO
        writing top-level names to python_openzwave.egg-info\top_level.txt
        writing dependency_links to python_openzwave.egg-info\dependency_links.txt
        writing entry points to python_openzwave.egg-info\entry_points.txt
        reading manifest file 'python_openzwave.egg-info\SOURCES.txt'
        writing manifest file 'python_openzwave.egg-info\SOURCES.txt'
        Copying python_openzwave.egg-info to c:\python27clean\Lib\site-packages\python_openzwave-0.4.4-py2.7.egg-info
        running install_scripts
        Installing pyozw_check-script.py script to c:\python27clean\Scripts
        Installing pyozw_check.exe script to c:\python27clean\Scripts
        Installing pyozw_check.exe.manifest script to c:\python27clean\Scripts
        Installing pyozw_shell-script.py script to c:\python27clean\Scripts
        Installing pyozw_shell.exe script to c:\python27clean\Scripts
        Installing pyozw_shell.exe.manifest script to c:\python27clean\Scripts

And finally, test it :

    .. code-block:: bash

        pyozw_check -l -d COM2 -t 30

    .. code-block:: bash

        -------------------------------------------------------------------------------
        Define options for device COM2
        Start network
        Wait for network awake (30s)
        -------------------------------------------------------------------------------
        Network is awaked. Talk to controller.
        Get python_openzwave version : 0.4.4
        Get python_openzwave config version : Original Z-Wave 2.78
        Get python_openzwave flavor : dev
        Get openzwave version : 1.4.2942
        Get config path : C:\Program Files\Python36\lib\site-packages\python_openzwave\ozw_config
        Controller capabilities : {'primaryController', 'staticUpdateController'}
        Controller node capabilities : {'listening', 'primaryController', 'beaming', 'staticUpdateController'}
        Nodes in network : 4
        -------------------------------------------------------------------------------
        Wait for network ready (30s)
        -------------------------------------------------------------------------------
        Network is ready. Get nodes
        ------------------------------------------------------------
        1 - Name :  ( Location :  )
         1 - Ready : True / Awake : True / Failed : False
         1 - Manufacturer : Aeotec  ( id : 0x0086 )
         1 - Product : DSA02203 Z-Stick S2 ( id  : 0x0001 / type : 0x0002 / Version : 3)
         1 - Command classes : set()
         1 - Capabilities : {'listening', 'primaryController', 'beaming', 'staticUpdateController'}
         1 - Neighbors : {4} / Power level : None
         1 - Is sleeping : False / Can wake-up : False / Battery level : None
        ------------------------------------------------------------
        2 - Name :  ( Location :  )
         2 - Ready : True / Awake : True / Failed : False
         2 - Manufacturer :   ( id : 0x0000 )
         2 - Product :  ( id  : 0x0000 / type : 0x0000 / Version : 2)
         2 - Command classes : set()
         2 - Capabilities : {'listening', 'routing'}
         2 - Neighbors : {3} / Power level : None
         2 - Is sleeping : False / Can wake-up : False / Battery level : None
        ------------------------------------------------------------
        3 - Name :  ( Location :  )
         3 - Ready : False / Awake : True / Failed : True
         3 - Manufacturer :   ( id : 0x0000 )
         3 - Product :  ( id  : 0x0000 / type : 0x0000 / Version : 3)
         3 - Command classes : set()
         3 - Capabilities : {'listening', 'routing', 'beaming'}
         3 - Neighbors : set() / Power level : None
         3 - Is sleeping : False / Can wake-up : False / Battery level : None
        ------------------------------------------------------------
        4 - Name :  ( Location :  )
         4 - Ready : True / Awake : True / Failed : False
         4 - Manufacturer : GreenWave  ( id : 0x0099 )
         4 - Product : PowerNode 6 port ( id  : 0x0004 / type : 0x0003 / Version : 4)
         4 - Command classes : {'COMMAND_CLASS_MANUFACTURER_SPECIFIC', 'COMMAND_CLASS_ASSOCIATION', 'COMMAND_CLASS_NO_OPERATION', 'COMM
        AND_CLASS_VERSION', 'COMMAND_CLASS_SWITCH_BINARY', 'COMMAND_CLASS_MULTI_INSTANCE/CHANNEL', 'COMMAND_CLASS_CRC_16_ENCAP', 'COMMA
        ND_CLASS_PROTECTION', 'COMMAND_CLASS_CONFIGURATION', 'COMMAND_CLASS_BASIC', 'COMMAND_CLASS_METER', 'COMMAND_CLASS_SWITCH_ALL'}
         4 - Capabilities : {'listening', 'routing', 'beaming'}
         4 - Neighbors : {1} / Power level : None
         4 - Is sleeping : False / Can wake-up : False / Battery level : None
        ------------------------------------------------------------
        Driver statistics : {'SOFCnt': 49, 'ACKWaiting': 0, 'readAborts': 0, 'badChecksum': 0, 'readCnt': 49, 'writeCnt': 46, 'CANCnt':
         0, 'NAKCnt': 1, 'ACKCnt': 30, 'OOFCnt': 0, 'dropped': 17, 'retries': 0, 'callbacks': 0, 'badroutes': 0, 'noack': 4, 'netbusy':
         0, 'nondelivery': 0, 'routedbusy': 0, 'broadcastReadCnt': 0, 'broadcastWriteCnt': 9}
        ------------------------------------------------------------
        Stop network
        Exit

