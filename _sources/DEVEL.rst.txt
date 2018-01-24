:orphan:

======================
Developers information
======================

How to develop for python-openzwave
===================================

Get the sources

.. code-block:: bash

    git clone https://github.com/OpenZWave/python-openzwave

You can install all the dependances to develop for python-openzwave using the command :

.. code-block:: bash

    sudo make developer-deps

You must now install python-openzwave in develop mode

.. code-block:: bash

    make develop

Your password will be asked (by sudo) for installing eggs in your local directory.

Develop, test, debug, test, ... :)

Update the documentation if needed. You surely found the documentation useful, so please keep it up to date.

You can create an account on travis or docker to run the tests.

At last but not least, submit your request.

How to develop for libopenzwave (was python-openzwave-lib)
==========================================================
After updating the pyx, you need to reinstall it. Otherwise, your changes will not be applied :

.. code-block:: bash

    make develop

Tests
=====

First, install the dependances :

.. code-block:: bash

    sudo make tests-deps

To launch all the tests suite (about 140 tests), use the following command :

.. code-block:: bash

    make tests

To launch particular tests :

.. code-block:: bash

    nosetests --verbosity=2 tests/api/test_controller_command.py

Some tests need manual operations (ie to add a node, to remove one, ...). For example, to test the remove node, use :

.. code-block:: bash

    export MANUALSKIP='False' && nosetests --verbosity=2 tests/api/test_controller_command.py -m test_150 && unset MANUALSKIP
    test_150_command_remove_node_and_wait_for_user (tests.api.test_controller_command.TestControllerCommand) ... ok

    ----------------------------------------------------------------------
    Ran 1 test in 16.031s

    OK

You should push the inclusion button of the node before the end of the test.

Some tests don't need a ZWave Stick to be launched, so they can be run on the autobuilders (travis, docker, ...). Place them in the autobuild directory.

Travis-ci, Docker Hub, nosetests and pylint are used to test quality of code. There reports are here :

 - Docker : https://registry.hub.docker.com/u/bibi21000/python-openzwave/
 - Travis : https://travis-ci.org/bibi21000/python-openzwave
 - `Nosetests report <file:../nosetests/nosetests.html>`_
 - `Coverage report <file:../coverage/index.html>`_
 - `Pylint report <file:../pylint/report.html>`_

Documentation
=============

First, install the dependances :

.. code-block:: bash

    sudo make doc-deps

Documentation is managed with sphinx.
Don't utpdate txt files (README, INSTALL, ...), update the RST sources in docs.
Use the following commands to generate all docs files (txt, html and joomla)

You need to have installed python-openzwave (in either develop or install mode) before generating the documentation.

.. code-block:: bash

    make docs

Static vs dynamic (or shared)
=============================
The openzwave (c++) lib needs to run as a singleton : it means that it MUST have only one instance of the manager running on your computer.

There is 2 ways of linking libraries with a program :

    * static : includes a copy of the library in your binary program.
      This means that your program has its own instance of the library.
      This the way the install.sh runs.
      So you CAN'T have another program (like the control-panel) running when using the python-openzwave library

    * dynamic or shared : includes a link to the library in your binary program.
      This means that your program share the library with other programs.
      In this case, the instance is owned directly by the library.
      This the way the debian package works. So you CAN have another program running when using the python-openzwave library.
      Of course, this program MUST use the shared library too.

About sudo
==========
If you are like me and don't like root (and sudo), you can use the following tip to install packages via pip :

Look at your python local library, it should looks like :

.. code-block:: bash

  ls -lisa /usr/local/lib/python2.7/dist-packages/
  total 2428
  1445174  12 drwxrwsr-x 115 root staff  12288 avril  9 21:35 .
  1445172   4 drwxrwsr-x   4 root staff   4096 mai    2  2014 ..
  1457164   4 drwxr-sr-x   5 root staff   4096 nov.  26  2013 actdiag
  1715480   4 drwxr-sr-x   2 root staff   4096 nov.  26  2013 actdiag-0.5.1.egg-info
  1457163   4 -rw-r--r--   1 root staff   1004 nov.  26  2013 actdiag_sphinxhelper.py
  1457172   4 -rw-r--r--   1 root staff    620 nov.  26  2013 actdiag_sphinxhelper.pyc
  ....

So, add your common user to the staff group :

.. code-block:: bash

  sudo usermod -a -G staff userName

Add the write right to the group staff

.. code-block:: bash

  sudo chmod -Rf g+w /usr/local/lib/python2.7/dist-packages/

And now, it's time log off and log on. Groups are checked when you open the session.

You can now install your packages without sudo.

Python3 and virtualenv
======================
Python 3 is actually not supported.

A branch (python3) has been created with a special Dockerfile. It build python-openzwave and launch some tests.
This branch is automatically merged from master at "make commit".

So please, do not directly push under python3 branch. Make your developments under master or another branch.

It's important for me have python2/python3 compatibilty in the master branch.
cython can help for this : http://docs.cython.org/src/tutorial/strings.html

The Makefile sill try to automatically configure your version of python (running python --version).

If you want to install python-openzwave in a python virtual environnement, you should use something like :

.. code-block:: bash

    make VIRTUAL_ENV=/path/to/my/venv ...

If you use python 3 and your python executable is called python3 :

.. code-block:: bash

    make PYTHON_EXEC=python3 ...

You can also put these variables in a CONFIG.make file instead of passing them to the command line
