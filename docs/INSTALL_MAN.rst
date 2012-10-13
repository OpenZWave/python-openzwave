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

    sudo apt-get install mercurial subversion

You need cython (0.14 or 0.15) to compile the python library (libopenzwave.pyx).
Some users have reported errors when using 0.16. You also need some python depencies

On a debian like distribution :

    sudo apt-get install cython python-dev python-setuptools python-louie

You need sphinx and make to generate the documentation.

On a debian like distribution :

    sudo apt-get install python-sphinx make

To compile the openzwave library, you need the common builds tools
and the libudev developments headers.

On a debian like distribution :

    sudo apt-get install build-essential libudev-dev g++

Get sources of python-openzwave and open-zwave
==============================================

You are now ready to download sources of python-openzwave :

    hg clone https://code.google.com/p/python-openzwave/

Go to the python-openzwave directory and grab the sources of openzwave

	svn checkout http://open-zwave.googlecode.com/svn/trunk/ openzwave

Build openzwave and python-openzwave
====================================

Go to the openzwave directory and build it :

	cd openzwave/cpp/build/linux
	make
	cd ../../../..

Build python-openzwave

	python setup-lib.py build
	python setup-api.py build

And install them
================

	sudo python setup-lib.py install
	sudo python setup-api.py install
