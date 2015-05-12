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
from pympler.asizeof import asizeof, flatsize, itemsize, basicsize

device="/dev/ttyUSB0"
log="Info"

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    if arg.startswith("--help"):
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
#options.set_save_log_level('Debug')
options.set_save_log_level(log)
options.set_logging(True)
options.lock()

#Create a network object
network = ZWaveNetwork(options, log=None)

print "------------------------------------------------------------"
print "Try to evaluate memory use                                  "
print "------------------------------------------------------------"
print "------------------------------------------------------------"
print "Waiting for driver :                                        "
print "------------------------------------------------------------"
for i in range(0,20):
    if network.state>=network.STATE_STARTED:
        print " done"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if network.state<network.STATE_STARTED:
    print "."
    print "Can't initialise driver! Look at the logs in OZW_Log.log"
    quit(1)
print "------------------------------------------------------------"
print "Use openzwave library : %s" % network.controller.ozw_library_version
print "Use python library : %s" % network.controller.python_library_version
print "Use ZWave library : %s" % network.controller.library_description
print "Network home id : %s" % network.home_id_str
print "Controller node id : %s" % network.controller.node.node_id
print "Controller node version : %s" % (network.controller.node.version)
print "Nodes in network : %s" % network.nodes_count
print "------------------------------------------------------------"
print "Waiting for network to become ready : "
print "------------------------------------------------------------"
for i in range(0,90):
    if network.state>=network.STATE_READY:
        print " done"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if not network.is_ready:
    print "."
    print "Can't start network! Look at the logs in OZW_Log.log"
    quit(2)
print "------------------------------------------------------------"
print "Controller capabilities : %s" % network.controller.capabilities
print "Controller node capabilities : %s" % network.controller.node.capabilities
print "------------------------------------------------------------"
print "Driver statistics : %s" % network.controller.stats
print "------------------------------------------------------------"
print "Nodes in network : %s" % network.nodes_count
print "------------------------------------------------------------"
print "Memory use : "
print "------------------------------------------------------------"
print "Memory use for network %s : " %(network.home_id_str)
print "  asizeof   : %s bytes" %(asizeof(network))
print "  basicsize : %s bytes" %(basicsize(network))
print "  itemsize  : %s bytes" %(itemsize(network))
print "  flatsize  : %s bytes" %(flatsize(network))
print "------------------------------------------------------------"
manager = network.manager
print "Memory use for manager : "
print "  asizeof   : %s bytes" %(asizeof(manager))
print "  basicsize : %s bytes" %(basicsize(manager))
print "  itemsize  : %s bytes" %(itemsize(manager))
print "  flatsize  : %s bytes" %(flatsize(manager))
print "------------------------------------------------------------"
print "Memory use for controller : "
print "  asizeof   : %s bytes" %(asizeof(network.controller))
print "  basicsize : %s bytes" %(basicsize(network.controller))
print "  itemsize  : %s bytes" %(itemsize(network.controller))
print "  flatsize  : %s bytes" %(flatsize(network.controller))
print "------------------------------------------------------------"
print "Memory use for %s scenes (scenes are generated on call) : " %(network.scenes_count)
scenes = network.get_scenes()
print "  asizeof   : %s bytes" %(asizeof(scenes))
print "  basicsize : %s bytes" %(basicsize(scenes))
print "  itemsize  : %s bytes" %(itemsize(scenes))
print "  flatsize  : %s bytes" %(flatsize(scenes))
print "------------------------------------------------------------"
print "Parsing scenes"
for scene in scenes:
    print "  Memory use for scene %s: " %(scene)
    print "    asizeof   : %s bytes" %(asizeof(scenes[scene]))
    print "    basicsize : %s bytes" %(basicsize(scenes[scene]))
    print "    itemsize  : %s bytes" %(itemsize(scenes[scene]))
    print "    flatsize  : %s bytes" %(flatsize(scenes[scene]))
print "------------------------------------------------------------"
print "Memory use for %s nodes : " %(network.nodes_count)
nodes = network.nodes
print "  asizeof   : %s bytes" %(asizeof(nodes))
print "  basicsize : %s bytes" %(basicsize(nodes))
print "  itemsize  : %s bytes" %(itemsize(nodes))
print "  flatsize  : %s bytes" %(flatsize(nodes))
print "------------------------------------------------------------"
print "Parsing nodes"
for node in nodes:
    print "  Memory use for node %s: " %(node)
    print "    asizeof   : %s bytes" %(asizeof(nodes[node]))
    print "    basicsize : %s bytes" %(basicsize(nodes[node]))
    print "    itemsize  : %s bytes" %(itemsize(nodes[node]))
    print "    flatsize  : %s bytes" %(flatsize(nodes[node]))
    for value in nodes[node].values:
        print "    Memory use for value %s : " %(value)
        print "      asizeof   : %s bytes" %(asizeof(nodes[node].values[value]))
        print "      basicsize : %s bytes" %(basicsize(nodes[node].values[value]))
        print "      itemsize  : %s bytes" %(itemsize(nodes[node].values[value]))
        print "      flatsize  : %s bytes" %(flatsize(nodes[node].values[value]))
print "------------------------------------------------------------"
print
print "------------------------------------------------------------"
print "Stop network"
print "------------------------------------------------------------"
network.stop()
