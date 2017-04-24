.. image:: https://travis-ci.org/OpenZWave/python-openzwave.svg?branch=master
    :target: https://travis-ci.org/OpenZWave/python-openzwave
    :alt: Travis status

.. image:: https://circleci.com/gh/OpenZWave/python-openzwave.png?style=shield
    :target: https://circleci.com/gh/OpenZWave/python-openzwave
    :alt: Circle status

.. image:: https://img.shields.io/pypi/dm/python_openzwave.svg
    :target: https://pypi.python.org/pypi/python_openzwave
    :alt: Pypi downloads

.. image:: https://img.shields.io/pypi/format/python_openzwave.svg
    :target: https://pypi.python.org/pypi/python_openzwave
    :alt: Pypi format
    
.. image:: https://img.shields.io/pypi/status/python_openzwave.svg
    :target: https://pypi.python.org/pypi/python_openzwave
    :alt: Pypi status
    
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

python-openzwave 0.4.0 is coming !!!
====================================
 
 - 0.4.0.x versions are for testers only. Don't use it in a production environement !!!
 
 - New installation process via pip
 
 - First, you need some build tools and libs. On ubuntu, you should use :

     .. code-block:: bash

        sudo apt-get install --force-yes -y make libudev-dev g++ libyaml-dev

 - Make your virtualenv and activate it : 
 
    .. code-block:: bash

        virtualenv --python=python3 venv3
        source venv3/bin/activate

 - Install the default (embed) flavor :       
 
    .. code-block:: bash
    
        (venvX) pip install python_openzwave
    
 - The previous command install python_openzwave statitically linked to sources downloaded from https://github.com/OpenZWave/python-openzwave/tree/master/archives.
   You can change this using flavors. There is a bug in the package dependencies and flavors on some systems. You may need to install dependencies manualy :
 
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
    - embed_shared (experimental) : download sources from https://github.com/OpenZWave/python-openzwave/tree/master/archives, build and install as module on the system. 
      Python_openzwave use it. Need root access to install openzwave libs.
    - git_shared (experimental) : download sources from openzwave github, build and install them as module on the system.
      Python_openzwave use it. Need root access to install openzwave libs.
    - ozwdev and ozwdev_shared : use the dev branch of openzwave on github.
    - dev : for python_openzwave developpers

   
 - Install it :
 
    .. code-block:: bash
    
        (venvX) pip install python_openzwave --install-option="--flavor=git"

 - You can update to the last version of openzwave using the git flavor :
        
    .. code-block:: bash
    
        (venvX) pip uninstall -y python_openzwave
        (venvX) pip install python_openzwave --no-cache-dir --install-option="--flavor=git"
        
    
 - At last, you can launch pyozw_check:

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
    

 - The old manager is now available via the pyozw_shell command. You need to install module "urwid>=1.1.1" with pip before using it.

 - libopenzwave and openzwave python modules are packaged in the python_openzwave. 
   So developpers needs to update their install_requires (it works fine with pyozw_manager). 
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

python-openzwave 0.3.0 is out !!!
=================================

Look at CHANGELOG to see new features and release notes.

Look at INSTALL_REPO to test it now.

Look at INSTALL_ARCH to install from archive : no need to install cython anymore.

Support
=======
You can ask for support on the google group : http://groups.google.com/d/forum/python-openzwave-discuss.

Please don't ask for support in github issues or by email.

Pull requests
=============
Please read DEVEL documentation before submitting pull request.
A lot of project tasks are done automatically or with makefile, so they must be done in a certain place or in a special order.

Migrating from python-openzwave 0.2.X to 0.3.0
==============================================
I need to update source tree of python-openzwave and modules's names because of a bug in setuptools 
: https://bitbucket.org/pypa/setuptools/issue/230/develop-mode-does-not-respect-src .
Sorry for that.

Update your sources:

.. code-block:: bash

    git pull

Before building python-openzwave 0.3.0, you must uninstall the old version :

.. code-block:: bash

    sudo make uninstall

About cython : I've made many tests using cython installed via pip : (0.20, 0.21 and 0.22).
Compilation is ok but a segfault appears when launching the tests. Please remove it.

.. code-block:: bash

    sudo pip uninstall Cython

You also need to make some minor updates in you code, look at CHANGELOG

If you have problems, please submit an issue with :

 - cython -V
 - the content of the directory /usr/local/lib/python2.7/dist-packages/ (for python2.7)
 - the content of /usr/local/lib/python2.7/dist-packages/easy-install.pth (for python 2.7)


Ubuntu 64bits ... and the others
================================

If you're using Ubuntu 64 bits (and mayde others) and keep your distribution up to date,
you certainly have the segfault problem.

Ubuntu 12.04 and 14.04 seems to be affected by this bug. Ubuntu 15.10 and Debian Jessie not.

It appears with the last update of python :

.. code-block:: bash

    $ python
    Python 2.7.6 (default, Jun 22 2015, 17:58:13)
    [GCC 4.8.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.


I've open a discussion on cython-users here : https://groups.google.com/forum/#!topic/cython-users/mRsviGuCFOk

The only way I found to avoid this is to rebuild and reinstall the old release of python :

.. code-block:: bash

    wget https://launchpad.net/ubuntu/+archive/primary/+files/python2.7_2.7.6-8.dsc https://launchpad.net/ubuntu/+archive/primary/+files/python2.7_2.7.6.orig.tar.gz https://launchpad.net/ubuntu/+archive/primary/+files/python2.7_2.7.6-8.diff.gz

    dpkg-source -x python2.7_2.7.6-8.dsc

    sudo apt-get build-dep python2.7

    cd python2.7-2.7.6

    dpkg-buildpackage

Wait, wait and await again :)

.. code-block:: bash

    cd ..

    sudo dpkg -i *.deb

To prevent future updates of python, you could mark its packages. For example, if you use apt to update your distribution, use the following command :

.. code-block:: bash

    sudo apt-mark hold idle-python2.7 libpython2.7-minimal python2.7-dbg python2.7-minimal libpython2.7 libpython2.7-stdlib python2.7-dev libpython2.7-dbg  libpython2.7-testsuite python2.7-doc libpython2.7-dev python2.7 python2.7-examples

Some users have reported that building python-openzwave using the archive (INSTALL_ARCH) can also do the trick. Let me know if it works for you.
