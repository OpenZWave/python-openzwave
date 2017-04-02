.. image:: https://travis-ci.org/OpenZWave/python-openzwave.svg?branch=master
    :target: https://travis-ci.org/OpenZWave/python-openzwave
    :alt: Travis status

.. image:: https://circleci.com/gh/OpenZWave/python-openzwave.png?style=shield
    :target: https://circleci.com/gh/OpenZWave/python-openzwave
    :alt: Circle status

================
python-openzwave
================

python-openzwave is a python wrapper for the openzwave c++ library : https://github.com/OpenZWave/open-zwave

 * full manager implementation with options
 * an API to map the ZWave network in Python objects
 * a command line manager to manage / debug your ZWave network
 * a full-event webapp example : flask + socket.io + jquery
 * a suite of tests
 * many examples

python-openzwave 0.3.0 is out !!!
=================================

Look at CHANGELOG to see new features and release notes.

Look at INSTALL_REPO to test it now.

Look at INSTALL_ARCH to install from archive : no need to install cython anymore.

Support
=======
You can ask for support on the google group : http://groups.google.com/d/forum/python-openzwave-discuss.

Please don't ask for support in github issues or by email.

Pull requests
=============
Please read DEVEL documentation before submitting pull request.
A lot of project tasks are done automatically or with makefile, so they must be done in a certain place or in a special order.

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


Ubuntu 64bits ... and the others
================================

If you're using Ubuntu 64 bits (and mayde others) and keep your distribution up to date,
you certainly have the segfault problem.

Ubuntu 12.04 and 14.04 seems to be affected by this bug. Ubuntu 15.10 and Debian Jessie not.

It appears with the last update of python :

.. code-block:: bash

    $ python
    Python 2.7.6 (default, Jun 22 2015, 17:58:13)
    [GCC 4.8.2] on linux2
    Type "help", "copyright", "credits" or "license" for more information.


I've open a discussion on cython-users here : https://groups.google.com/forum/#!topic/cython-users/mRsviGuCFOk

The only way I found to avoid this is to rebuild and reinstall the old release of python :

.. code-block:: bash

    wget https://launchpad.net/ubuntu/+archive/primary/+files/python2.7_2.7.6-8.dsc https://launchpad.net/ubuntu/+archive/primary/+files/python2.7_2.7.6.orig.tar.gz https://launchpad.net/ubuntu/+archive/primary/+files/python2.7_2.7.6-8.diff.gz

    dpkg-source -x python2.7_2.7.6-8.dsc

    sudo apt-get build-dep python2.7

    cd python2.7-2.7.6

    dpkg-buildpackage

Wait, wait and await again :)

.. code-block:: bash

    cd ..

    sudo dpkg -i *.deb

To prevent future updates of python, you could mark its packages. For example, if you use apt to update your distribution, use the following command :

.. code-block:: bash

    sudo apt-mark hold idle-python2.7 libpython2.7-minimal python2.7-dbg python2.7-minimal libpython2.7 libpython2.7-stdlib python2.7-dev libpython2.7-dbg  libpython2.7-testsuite python2.7-doc libpython2.7-dev python2.7 python2.7-examples

Some users have reported that building python-openzwave using the archive (INSTALL_ARCH) can also do the trick. Let me know if it works for you.
