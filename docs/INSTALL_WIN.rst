:orphan:

======================================
Installing python-openzwave on Windows
======================================


This HOW-TO is for 0.4.X.

It should be possible to make it pip friendly. Need a command line to build openzwave c++ lib.

Install Microsoft tools
=======================

This package use MSBuild.exe to build openzwave code.
You can find it in Visual Studio 2017 or Visual Studio 2015.
It's also possible to get them as a separate package.

Only release 14.0 and 15.0 are tested.

Install other tools
===================

You need git to clone the repository and python.

Install python's eggs :

 - for python 2.7 :
  
    .. code-block:: bash
  
        (venvX) pip install cython wheel six Louie

 - for python 3 :
  
    .. code-block:: bash
  
        (venvX) pip install cython wheel six PyDispatcher


To be continued ...

How To Build python-openzwave on Windows with VS2015 (deprecated)
=================================================================

Assuming Python 3.5 is set in PATH
Assuming your python environment has pip, cython, setuptools


Get sources
-----------

.. code-block:: bash

    git clone https://github.com/openzwave/python-openzwave.git

    cd python-openzwave
    git clone git://github.com/OpenZWave/open-zwave.git openzwave

    cd openzwave
    git checkout Dev
    cd ..
    git checkout


Build open-zwave
----------------

Open openzwave/cpp/build/windows/vs2010/OpenZWave.sln in Visual Studio

When asked, accept the project upgrade to VS2015

Build Win32|Release


Build python_openzwave
----------------------

From a Command Prompt, install it :

.. code-block:: bash

    python setup install --dev

Reference for 0.3.X : https://github.com/OpenZWave/python-openzwave/issues/53

Cygwin
------
python3
