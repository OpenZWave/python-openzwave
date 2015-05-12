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

    git clone https://github.com/OpenZWave/python-openzwave

The previous command will create a copy of the official repository on your
computer in a directory called python-openzwave.


Install dependencies
====================
You need some tools (a c++ compiler, headers dir python, ...) to build python-openzwave and openzwave library.

On a debian like distribution :

.. code-block:: bash

    sudo make repo-deps

For non-debian (fedora, ...), you can retrieve the packages needed in the Makefile.


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

Or if you have already build python-openzwave in a previous installation, you can use the clean target to remove old builds.

.. code-block:: bash

    sudo make clean


Installation
============
You can now ready to install the eggs using the following command :

.. code-block:: bash

    sudo make install

You can also remove python-openzwave using :

.. code-block:: bash

    sudo make uninstall


Running tests
=============
You can launch the regression tests using :

.. code-block:: bash

    make tests

Keep in mind that the tests will "play" with your nodes : switching on and off, dimming, adding and removing scenes, ...


About the repositroy
====================
This repository is a development tool, so it might be "unstable" ... yeah, sometimes it won't build anymore :)

If you want to retrieve the last "good" commit, look at https://github.com/OpenZWave/python-openzwave/commits/master.
The commits names "Auto-commit for docs" are done after the full process : build + test + docs, so they might be "working" (almost for me).
