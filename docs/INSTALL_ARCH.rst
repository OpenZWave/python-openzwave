=============================================
Installing python-openzwave from repositories
=============================================


Install the needed tools
========================

You need cython (0.14) to compile the python library (libopenzwave.pyx).
Some users have reported errors when using 0.16 or 0.17.
Some 64 bits users reports segfault when using examples. Seems that using cython 0.15 was the problem.
Gentoo users : don't use cython that is shipped with your distribution.

Install pip 

.. code-block:: bash

    sudo apt-get install python-pip python-dev

And use it to install cython.

.. code-block:: bash

    sudo pip install cython==0.14

You also need some python modules, on a debian like distribution :

.. code-block:: bash

    sudo apt-get install python-dev python-setuptools python-louie

To compile the openzwave library, you need the common builds tools
and the libudev developments headers.

On a debian like distribution :

.. code-block:: bash

    sudo apt-get install build-essential libudev-dev g++ make


Get archive of python-openzwave
===============================

You are now ready to download sources of python-openzwave here :

.. code-block:: bash

    http://code.google.com/p/python-openzwave/downloads/list

This archive contains sources of python-openzwave and openzwave.

.. code-block:: bash

    tar xvzf python-openzwave-X.Y.Z.tar.gz

This command will extract all the needed sources.


Build process
=============

Go to the previously created directory :

.. code-block:: bash

    cd python-openzwave-X.Y.Z.tar.gz

Now, you can compile sources :

.. code-block:: bash

    ./compile.sh

Or if you have already build python-openzwave in a previous installation,
you can use the clean option to remove old builds.

.. code-block:: bash

    ./compile.sh clean


Installation
============

You can now install the packages using the following command will.

.. code-block:: bash

    sudo ./install.sh

The installation script create a list of installed files. So you can remove
python-openzwave using the following command :

.. code-block:: bash

    sudo ./uninstall.sh
