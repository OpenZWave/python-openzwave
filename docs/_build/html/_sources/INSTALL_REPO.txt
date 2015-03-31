:orphan:

===========================================
Installing python-openzwave from repository
===========================================


Install the needed tools
========================

You must install git and make to retrieve sources of python-openzwave and
openzwave.

On a debian like distribution :

.. code-block:: bash

    sudo apt-get install -y git make


Get sources of python-openzwave
===============================

You are now ready to download sources of python-openzwave :

.. code-block:: bash

    git clone https://github.com/bibi21000/python-openzwave

The previous command will create a copy of the official repository on your
computer in a directory called python-openzwave.

Install dependencies
====================

You need some tools (a c++ compiler, headers dir python, ...) to build python-openzwave and openzwave library.

On a debian like distribution :

.. code-block:: bash

    sudo make deps

For non-debian (fedora, ...), you can retrieve the packages needed in the Makefile.

If you want to build the documentatation, you also need to install sphinx and some contributions :

On a debian like distribution :

.. code-block:: bash

    sudo apt-get install python-sphinx

You also need to install some sphinx contributions :

.. code-block:: bash

    sudo pip install sphinxcontrib-blockdiag sphinxcontrib-actdiag
    sudo pip install sphinxcontrib-nwdiag sphinxcontrib-seqdiag

Update and build process
========================

Go to the previously created directory

.. code-block:: bash

    cd python-openzwave

The following command will update your local repository to the last release
of python-openzwave and openzwave.

.. code-block:: bash

    make update

When update process is done, you can compile sources

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

Python3 and virtualenv
======================

The Makefile sill try to automatically configure your version of python (running python --version).

If you want to install python-openzwave in a python virtual environnement, you should use something like :

.. code-block:: bash

    make VIRTUAL_ENV=/path/to/my/venv build

If you use python 3 and your python executable is called python3 :

.. code-block:: bash

    make PYTHON_EXEC=python3 build

You can also put these variables in a CONFIG.make file instead of passing them to the command line

