#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

License : GPL(v3)

**python-openzwave** is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

**python-openzwave** is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with python-openzwave. If not, see http://www.gnu.org/licenses.

"""

import logging
import sys, os

#logging.getLogger('openzwave').addHandler(logging.NullHandler())
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')

import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time
from louie import dispatcher, All

device="/dev/ttyUSB0"
log="None"
sniff=300.0

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--sniff"):
        temp,sniff = arg.split("=")
        sniff = float(sniff)
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

#Define some manager options
options = ZWaveOption(device, \
  config_path="../openzwave/config", \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
options.set_logging(True)
options.lock()

def louie_network_started(network):
    print("Hello from network : I'm started : homeid %0.8x - %d nodes were found." % \
        (network.home_id, network.nodes_count))

def louie_network_failed(network):
    print("Hello from network : can't load :(.")

def louie_network_ready(network):
    print("Hello from network : I'm ready : %d nodes were found." % network.nodes_count)
    print("Hello from network : my controller is : %s" % network.controller)
    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

def louie_node_update(network, node):
    print('Hello from node : %s.' % node)

def louie_value_update(network, node, value):
    print('Hello from value : %s.' % value)

#Create a network object
network = ZWaveNetwork(options, autostart=False)

#We connect to the louie dispatcher
dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)

network.start()

#We wait for the network.
print "***** Waiting for network to become ready : "
for i in range(0,90):
    if network.state>=network.STATE_READY:
        print "***** Network is ready"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)

time.sleep(5.0)

#We update the name of the controller
print("Update controller name")
network.controller.node.name = "Hello name"

time.sleep(5.0)

#We update the location of the controller
print("Update controller location")
network.controller.node.location = "Hello location"

time.sleep(5.0)

for node in network.nodes:
    for val in network.nodes[node].get_switches() :
        print("Activate switch")
        network.nodes[node].set_switch(val,True)
        time.sleep(10.0)
        print("Deactivate switch")
        network.nodes[node].set_switch(val,False)
    #We only activate the first switch
    #exit

time.sleep(5.0)

for node in network.nodes:
    for val in network.nodes[node].get_dimmers() :
        print("Activate dimmer : %s" % network.nodes[node])
        network.nodes[node].set_dimmer(val,80)
        time.sleep(10.0)
        print("Deactivate dimmer")
        network.nodes[node].set_dimmer(val,0)
        time.sleep(10.0)
        print("Deactivate dimmer")
        network.nodes[node].set_dimmer(val,0)
    #We only activate the first dimmer
    #exit

time.sleep(10.0)

network.stop()
