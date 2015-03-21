:orphan:

=======================
Developpers information
=======================

How to develop for python-openzwave
===================================

Get the sources

.. code-block:: bash

    git clone https://github.com/bibi21000/python-openzwave

You must now install python-openzwave in develop mode

.. code-block:: bash

    make develop

Your password will be asked (by sudo) for installing eggs in your local directory.

Develop, test, debug, test, ... :)

Update the documentation if needed. You surely found the documentation useful, so please keep it up to date

You can create an account on travis to run the (futurs) tests.

At last but not least, submit your request


Documentation
=============

Documentation is managed with sphinx.
Don't utpdate txt files (README, INSTALL, ...), update the RST sources in docs.
Use the following commands to generate all docs files (txt, html and joomla)

You need to have installed python-openzave (in either develop or install mode) before generating the documentation.

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

Migrate from py-openzwave to python-openzwave
=============================================

Remove the old py-openzwave

.. code-block:: bash

    find /usr -iname openzwave.so

This command show the list of files naming openzwave.so in /usr, ie /usr/local/lib/python2.7/dist-package/openzwave.so

Remove it :

.. code-block:: bash

    sudo rm /usr/local/lib/python2.7/dist-package/openzwave.so

Install the new version of python-openzwave : look at README

Update your code :

Everywhere in your code replace :

 .. code-block:: bash

   "import openzwave" to "import libopenzwave" "from openzwave" to "from libopenzwave"

notifications :

In Maarten py-openzwave librairy, value is a string but in python-openzwave, it's a value of the right type :

.. code-block:: python

    # 'value' : value.c_str(),

    'value' : getValueFromType(manager,v.GetId?()),

wrapper : The wrapper is no longer supported.

Now high level acces to ZWave network is provided by the API

