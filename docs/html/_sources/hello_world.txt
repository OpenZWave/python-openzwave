:orphan:

============================
python-openzwave hello_world
============================

Here is the hello_world example for the python-openzwave API. In this
tutorial we will implement a simple sniffer. The full code is available
in the examples directory : hello_world.py.

Some theory
===========

OpenZwave uses the mechanism of notifications to manage events network.
When the driver is ready, the node is added, a value is modified, ... openzwave
generates a notification you must catch with a callback function.

Python-openzwave API catch the notification and send a louie signal.

Some words about python-louie : it's a simple mechanism where a dispatcher
send a signal on a channel, and clients connect to him.

Here is the way a sender dispatch a signal :

.. code-block:: python

     dispatcher.send(self.SIGNAL_NODE, **{'network': self, 'node':self.nodes[args['nodeId']]})

Here is the way a client connect to a channel :

.. code-block:: python

    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)

The first argument is a call back function :

.. code-block:: python

    def louie_node_update(network, node):
        print('Louie signal : Node update : %s.' % node)

It receives as parameters the ones populate by the sender : the network ans a node in ths case.
The callback must set its parameter names as the same as the sender.

Hello from ZWave
================

The import clauses :

.. code-block:: python

    import openzwave
    from openzwave.node import ZWaveNode
    from openzwave.value import ZWaveValue
    from openzwave.scene import ZWaveScene
    from openzwave.controller import ZWaveController
    from openzwave.network import ZWaveNetwork
    from openzwave.option import ZWaveOption
    import time
    from louie import dispatcher, All

First thing to do is to defined some options for the manager :

.. code-block:: python

    options = ZWaveOption(device, config_path="../openzwave/config", user_path=".", cmd_line="")
    options.set_log_file("OZW_Log.log")
    options.set_append_log_file(False)
    options.set_console_output(False)
    options.set_save_log_level('Debug')
    options.set_logging(True)
    network = None

We also defined a network object, we will populate it later.

To use this options, you must lock them. No further modification could be done on them.

.. code-block:: python

    options.lock()

We can now create the network :

.. code-block:: python

    network = ZWaveNetwork(options, autostart=False)

The signals listeners
=====================

We will now create some connection to the louie dispatcher. We will then to 3
main signals, they will notify us about the state of the network :

.. code-block:: python

    dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
    dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
    dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

To do that we use 3 callback functions :

When the driver is ready, we simply print some options on the screen :

.. code-block:: python

    def louie_network_started(network):
        print("Hello from network : I'm started : homeid %0.8x - %d nodes were found." % (network.home_id, network.nodes_count))

When the driver fails, we reports the error to screen :

.. code-block:: python

    def louie_network_failed(network):
        print("Hello from network : can't load :(.")

This an important event. It means that all nodes have been queried on the network.
You can now use the network object pass in parameter to query nodes. To do that we connect
to some louie signals. It also sleep during 5 minutes. After that, the scripts
will continue and the network will be stopped.

.. code-block:: python

    def louie_network_ready(network):
        print("Hello from network : I'm ready : %d nodes were found." % network.nodes_count)
        print("Hello from network : my controller is : %s" % network.controller)
        dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
        dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

When a node is updated, added, removed, ...

.. code-block:: python

    def louie_node_update(network, node):
        print('Hello from node : %s.' % node)

When a value is updated, added, removed, ...

.. code-block:: python

    def louie_value_update(network, node, value):
        print('Hello from value : %s.' % value)

The start code
==============

We start the network

.. code-block:: python

    network.start()

And we wait for the network. You MUST NOT use the network objects before
network is ready.

.. code-block:: python

    for i in range(0,90):
        if network.state>=network.STATE_READY:
            print "***** Network is ready"
            break
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1.0)

We now change the name of the controller. You will have a notification.

.. code-block:: python

    network.controller.node.name = "Hello name"
    time.sleep(10.0)

Same when changing the location.

.. code-block:: python

    network.controller.node.location = "Hello location"
    time.sleep(120.0)

And we wait for 2 minutes. If you have sensors on your network, you will
see the value notifications on the screen. If you have switch or dimmers,
activate them manually, ...

Now stop the network and release objects.

.. code-block:: python

    network.stop()

That's all :)

Full source code is in examples/hello_world.py

To see a more functionnal example, look at ozwsh code.
