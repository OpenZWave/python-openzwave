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

    * Reset controller (hard and soft) and

    * Change node informations (name, location, ... )

    * view and change values informations

    * view and change group informations

    * Full management of scenes

It's a shell like manager. You can visit your zwave network using the
command cd. All available commands are displayed on every sceens.

For the developpers : this a good example on how to use the api.
Update are sent to uwird widget using louie notifications. ZWave data
updates are done in the set, add, delete, remove, ... methods.


api_demo
========

A test demo : it list all nodes/values on your network and activate
your switches.

Start it with :

    ./api_demo.sh --device=/dev/yourzwavestick


Other examples
==============

manager : my first try to use uwird. I don't think I will developp it anymore.
Feel free to fork it.

The old directory contains examples of py-openzwave (the ancestor of python-openzwave),
feel free to upgrade them.

If you develop some examples using python-openzwave library, send us the sources,
they will be addes to examples.
