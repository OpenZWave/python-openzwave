:orphan:

========================================
Installing python-openzwave from archive
========================================

This is the simplest (and the fastest) way to install python-openzwave. It comes with openzwave source files and is already cythonized.

This is surely the best solution to install python-openzwave on a raspberry pi.

Get archive of python-openzwave
===============================

You are now ready to download sources of python-openzwave here :

.. code-block:: bash

    https://github.com/OpenZWave/python-openzwave/tree/master/archives

This archive contains sources of python-openzwave and openzwave.

.. code-block:: bash

    tar xvzf python-openzwave-X.Y.Z.tar.gz

This command will extract all the needed sources. And change to the right directory.

.. code-block:: bash

    cd python-openzwave-X.Y.Z

Install the needed tools
========================

You must install git and other tools to get sources of python-openzwave and
openzwave and build them. Look at the documentation of your Linux distribution to do that.

On a debian like distribution :

.. code-block:: bash

    sudo make deps

Build process
=============

Now, you can compile sources :

.. code-block:: bash

    make build

If you have already built python-openzwave or if the build failed
you can use the clean target and build again :

.. code-block:: bash

    sudo make clean
    make build

Do not use root to build python-openzwave as root it will surely fails. Please use a "normal user".


Installation
============

You can now install the packages using the following command :

.. code-block:: bash

    sudo make install

You can remove python-openzwave using :

.. code-block:: bash

    sudo make uninstall

If it fails
===========

Simply remove the python-openzwave-x.y.z directory and extract it again.

