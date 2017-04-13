:orphan:

======================================
Installing python-openzwave on Windows
======================================


This HOW-TO is for 0.4.X.

It should be possible to make it pip friendly. Need a command line to build openzwave c++ lib.

How To Build python-openzwave on Windows with VS2015
====================================================

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

