.. image:: https://travis-ci.org/OpenZWave/python-openzwave.svg?branch=master
    :target: https://travis-ci.org/OpenZWave/python-openzwave
    :alt: Travis status

.. image:: https://circleci.com/gh/OpenZWave/python-openzwave.png?style=shield
    :target: https://circleci.com/gh/OpenZWave/python-openzwave
    :alt: Circle status

.. image:: https://img.shields.io/pypi/format/python_openzwave.svg
    :target: https://pypi.python.org/pypi/python_openzwave
    :alt: Pypi format
    
.. image:: https://img.shields.io/badge/Documentation-ok-brightgreen.svg?style=flat
   :target: http://openzwave.github.io/python-openzwave/index.html
   :alt: Documentation

================
python-openzwave
================

python-openzwave is a python wrapper for the openzwave c++ library : https://github.com/OpenZWave/open-zwave

 * full manager implementation with options
 * an API to map the ZWave network in Python objects
 * a command line manager to manage / debug your ZWave network
 * a full-event webapp example : flask + socket.io + jquery
 * a suite of tests
 * many examples
 * `Full documentation <http://openzwave.github.io/python-openzwave/index.html>`_

python-openzwave 0.4.x is here !!!
==================================
 
- New installation process via pip
 
- First, you need some build tools and libs. On ubuntu, you should use :

     .. code-block:: bash

        sudo apt-get install --force-yes -y make libudev-dev g++ libyaml-dev

- Make your virtualenv and activate it : 
 
    .. code-block:: bash

        virtualenv --python=python3 venv3
        source venv3/bin/activate

- Install the default flavor  :       
 
    .. code-block:: bash
    
        (venvX) pip install python_openzwave
    
- The previous command try to install python_openzwave with the flavor 'shared'. 
  If it can't find a precompiled library of openzwave, it will use the flavor 'embed' with sources downloaded from https://github.com/OpenZWave/python-openzwave/tree/master/archives.
  You can change this using flavor option. 
  There is a bug in the package dependencies and flavors on some systems. You may need to install dependencies manualy :
 
 - on python 2.7 :
  
    .. code-block:: bash
  
        (venvX) pip install cython wheel six
        (venvX) pip install 'Louie>=1.1'

 - on python 3 :
  
    .. code-block:: bash
  
        (venvX) pip install cython wheel six
        (venvX) pip install 'PyDispatcher>=2.0.5'

- Choose your flavor :
 
    - embed : the default one. Download sources from https://github.com/OpenZWave/python-openzwave/tree/master/archives and
      build them. Python_openzwave is statically build using a cythonized version of libopenzwave. No need to install cython.
    - shared : if you have install openzwave as module manually, you can link python_openzwave to it.
    - git : download sources from openzwave github and link statically to it.
    - embed_shared : download sources from https://github.com/OpenZWave/python-openzwave/tree/master/archives, build and install as module on the system. 
      Python_openzwave use it. Need root access to install openzwave libs.
    - git_shared : download sources from openzwave github, build and install them as module on the system.
      Python_openzwave use it. Need root access to install openzwave libs.
    - ozwdev and ozwdev_shared : use the dev branch of openzwave on github.
    - dev : for python_openzwave developers. Look for openzwave sources in a local folder specified by the LOCAL_OPENZWAVE environment variable (defaults to 'openzwave').
   
- Install it :
 
    .. code-block:: bash
    
        (venvX) pip install python_openzwave  --no-deps --install-option="--flavor=git"

- You can update to the last version of openzwave using the git flavor :
       
    .. code-block:: bash
    
        (venvX) pip uninstall -y python_openzwave
        (venvX) pip install python_openzwave --no-cache-dir --no-deps --install-option="--flavor=git"
        
    
- At last, you can launch pyozw_check to test your installation :

   If no usb stick is connected to the machine, launch :

    .. code-block:: bash

        (venvX) pyozw_check

   If you've one, use it for advanced checks : 
    
    .. code-block:: bash

        (venvX) pyozw_check -i -d /dev/ttyUSB0

    .. code-block:: bash
    
        -------------------------------------------------------------------------------
        Import libs
        Try to import libopenzwave
        Try to import libopenzwave.PyLogLevels
        Try to get options
        Try to get manager
        Try to get python_openzwave version
        0.4.0.27
        Try to get python_openzwave full version
        python-openzwave version 0.4.0.27 (dev / Apr 18 2017 - 23:22:26)
        Try to get openzwave version
        1.4.2501
        Try to get default config path
        /etc/openzwave/
        Try to import openzwave (API)
        -------------------------------------------------------------------------------
        Intialize device /dev/ttyUSB0
        Try to get options
        Try to get manager
        2017-04-12 16:41:29.329 Always, OpenZwave Version 1.4.2497 Starting Up
        Try to add watcher
        ...
        2017-04-12 16:44:05.880 Always, ***************************************************************************
        2017-04-12 16:44:05.880 Always, *********************  Cumulative Network Statistics  *********************
        2017-04-12 16:44:05.880 Always, *** General
        2017-04-12 16:44:05.880 Always, Driver run time: . .  . 0 days, 0 hours, 1 minutes
        2017-04-12 16:44:05.880 Always, Frames processed: . . . . . . . . . . . . . . . . . . . . 27
        2017-04-12 16:44:05.880 Always, Total messages successfully received: . . . . . . . . . . 27
        2017-04-12 16:44:05.880 Always, Total Messages successfully sent: . . . . . . . . . . . . 19
        2017-04-12 16:44:05.880 Always, ACKs received from controller:  . . . . . . . . . . . . . 19
        2017-04-12 16:44:05.880 Always, *** Errors
        2017-04-12 16:44:05.880 Always, Unsolicited messages received while waiting for ACK:  . . 0
        2017-04-12 16:44:05.880 Always, Reads aborted due to timeouts:  . . . . . . . . . . . . . 0
        2017-04-12 16:44:05.880 Always, Bad checksum errors:  . . . . . . . . . . . . . . . . . . 0
        2017-04-12 16:44:05.880 Always, CANs received from controller:  . . . . . . . . . . . . . 0
        2017-04-12 16:44:05.880 Always, NAKs received from controller:  . . . . . . . . . . . . . 0
        2017-04-12 16:44:05.880 Always, Out of frame data flow errors:  . . . . . . . . . . . . . 0
        2017-04-12 16:44:05.880 Always, Messages retransmitted: . . . . . . . . . . . . . . . . . 0
        2017-04-12 16:44:05.880 Always, Messages dropped and not delivered: . . . . . . . . . . . 0
        2017-04-12 16:44:05.880 Always, ***************************************************************************
        2017-04-12 16:44:07.887 Info, mgr,     Driver for controller /dev/ttyUSB0 removed
        Try to remove watcher
        Try to destroy manager
        Try to destroy options
    
   You can list the nodes on your network using : 
    
    .. code-block:: bash

        (venvX) pyozw_check -l -d /dev/ttyUSB0 -t 60

    .. code-block:: bash

        -------------------------------------------------------------------------------
        Define options for device /dev/ttyUSB0
        Start network
        Wait for network (30s)
        Network is ready
        -------------------------------------------------------------------------------
        Controller capabilities : {'primaryController', 'staticUpdateController'}
        Controller node capabilities : {'listening', 'primaryController', 'staticUpdateController', 'beaming'}
        Nodes in network : 4
        Driver statistics : {'noack': 6, 'routedbusy': 0, 'readCnt': 115, 'ACKWaiting': 0, 'badChecksum': 0, 'broadcastReadCnt': 0, 'NAKCnt': 0, 'broadcastWriteCnt': 9, 'dropped': 0, 'CANCnt': 0, 'callbacks': 0, 'OOFCnt': 0, 'readAborts': 0, 'badroutes': 0, 'SOFCnt': 115, 'netbusy': 0, 'writeCnt': 49, 'nondelivery': 0, 'ACKCnt': 49, 'retries': 0}
        ------------------------------------------------------------
        1 - Name :  ( Location :  )
         1 - Ready : True / Awake : True / Failed : False
         1 - Manufacturer : Aeotec  ( id : 0x0086 )
         1 - Product : DSA02203 Z-Stick S2 ( id  : 0x0001 / type : 0x0002 )
         1 - Version : 3 / Secured : False / Zwave+ : False
         1 - Command classes : {'COMMAND_CLASS_NO_OPERATION', 'COMMAND_CLASS_BASIC'}
         1 - Capabilities : {'staticUpdateController', 'listening', 'primaryController', 'beaming'}
         1 - Neigbors : {4} / Power level : None
         1 - Is sleeping : False / Can wake-up : False / Battery level : None

        ...
        
        ------------------------------------------------------------
        4 - Name :  ( Location :  )
         4 - Ready : True / Awake : True / Failed : False
         4 - Manufacturer : GreenWave  ( id : 0x0099 )
         4 - Product : PowerNode 6 port ( id  : 0x0004 / type : 0x0003 )
         4 - Version : 4 / Secured : False / Zwave+ : False
         4 - Command classes : {'COMMAND_CLASS_BASIC', 'COMMAND_CLASS_CONFIGURATION', 'COMMAND_CLASS_SWITCH_BINARY', 'COMMAND_CLASS_VERSION', 'COMMAND_CLASS_CRC_16_ENCAP', 'COMMAND_CLASS_MANUFACTURER_SPECIFIC', 'COMMAND_CLASS_ASSOCIATION', 'COMMAND_CLASS_MULTI_INSTANCE/CHANNEL', 'COMMAND_CLASS_METER', 'COMMAND_CLASS_PROTECTION', 'COMMAND_CLASS_NO_OPERATION', 'COMMAND_CLASS_SWITCH_ALL'}
         4 - Capabilities : {'listening', 'routing', 'beaming'}
         4 - Neigbors : {1} / Power level : None
         4 - Is sleeping : False / Can wake-up : False / Battery level : None
         
         ...
         

 - The old manager is now available via the pyozw_shell command. You need to install module "urwid>=1.1.1" with pip before using it.

 - libopenzwave and openzwave python modules are packaged in the python_openzwave. 
   So developers needs to update their install_requires (it works fine with pyozw_manager). 
   They can use the following code to update softly :

    .. code-block:: python
    
        pyozw_version='0.4.1'
    
        def install_requires():
            try:
                import python_openzwave
                return ['python_openzwave==%s' % pyozw_version]
            except ImportError:
                pass
            try:
                import libopenzwave
                return ['openzwave==%s' % pyozw_version]
            except ImportError:
                pass
            return ['python_openzwave == %s' % pyozw_version]


 - If you already have an 0.3.x version installed, you should update your installation as usual. Don't install it with pip as it can break your installation (maybe not if you don't remove old modules)

 - Support for windows, macosx, ... is not tested. Feel free to report bug and patches. We can try to support these plateforms. Don't have Windows at home so I can't help. Same for mac.

 - Old installation process is deprecated and reserved for python-openzwave-developers and alternatives machines.

 - Please report your successful installations here : https://github.com/OpenZWave/python-openzwave/issues/73

Support
=======
You can ask for support on the google group : http://groups.google.com/d/forum/python-openzwave-discuss.

Please don't ask for support in github issues or by email.

Pull requests
=============
Please read DEVEL documentation before submitting pull request.
A lot of project tasks are done automatically or with makefile, so they must be done in a certain place or in a special order.
