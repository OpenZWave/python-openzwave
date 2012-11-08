#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
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

#Insert your build directory here (it depends of your python distribution)
#To get one, run the make_doc.sh command
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.7/dist-packages'))
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time

device="/dev/zwave-aeon-s2"
log="Debug"

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
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
#options.set_save_log_level('Info')
options.set_logging(True)
options.lock()

#Create a network object
network = ZWaveNetwork(options, log=None)

print "------------------------------------------------------------"
print "Waiting for driver : "
print "------------------------------------------------------------"
for i in range(0,20):
    if network.state>=network.STATE_INITIALISED:
        print " done"
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if network.state<network.STATE_INITIALISED:
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
        #sys.stdout.write(network.state_str)
        #sys.stdout.write("(")
        #sys.stdout.write(str(network.nodes_count))
        #sys.stdout.write(")")
        #sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)
if not network.is_ready:
    print "."
    print "Can't start network! Look at the logs in OZW_Log.log"
    quit(2)
print "------------------------------------------------------------"
print "Controller capabilities : %s" % network.controller.capabilities
print "Controller node capabilities : %s" % network.controller.node.capabilities
print "Nodes in network : %s" % network.nodes_count
print "Driver statistics : %s" % network.controller.stats
print "------------------------------------------------------------"
for node in network.nodes:
    print
    print "------------------------------------------------------------"
    print "%s - Name : %s" % (network.nodes[node].node_id,network.nodes[node].name)
    print "%s - Manufacturer name / id : %s / %s" % (network.nodes[node].node_id,network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id)
    print "%s - Product name / id / type : %s / %s / %s" % (network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type)
    print "%s - Version : %s" % (network.nodes[node].node_id, network.nodes[node].version)
    print "%s - Command classes : %s" % (network.nodes[node].node_id,network.nodes[node].command_classes_as_string)
    print "%s - Capabilities : %s" % (network.nodes[node].node_id,network.nodes[node].capabilities)
    print "%s - Neigbors : %s" % (network.nodes[node].node_id,network.nodes[node].neighbors)
    groups = {}
    for grp in network.nodes[node].groups :
        groups[network.nodes[node].groups[grp].index] = {'label':network.nodes[node].groups[grp].label, 'associations':network.nodes[node].groups[grp].associations}
    print "%s - Groups : %s" % (network.nodes[node].node_id, groups)
    values = {}
    for val in network.nodes[node].values :
        values[network.nodes[node].values[val].object_id] = {
            'label':network.nodes[node].values[val].label,
            'help':network.nodes[node].values[val].help,
            'command_class':network.nodes[node].values[val].command_class,
            'max':network.nodes[node].values[val].max,
            'min':network.nodes[node].values[val].min,
            'units':network.nodes[node].values[val].units,
            'data':network.nodes[node].values[val].data_as_string,
            'ispolled':network.nodes[node].values[val].is_polled
            }
    #print "%s - Values : %s" % (network.nodes[node].node_id, values)
    #print "------------------------------------------------------------"
    for cmd in network.nodes[node].command_classes:
        print "   ---------   "
        #print "cmd = ",cmd
        values = {}
        for val in network.nodes[node].get_values_for_command_class(cmd) :
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'help':network.nodes[node].values[val].help,
                'max':network.nodes[node].values[val].max,
                'min':network.nodes[node].values[val].min,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data,
                'data_str':network.nodes[node].values[val].data_as_string,
                'genre':network.nodes[node].values[val].genre,
                'type':network.nodes[node].values[val].type,
                'ispolled':network.nodes[node].values[val].is_polled,
                'readonly':network.nodes[node].values[val].is_read_only,
                'writeonly':network.nodes[node].values[val].is_write_only,
                }
        print "%s - Values for command class : %s : %s" % (network.nodes[node].node_id,
                                    network.nodes[node].get_command_class_as_string(cmd),
                                    values)
    print "------------------------------------------------------------"
print
print "------------------------------------------------------------"
print "Driver statistics : %s" % network.controller.stats
print "------------------------------------------------------------"
print
print "------------------------------------------------------------"
print "Try to autodetect nodes on the network"
print "------------------------------------------------------------"
print "Nodes in network : %s" % network.nodes_count
print "------------------------------------------------------------"
print "Retrieve switches on the network"
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  state: %s" % (network.nodes[node].get_switch_state(val)))
print "------------------------------------------------------------"
print "Retrieve dimmers on the network"
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_dimmers() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  level: %s" % (network.nodes[node].get_dimmer_level(val)))
print "------------------------------------------------------------"
print "Retrieve sensors on the network"
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_sensors() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  value: %s %s" % (network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units))
print "------------------------------------------------------------"
print "Retrieve switches all compatibles devices on the network    "
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches_all() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  value / items: %s / %s" % (network.nodes[node].get_switch_all_item(val), network.nodes[node].get_switch_all_items(val)))
print "------------------------------------------------------------"
print "Retrieve protection compatibles devices on the network    "
print "------------------------------------------------------------"
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_protections() :
        print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
        print("  value / items: %s / %s" % (network.nodes[node].get_protection_item(val), network.nodes[node].get_protection_items(val)))
print "------------------------------------------------------------"

#print
#print "------------------------------------------------------------"
#print "Activate the switches on the network"
#print "Nodes in network : %s" % network.nodes_count
#print "------------------------------------------------------------"
#for node in network.nodes:
#    for val in network.nodes[node].get_switches() :
#        print("Activate switch %s on node %s" % \
#                (network.nodes[node].values[val].label,node))
#        network.nodes[node].set_switch(val,True)
#        print("Sleep 10 seconds")
#        time.sleep(10.0)
#        print("Dectivate switch %s on node %s" % \
#                (network.nodes[node].values[val].label,node))
#        network.nodes[node].set_switch(val,False)
#print "%s" % ('Done')
#print "------------------------------------------------------------"

print
print "------------------------------------------------------------"
print "Driver statistics : %s" % network.controller.stats
print "------------------------------------------------------------"

print
print "------------------------------------------------------------"
print "Stop network"
print "------------------------------------------------------------"
network.stop()
