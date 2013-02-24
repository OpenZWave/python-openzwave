================================
Manual installation instructions
================================

If you can't build python-openzwave using other instruction you can try to
install it using this method.


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


Get sources of python-openzwave and open-zwave
==============================================

You are now ready to download sources of python-openzwave :

.. code-block:: bash

    hg clone https://code.google.com/p/python-openzwave/

Go to the python-openzwave directory and grab the sources of openzwave

.. code-block:: bash

    svn checkout http://open-zwave.googlecode.com/svn/trunk/ openzwave


Build openzwave and python-openzwave
====================================

Go to the openzwave directory and build it :

.. code-block:: bash

    cd openzwave/cpp/build/linux
    make
    cd ../../../..

Build python-openzwave

.. code-block:: bash

    python setup-lib.py build
    python setup-api.py build


And install them
================

.. code-block:: bash

    sudo python setup-lib.py install
    sudo python setup-api.py install
