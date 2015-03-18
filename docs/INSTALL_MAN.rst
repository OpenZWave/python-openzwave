================================
Manual installation instructions
================================

If you can't build python-openzwave using other instruction you can try to
install it using this method.


Install the needed tools
========================

You must install git and other tools to get sources of python-openzwave and
openzwave. Look at the documentation of your Linux distribution to do that.

On a debian like distribution :

.. code-block:: bash

    sudo apt-get install git python-pip python-dev cython

You also need some python modules, on a debian like distribution :

.. code-block:: bash

    sudo apt-get install python-dev python-setuptools python-louie

You need sphinx and make to generate the documentation.

TODO : installation for python 3

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

    git clone git@github.com:bibi21000/python-openzwave.git

Go to the python-openzwave directory and grab the sources of openzwave

.. code-block:: bash

    git clone git://github.com/OpenZWave/open-zwave.git openzwave


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
