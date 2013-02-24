=============================================
Installing python-openzwave from repositories
=============================================


Install the needed tools
========================

You must install mercurial and subversion to get sources of python-openzwave
and openzwave. Look at the documentation of your Linux distribution to do that.

On a debian like distribution :

.. code-block:: bash

    sudo apt-get install mercurial subversion

You need cython (0.14 or 0.15) to compile the python library (libopenzwave.pyx).
Some users have reported errors when using 0.16 or 0.17.
You can install a working version of cython using pip.

Note for 64 bits users : some users reports segfault when using examples. Seems that using cython==0.14 solve the problem.
Note for Gentoo users : don't use cython that is shipped with your distribution. Install it using pip.

.. code-block:: bash

    sudo pip install cython==0.15

You also need some python modules, on a debian like distribution :

.. code-block:: bash

    sudo apt-get install python-dev python-setuptools python-louie

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

    hg clone https://code.google.com/p/python-openzwave/

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
