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

print("------------------------------------------------------------")
print("Try to evaluate memory use                                  ")
print("------------------------------------------------------------")
print("------------------------------------------------------------")
print("Waiting for driver :                                        ")
print("------------------------------------------------------------")
for i in range(0,20):
    if network.state>=network.STATE_STARTED:
        print(" done")
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if network.state<network.STATE_STARTED:
    print(".")
    print("Can't initialise driver! Look at the logs in OZW_Log.log")
    quit(1)
print("------------------------------------------------------------")
print("Use openzwave library : {}".format(network.controller.ozw_library_version))
print("Use python library : {}".format(network.controller.python_library_version))
print("Use ZWave library : {}".format(network.controller.library_description))
print("Network home id : {}".format(network.home_id_str))
print("Controller node id : {}".format(network.controller.node.node_id))
print("Controller node version : {}".format(network.controller.node.version))
print("Nodes in network : {}".format(network.nodes_count))
print("------------------------------------------------------------")
print("Waiting for network to become ready : ")
print("------------------------------------------------------------")
for i in range(0,90):
    if network.state>=network.STATE_READY:
        print(" done")
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if not network.is_ready:
    print(".")
    print("Can't start network! Look at the logs in OZW_Log.log")
    quit(2)
print("------------------------------------------------------------")
print("Controller capabilities : {}".format(network.controller.capabilities))
print("Controller node capabilities : {}".format(network.controller.node.capabilities))
print("------------------------------------------------------------")
print("Driver statistics : {}".format(network.controller.stats))
print("------------------------------------------------------------")
print("Nodes in network : {}".format(network.nodes_count))
print("------------------------------------------------------------")
print("Memory use : ")
print("------------------------------------------------------------")
print("Memory use for network {} : ".format(network.home_id_str))
print("  asizeof   : {} bytes".format(asizeof(network)))
print("  basicsize : {} bytes".format(basicsize(network)))
print("  itemsize  : {} bytes".format(itemsize(network)))
print("  flatsize  : {} bytes".format(flatsize(network)))
print("------------------------------------------------------------")
manager = network.manager
print("Memory use for manager : ")
print("  asizeof   : {} bytes".format(asizeof(manager)))
print("  basicsize : {} bytes".format(basicsize(manager)))
print("  itemsize  : {} bytes".format(itemsize(manager)))
print("  flatsize  : {} bytes".format(flatsize(manager)))
print("------------------------------------------------------------")
print("Memory use for controller : ")
print("  asizeof   : {} bytes".format(asizeof(network.controller)))
print("  basicsize : {} bytes".format(basicsize(network.controller)))
print("  itemsize  : {} bytes".format(itemsize(network.controller)))
print("  flatsize  : {} bytes".format(flatsize(network.controller)))
print("------------------------------------------------------------")
print("Memory use for {} scenes (scenes are generated on call) : ".format(network.scenes_count))
scenes = network.get_scenes()
print("  asizeof   : {} bytes".format(asizeof(scenes)))
print("  basicsize : {} bytes".format(basicsize(scenes)))
print("  itemsize  : {} bytes".format(itemsize(scenes)))
print("  flatsize  : {} bytes".format(flatsize(scenes)))
print("------------------------------------------------------------")
print("Parsing scenes")
for scene in scenes:
    print("  Memory use for scene {}: ".format(scene))
    print("    asizeof   : {} bytes".format(asizeof(scenes[scene])))
    print("    basicsize : {} bytes".format(basicsize(scenes[scene])))
    print("    itemsize  : {} bytes".format(itemsize(scenes[scene])))
    print("    flatsize  : {} bytes".format(flatsize(scenes[scene])))
print("------------------------------------------------------------")
print("Memory use for {} nodes : ".format(network.nodes_count))
nodes = network.nodes
print("  asizeof   : {} bytes".format(asizeof(nodes)))
print("  basicsize : {} bytes".format(basicsize(nodes)))
print("  itemsize  : {} bytes".format(itemsize(nodes)))
print("  flatsize  : {} bytes".format(flatsize(nodes)))
print("------------------------------------------------------------")
print("Parsing nodes")
for node in nodes:
    print("  Memory use for node {}: ".format(node))
    print("    asizeof   : {} bytes".format(asizeof(nodes[node])))
    print("    basicsize : {} bytes".format(basicsize(nodes[node])))
    print("    itemsize  : {} bytes".format(itemsize(nodes[node])))
    print("    flatsize  : {} bytes".format(flatsize(nodes[node])))
    for value in nodes[node].values:
        print("    Memory use for value {} : ".format(value))
        print("      asizeof   : {} bytes".format(asizeof(nodes[node].values[value])))
        print("      basicsize : {} bytes".format(basicsize(nodes[node].values[value])))
        print("      itemsize  : {} bytes".format(itemsize(nodes[node].values[value])))
        print("      flatsize  : {} bytes".format(flatsize(nodes[node].values[value])))
print("------------------------------------------------------------")
print("")
print("------------------------------------------------------------")
print("Stop network")
print("------------------------------------------------------------")
network.stop()
