:orphan:

PyOzwWeb documentation
======================

What it's
---------

This will be the next release of the manager in the future. It's also a good solution for a full event webapp (jquery + socketio)

Launching it
------------

Go to the right directory :

.. code-block:: bash

    cd src-web/pyozwweb

Update the config :

.. code-block:: bash

    vim app.conf

    [zwave]
    device = /dev/ttyUSB0

You can fine tune logging in logging.conf and run the app :

.. code-block:: bash

    ./run.py

And connect to http://127.0.0.1:5000 using your favorite browser.

You can also change the ip/port to allow remote connections :

.. code-block:: bash

    [server]
    host = 0.0.0.0
    port = 8080

Source
------

.. toctree::
    :maxdepth: 3

.. automodule:: pyozwweb.app.listener
    :members: ListenerThread
