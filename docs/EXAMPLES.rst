================
python-openzwave
================

You don't need to install (but building it) python-openzwave to test examples.


ozwsh
=====

A shell manager for your ZWave network. It use urwid and louie python extensions.
If needed, type the following command to install them :

    sudo pip install urwid louie

Start ozwsh with :

    ./ozwsh.sh --device=/dev/yourzwavestick

It allows :

    * Reset controller (hard and soft) and add/remove device/controller

    * Change node informations (name, location, ... )

    * view and change values informations

    * view and change group informations

    * Full management of scenes, switches, dimmers and sensors

It's a shell like manager. You can visit your zwave network using the
command cd. All available commands are displayed on every sceens.

For the developpers : this a good example on how to use the api.
Update are sent to uwird widget using louie notifications. ZWave data
updates are done in the set, add, delete, remove, ... methods.

There is some others examples, to test them :

    cd examples

    ./build_examples.sh

This will install all the needed files used by the examples in a temporary
directory.

api_demo
========

A test demo for the api : it list all nodes/values on your network, trying
to identify your switches, dimmers and sensors.

Start it with :

    ./api_demo.py --device=/dev/yourzwavestick

test_lib
========

A test demo for the library : connect to the network and sniff for notifications.

Start it with :

    ./test_lib.py --device=/dev/yourzwavestick --sniff=30

api_snif
========

A test demo for the api : connect to the api and sniff for louie signal from it.

Start it with :

    ./api_sniff.py --device=/dev/yourzwavestick --sniff=30

memory_use
==========

Try to evaluate the memory use of the api.

Start it with :

    ./memory_use.py --device=/dev/yourzwavestick

Other examples
==============

manager : my first try to use uwird. I don't think I will developp it anymore.
Feel free to fork it.

The old directory contains examples of py-openzwave (the ancestor of python-openzwave),
feel free to upgrade them.

If you develop some examples using python-openzwave library, send us the sources,
they will be addes to examples.
