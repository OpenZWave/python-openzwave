:orphan:

======================
Developers information
======================

How to develop for python-openzwave
===================================

Fork the project on Github.

Get the sources :

.. code-block:: bash

    git clone https://github.com/yourname/python-openzwave

You can install all the dependances to develop for python-openzwave using the command :

.. code-block:: bash

    sudo make developer-deps

You must now install python-openzwave in develop mode. Depending on which python versin you prefer, use :

.. code-block:: bash

    make venv2-dev

or
    
.. code-block:: bash

    make venv2-dev

Keep in mind that your update must be python 2 / python 3 compatible.

Develop, test, debug, test, ... :)

Update the documentation if needed. You surely found the documentation useful, so please keep it up to date.

It a good idea to add automatic tests.

Launch the full test suite (for python 2 and python 3) :

.. code-block:: bash

    make venv-tests

At last but not least, submit your request with the result of tests in the comment.

If you don't follow the previous steps, your PR will be refused or letting in pending state until I've got time to test it.

Documentation
=============

First, install the dependances :

.. code-block:: bash

    sudo make doc-deps

Documentation is managed with sphinx.

Don't utpdate txt and rst files (README, INSTALL, ...) in the root directory, update the RST sources in docs.

