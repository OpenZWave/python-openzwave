:orphan:

PyOzwMan documentation
======================

A shell manager for your ZWave network

It use urwid and louie python extensions.
If needed, type the following command to install them :

Start ozwsh with :

.. code-block:: bash

    ozwsh --device=/dev/yourzwavestick

Use the --help option to get all available options :

.. code-block:: bash

    ozwsh --help

With PyOzwMan, you can :

    * Reset controller (hard and soft) and add/remove device/controller
    * Change node informations (name, location, ... )
    * view and change values informations
    * view and change group informations
    * view and change config parameters
    * view and change gassociations
    * Full management of scenes, switches, dimmers and sensors

It's a shell like manager. You can visit your zwave network using the
command cd. All available commands are displayed on every screens.
You can use the tab keys to switch between the view panel and the edit panel
and the up and down ones to view all informations.

For the developers : this provides a good example on how to use the api.
Update are sent to uwird widget using louie notifications. ZWave data
updates are done in the set, add, delete, remove, ... methods.
