:orphan:

================
python-openzwave
================

You need to install and build python-openzwave to test examples.

pyozwman
========

A shell manager for your ZWave network : :doc:`PyOzwMan documentation </pyozwman>`

pyozwweb
========

A Flask + socket.io + jquery web application framework for your ZWave network : :doc:`PyOzwWeb documentation </pyozwweb>`

api_demo
========

A test demo for the api : it list all nodes/values on your network, trying
to identify your switches, dimmers and sensors.

Start it with :

.. code-block:: bash

    ./api_demo.py --device=/dev/yourzwavestick

test_lib
========

A test demo for the library : connect to the network and sniff for notifications.

Start it with :

.. code-block:: bash

    ./test_lib.py --device=/dev/yourzwavestick --sniff=30

api_snif
========

A test demo for the api : connect to the api and sniff for louie signal from it.

Start it with :

.. code-block:: bash

    ./api_sniff.py --device=/dev/yourzwavestick --sniff=30

memory_use
==========

Try to evaluate the memory use of the api.

Start it with :

.. code-block:: bash

    ./memory_use.py --device=/dev/yourzwavestick
