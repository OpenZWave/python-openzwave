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

You need sphinx and make to generate the documentation.

On a debian like distribution :

.. code-block:: bash

    sudo apt-get install python-sphinx make

You also need to install some sphinx contributions :

.. code-block:: bash

    sudo pip install sphinxcontrib-blockdiag sphinxcontrib-actdiag
    sudo pip install sphinxcontrib-nwdiag sphinxcontrib-seqdiag

To compile the openzwave library, you need the common builds tools
and the libudev developments headers.

On a debian like distribution :

.. code-block:: bash

    sudo apt-get install build-essential libudev-dev g++


Get sources of python-openzwave
===============================

You are now ready to download sources of python-openzwave :

.. code-block:: bash

    git clone https://github.com/bibi21000/python-openzwave

The previous command will create a copy of the official repository on your
computer in a directory called python-openzwave.


Update and build process
========================

Go to the previously created directory

.. code-block:: bash

    cd python-openzwave

The following command will update your local repository to the last release
of python-openzwave and openzwave.

.. code-block:: bash

    ./update.sh

When update process is done, you can compile sources

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
