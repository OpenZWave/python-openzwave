:orphan:

================
python-openzwave
================

python-openzwave is a python wrapper for the openzwave c++ library : https://github.com/OpenZWave/open-zwave

 * full manager implementation with options
 * an API to map the ZWave network in Python objects
 * a full-event webapp example : flask + socket.io + jquery (Look at API documentation to try it)
 * a suite of tests
 * many examples

python-openzwave 0.3.0-alpha2 is out !!!
========================================

Look at CHANGELOG to see new features, to do list and release notes.

Look at INSTALL_REPO to test it now !!!

==============================================
Migrating from python-openzwave 0.2.X to 0.3.0
==============================================

I need to update source tree of python-openzwave and modules's names because of a bug in setuptools : https://bitbucket.org/pypa/setuptools/issue/230/develop-mode-does-not-respect-src .
Sorry for that.

Update your sources:

.. code-block:: bash

    git pull

Before building python-openzwave 0.3.0, you must uninstall the old version :

.. code-block:: bash

    sudo make uninstall

About cython : I've made many tests using cython installed via pip : (0.20, 0.21 and 0.22).
Compilation is ok but a segfault appears when launching the tests. Please remove it.

.. code-block:: bash

    sudo pip uninstall Cython

You also need to make some minor updates in you code, look at CHANGELOG

If you have problems, please submit an issue with :

 - cython -V
 - the content of the directory /usr/local/lib/python2.7/dist-packages/ (for python2.7)
 - the content of /usr/local/lib/python2.7/dist-packages/easy-install.pth (for python 2.7)



