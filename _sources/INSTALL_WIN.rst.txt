:orphan:

======================================
Installing python-openzwave on Windows
======================================


Install Microsoft tools
=======================

This package use MSBuild.exe to build openzwave code.

You can find it in Visual Studio 2017 or Visual Studio 2015.

It's also possible to get it as a separate package.

Only release 14.0 and 15.0 of Microsft Build Tools are tested.

Install other tools
===================

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

And clone open-zwave inside python-openzwave :

.. code-block:: bash

    cd python-openzwave
    git clone https://github.com/OpenZWave/open-zwave.git openzwave

It's mandatory to clone the previous repository in a directory called openzwave (not open-zwave)

Visual studio
=============

Copy vs2010 in a new directory vs2017 (or vs2015 depending of which Visual Studio you use) :

.. code-block:: bash

    xcopy openzwave\cpp\build\windows\vs2010 openzwave\cpp\build\windows\vs2017 /s /e /h

Open the project (openzwave\cpp\build\windows\vs2017\OpenZWave.sln) in your Visual Studio.
If you want to build for 64bits, add a new target for it. And finally close it.

Python-openzwave
================

Build and install python-openzwave :

    .. code-block:: bash

        python setup.py install --flavor=dev

    .. code-block:: bash

        sysargv ['setup.py', 'install']
        <pyozw_setup.DevTemplate object at 0x03BAD690>thon setup.py install --flavor=dev
        Requirement already satisfied: Cython in c:\program files (x86)\python36-32\lib\site-packages
        {'name': 'libopenzwave', 'sources': ['src-lib/libopenzwave/libopenzwave.pyx'], 'include_dirs': ['openzwave/cpp/src', 'openzwave
        /cpp/src/value_classes', 'openzwave/cpp/src/platform', 'openzwave/cpp/build/windows', 'src-lib/libopenzwave', 'openzwave/cpp/bu
        ild/windows/vs2017/Release/'], 'define_macros': [('PY_LIB_VERSION', '0.4.4'), ('PY_SSIZE_T_CLEAN', 1), ('PY_LIB_FLAVOR', 'dev')
        , ('PY_LIB_BACKEND', 'cython')], 'libraries': ['setupapi', 'msvcrt', 'ws2_32', 'dnsapi'], 'extra_objects': ['openzwave/cpp/buil
        d/windows/vs2017/Release//OpenZWave.lib'], 'extra_compile_args': [], 'extra_link_args': [], 'language': 'c++'}
        ['six', 'PyDispatcher>=2.0.5', 'Cython']
        Requirement already satisfied: Cython in c:\program files (x86)\python36-32\lib\site-packages
        running install
        flavor --flavor=dev                      c:\program files (x86)\python36-32\lib\site-packages
        running build_openzwave
        Found MSBuild.exe : c:/Program Files (x86)/Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin\MSBuild.exe
        Found arch : Win32 wave
        Found Visual Studio project : vs2017 (x86)/Microsoft Visual Studio\2017\BuildTools\MSBuild\15.0\Bin\MSBuild.exe
        Found build path : openzwave/cpp/build/windows/vs2017/Release/
        ...
        ...
        byte-compiling C:\Program Files (x86)\Python36-32\Lib\site-packages\python_openzwave\scripts\__init__.py to __init__.cpython-36
        .pyc
        running install_egg_info
        running egg_info
        writing python_openzwave.egg-info\PKG-INFO
        writing dependency_links to python_openzwave.egg-info\dependency_links.txt
        writing entry points to python_openzwave.egg-info\entry_points.txt
         ================================================================
          .\scripts\allusers.bat
          this script is executed for all users
          delete/rename it if you dont need it
         ================================================================
        Page de codes active�: 437

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

