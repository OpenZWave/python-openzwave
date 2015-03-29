:orphan:

================
python-openzwave
================

This is the new generation of python-openzwave.

python-openzwave is a python wrapper for the openzwave library.
It's also contains an api (object representation of Zwave network) and ozwsh (a shell like manager using the api).

You can install python-openzwave in 3 ways :

    * From repository : you need to install mercurial, subversion and the common builds tools. Look at INSTALL_REPO to do such installation

    * From an archive : you don't need to install mercurial, subversion. Only the common builds tools are needed. Look at INSTALL_ARCH to do such installation

    * From scratch : if you can't build python-openzwave automatically or you are using windows or MacOS X. Look at INSTALL_MAN to do such installation

Migrating from python-openzwave 0.2.X to 0.3.0
==============================================

This version (0.3.0) is under development, do not use it in a production environnement.

I need to update source tree of python-openzwave and modules's names because of a bug in setuptools : https://bitbucket.org/pypa/setuptools/issue/230/develop-mode-does-not-respect-src.
Sorry for that.

So, beforre building python-openzwave, you must uninstall the old version :

.. code-block:: bash

    sudo make uninstall

After that, reinstall python-openzwave usinf your prefered method.

If you have problems, please submit an issue with :

 - the content of the directory /usr/local/lib/python2.7/dist-packages/ (for python2.7)
 - the content of /usr/local/lib/python2.7/dist-packages/easy-install.pth (for python 2.7)

Testing python-openzwave
========================

After installing python-openzwave, you can run tests :

.. code-block:: bash

    sudo make tests

To do
=====

- Improve tests : add virtual nodes and controllers to pass test on travis
- ...

