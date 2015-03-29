:orphan:

=============================================
Installing python-openzwave from repositories
=============================================


Install the needed tools
========================

You must install git and other tools to get sources of python-openzwave and
openzwave and build them. Look at the documentation of your Linux distribution to do that.

On a debian like distribution :

.. code-block:: bash

    sudo make deps

Get archive of python-openzwave
===============================

You are now ready to download sources of python-openzwave here :

.. code-block:: bash

    http://bibi21000.no-ip.biz/python-openzwave/

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

    make build

Or if you have already build python-openzwave in a previous installation,
you can use the clean option to remove old builds.

.. code-block:: bash

    make clean
    make build

Installation
============

You can now install the packages using the following command will.

.. code-block:: bash

    sudo make install

The installation script create a list of installed files. So you can remove
python-openzwave using the following command :

.. code-block:: bash

    sudo make uninstall
