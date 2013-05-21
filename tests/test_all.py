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
#logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')

#Insert your build directory here (it depends of your python distribution)
#To get one, run the make_doc.sh command
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.6/dist-packages'))
sys.path.insert(0, os.path.abspath('build/tmp/usr/local/lib/python2.7/dist-packages'))
import libopenzwave
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from louie import dispatcher, All
import time
import unittest

class WaitTestCase(unittest.TestCase):

    def wait_for_queue(self):
        for i in range(0,60):
            if network.controller.send_queue_count <= 0:
                break
            else:
                time.sleep(0.5)

    def ctrl_message(self, state, message, network, controller):
        self.ctrl_command_result = state

    def node_update(self, network, node):
        self.node_result = node

    def setUp(self):
        self.max_delay = 30
        self.ctrl_command_result = None
        dispatcher.connect(self.ctrl_message, ZWaveController.SIGNAL_CONTROLLER)
        self.node_result = None
        dispatcher.connect(self.node_update, ZWaveNetwork.SIGNAL_NODE)

class NetworkTestCase(WaitTestCase):

    def test_000_network_awake(self):
        self.assertTrue(network.state>=network.STATE_AWAKED)
        self.assertTrue(type(network.home_id_str)==type(""))

    def test_010_network_ready(self):
        self.assertTrue(network.state>=network.STATE_READY)

    def test_100_network_test(self):
        self.wait_for_queue()
        network.test(5)

    def test_200_network_get_value_from_id_on_network(self):
        self.wait_for_queue()
        myval = 0
        for node in network.nodes:
            for cmd in network.nodes[node].command_classes:
                for val in network.nodes[node].get_values_for_command_class(cmd) :
                    myval = network.nodes[node].values[val]
                    self.assertTrue(network.get_value_from_id_on_network(myval.id_on_network)!=None)

    def test_201_network_get_value_from_id_on_network_bad(self):
        self.wait_for_queue()
        myval = "a_bad-id"
        self.assertTrue(network.get_value_from_id_on_network(myval)==None)

class ControllerTestCase(WaitTestCase):

    def test_010_controller(self):
        self.assertTrue(type(network.controller.name) == type(""))
        self.assertTrue(type(network.controller.ozw_library_version) == type(""))
        self.assertTrue(type(network.controller.python_library_version) == type(""))
        self.assertTrue(type(network.controller.library_description) == type(""))

    def test_020_controller_capabilities(self):
        self.assertTrue(type(network.controller.capabilities) == type(set()))

    def test_030_controller_send_sqeue(self):
        self.assertTrue(type(network.controller.send_queue_count) == type(0))
        self.assertTrue(network.controller.send_queue_count >= 0)

    def test_040_controller_stats(self):
        self.assertTrue(type(network.controller.stats) == type(dict()))

    def test_110_controller_soft_reset(self):
        self.wait_for_queue()
        time.sleep(5)
        network.controller.soft_reset()
        self.wait_for_queue()
        self.assertTrue(network.controller.node.refresh_info() == True)

    def test_310_controller_node(self):
        self.assertTrue(type(network.controller.node.node_id) == type(0))
        self.assertTrue(network.controller.node.node_id > 0)
        self.assertTrue(type(network.controller.node.version) == type(0))
        self.assertTrue(network.controller.node.version > 0)

    def test_320_controller_node_capabilities(self):
        self.assertTrue(type(network.controller.node.capabilities) == type(set()))

    def test_330_controller_node_neighbors(self):
        self.assertTrue(type(network.controller.node.neighbors) == type(set()))

    def test_340_controller_node_baud_rate(self):
        self.assertTrue(type(network.controller.node.max_baud_rate) == type(long()))
        self.assertTrue(network.controller.node.max_baud_rate > 0)

    def test_410_controller_node_product(self):
        self.assertTrue(type(network.controller.node.product_type) == type(""))
        self.assertTrue(type(network.controller.node.product_id) == type(""))

    def test_420_controller_node_name(self):
        name = "TestUnit name"
        network.controller.node.name = name
        self.assertTrue(network.controller.node.name == name)

    def test_430_controller_node_product_location(self):
        location = "TestUnit location"
        network.controller.node.location = location
        self.assertTrue(network.controller.node.location == location)

    def test_440_controller_node_product_name(self):
        name = "TestUnit product name"
        network.controller.node.product_name = name
        self.assertTrue(network.controller.node.product_name == name)

    def test_510_controller_node_group(self):
        self.assertTrue(network.controller.node.num_groups >= 0)
        self.assertTrue(type(network.controller.node.groups) == type(dict()))

    def test_610_controller_node_command_class(self):
        self.assertTrue(type(network.controller.node.command_classes) == type(set()))
        self.assertTrue(len(network.controller.node.command_classes) >= 0)

    def test_710_controller_node_manufacturer_name(self):
        self.assertTrue(type(network.controller.node.manufacturer_id) == type(""))
        name = "TestUnit manufacturer name"
        network.controller.node.manufacturer_name = name
        self.assertTrue(network.controller.node.manufacturer_name == name)

    def test_760_controller_stats_label(self):
        self.assertTrue(type(network.controller.get_stats_label('retries')) == type(""))

    def test_810_controller_node_values(self):
        self.assertTrue(type(network.controller.node.get_values()) == type(dict()))

    def test_820_controller_node_generic(self):
        self.assertTrue(type(network.controller.node.generic) == type(0))
        self.assertTrue(network.controller.node.generic > 0)
        self.assertTrue(type(network.controller.node.basic) == type(0))
        self.assertTrue(network.controller.node.basic > 0)
        self.assertTrue(type(network.controller.node.specific) == type(0))
        self.assertTrue(network.controller.node.specific >= 0)
        self.assertTrue(type(network.controller.node.security) == type(0))
        self.assertTrue(network.controller.node.security >= 0)

    def notest_910_controller_node_refresh(self):
        self.wait_for_queue()
        self.assertTrue(network.controller.node.refresh_info() == True)

class NodesTestCase(WaitTestCase):

    def test_000_nodes_count(self):
        self.assertTrue(type(network.nodes_count) == type(0))
        self.assertTrue(network.nodes_count>0)

    def test_100_nodes_test(self):
        self.wait_for_queue()
        for node in network.nodes:
            network.nodes[node].test(5)

class ValuesTestCase(WaitTestCase):

    def notest_000_values(self):
        self.wait_for_queue()
        for node in network.nodes:
            for cmd in network.nodes[node].command_classes:
                for val in network.nodes[node].get_values_for_command_class(cmd) :
                    self.wait_for_queue()
                    value = network.nodes[node].values[val]
                    self.assertTrue(type(value.label) == type(""))
                    self.assertTrue(type(value.help) == type(""))
                    self.assertTrue(type(value.max) == type(long()))
                    self.assertTrue(type(value.min) == type(long()))
                    self.assertTrue(type(value.units) == type(""))
                    self.assertTrue(type(value.id_on_network) == type(""))
                    self.assertTrue(value.genre in libopenzwave.PyGenres)
                    #self.assertTrue(type(value.data_as_string) == type(""))
                    self.assertTrue(value.type in libopenzwave.PyValueTypes)
                    self.assertTrue(value.is_polled in [True, False])
                    self.assertTrue(value.is_read_only in [True, False])
                    self.assertTrue(value.is_write_only in [True, False])
                    #self.assertTrue(value.refresh() in [True, False])
                    #time.sleep(1)

class SwitchesTestCase(WaitTestCase):

    def test_010_switches_state(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_switches() :
                ran = True
                self.assertTrue(network.nodes[node].get_switch_state(val) in [True, False])
        if not ran :
            self.skipTest("No Switch found")

    def test_110_switches_on_off(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_switches() :
                ran = True
                time.sleep(1)
                network.nodes[node].set_switch(val,True)
                self.wait_for_queue()
                time.sleep(1)
                if network.nodes[node].get_switch_state(val) == False :
                    time.sleep(5)
                self.assertTrue(network.nodes[node].get_switch_state(val) == True)
                network.nodes[node].set_switch(val,False)
                self.wait_for_queue()
                time.sleep(1)
                if network.nodes[node].get_switch_state(val) == True :
                    time.sleep(5)
                self.assertTrue(network.nodes[node].get_switch_state(val) == False)
        if not ran :
            self.skipTest("No Switch found")

class DimmersTestCase(WaitTestCase):
    def test_010_dimmers_level(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_dimmers() :
                ran = True
                self.assertTrue(network.nodes[node].get_dimmer_level(val) in range(0,256))
        if not ran :
            self.skipTest("No Dimmer found")

    def test_110_dimmers_on_off(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_dimmers() :
                ran = True
                level = 80
                network.nodes[node].set_dimmer(val,level)
                time.sleep(1)
                if network.nodes[node].get_dimmer_level(val) not in range(level-5,level+5):
                    time.sleep(5)
                self.assertTrue(network.nodes[node].get_dimmer_level(val) in range(level-5,level+5))
                network.nodes[node].set_dimmer(val,0)
                time.sleep(2)
                if network.nodes[node].get_dimmer_level(val) != 0:
                    time.sleep(5)
                self.assertTrue(network.nodes[node].get_dimmer_level(val) == 0)
        if not ran :
            self.skipTest("No Dimmer found")

class SensorsTestCase(WaitTestCase):

    def test_010_sensors_bool(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_sensors(type='Bool') :
                ran = True
                self.assertTrue(network.nodes[node].get_sensor_value(val) in [True, False])
        if not ran :
            self.skipTest("No Bool sensor found")

    def test_110_sensors_byte(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_sensors(type='Byte') :
                ran = True
                good = True
                try :
                    newval = int(network.nodes[node].get_sensor_value(val))
                except :
                    good = False
                self.assertTrue(good)
        if not ran :
            self.skipTest("No Byte sensor found")

    def test_210_sensors_short(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_sensors(type='Short') :
                ran = True
                good = True
                try :
                    newval = int(network.nodes[node].get_sensor_value(val))
                except :
                    good = False
                self.assertTrue(good)
        if not ran :
            self.skipTest("No Short sensor found")

    def test_310_sensors_int(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_sensors(type='Int') :
                ran = True
                good = True
                try :
                    newval = int(network.nodes[node].get_sensor_value(val))
                except :
                    good = False
                self.assertTrue(good)
        if not ran :
            self.skipTest("No Int sensor found")

    def test_410_sensors_decimal(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_sensors(type='Decimal') :
                ran = True
                good = True
                try :
                    newval = float(network.nodes[node].get_sensor_value(val))
                except :
                    good = False
                self.assertTrue(good)
        if not ran :
            self.skipTest("No Decimal sensor found")

class SwitchesAllTestCase(WaitTestCase):

    def test_010_switches_all_item(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_switches_all() :
                ran = True
                self.assertTrue(type(network.nodes[node].get_switch_all_item(val)) == type(""))
        if not ran :
            self.skipTest("No Switch_All found")

    def test_015_switches_all_set_item(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_switches_all() :
                self.wait_for_queue()
                ran = True
                old_value = network.nodes[node].get_switch_all_item(val)
                new_value = "Disabled"
                network.nodes[node].set_switch_all(val, new_value)
                time.sleep(1)
                self.wait_for_queue()
                self.assertTrue(network.nodes[node].get_switch_all_item(val) == new_value)
                network.nodes[node].set_switch_all(val, old_value)
                time.sleep(1)
        if not ran :
            self.skipTest("No Switch_All found")

    def test_020_switches_all_items(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_switches_all() :
                ran = True
                self.assertTrue(type(network.nodes[node].get_switch_all_items(val)) == type("") \
                  or type(network.nodes[node].get_switch_all_items(val)) == type(set()))
        if not ran :
            self.skipTest("No Switch_All found")

    def test_110_switches_all_on(self):
        self.wait_for_queue()
        ran = False
        network.switch_all(True)
        time.sleep(5)
        self.wait_for_queue()
        for node in network.nodes:
            for val in network.nodes[node].get_switches_all() :
                item = network.nodes[node].get_switch_all_item(val)
                self.wait_for_queue()
                if item == "On and Off Enabled" or item == "On Enabled":
                    ran = True
                    #print "Node/State : %s/%s" % (node,network.nodes[node].get_switch_all_state(val))
                    self.assertTrue(network.nodes[node].get_switch_all_state(val) == True)
        if not ran :
            self.skipTest("No Switch_All with 'On and Off Enabled' or 'On Enabled' found")

    def test_120_switches_all_off(self):
        self.wait_for_queue()
        ran = False
        network.switch_all(False)
        time.sleep(5)
        self.wait_for_queue()
        for node in network.nodes:
            for val in network.nodes[node].get_switches_all() :
                item = network.nodes[node].get_switch_all_item(val)
                self.wait_for_queue()
                if item == "On and Off Enabled" or item == "Off Enabled":
                    ran = True
                    #print "Node/State : %s/%s" % (node,network.nodes[node].get_switch_all_state(val))
                    self.assertTrue(network.nodes[node].get_switch_all_state(val) == False)
        if not ran :
            self.skipTest("No Switch_All with 'On and Off Enabled' or 'Off Enabled' found")

class ProtectionTestCase(WaitTestCase):

    def test_010_protection_item(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_protections() :
                ran = True
                self.assertTrue(type(network.nodes[node].get_protection_item(val)) == type(""))
        if not ran :
            self.skipTest("No Protection found")

    def test_020_protection_set_item_no_operation(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_protections() :
                self.wait_for_queue()
                ran = True
                old_value = network.nodes[node].get_protection_item(val)
                new_value = "No Operation Possible"
                network.nodes[node].set_protection(val, new_value)
                time.sleep(1)
                self.wait_for_queue()
                self.assertTrue(network.nodes[node].get_protection_item(val) == new_value)
                network.nodes[node].set_protection(val, old_value)
                time.sleep(1)
        if not ran :
            self.skipTest("No Protection found")

    def test_030_protection_set_item_unprotected(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_protections() :
                self.wait_for_queue()
                ran = True
                old_value = network.nodes[node].get_protection_item(val)
                new_value = "Unprotected"
                network.nodes[node].set_protection(val, new_value)
                time.sleep(1)
                self.wait_for_queue()
                self.assertTrue(network.nodes[node].get_protection_item(val) == new_value)
                network.nodes[node].set_protection(val, old_value)
                time.sleep(1)
        if not ran :
            self.skipTest("No Protection found")

    def test_050_protection_items(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_protections() :
                ran = True
                self.assertTrue(type(network.nodes[node].get_protection_items(val)) == type("") \
                  or type(network.nodes[node].get_protection_items(val)) == type(set()))
        if not ran :
            self.skipTest("No Protection found")

class BatteryTestCase(WaitTestCase):

    def test_010_battery_item(self):
        self.wait_for_queue()
        ran = False
        for node in network.nodes:
            for val in network.nodes[node].get_battery_levels() :
                ran = True
                self.assertTrue(type(network.nodes[node].get_battery_level(val)) == type(0))
        if not ran :
            self.skipTest("No battery found")

class SceneTestCase(WaitTestCase):

    def test_005_scene_count(self):
        self.wait_for_queue()
        global count
        count = network.scenes_count
        self.assertTrue( count >= 0)

    def test_010_add_scene(self):
        self.wait_for_queue()
        global sceneid
        sceneid = network.create_scene("TestUnit Scene")
        self.assertTrue( sceneid > 0)

    def test_110_add_switches_to_scene(self):
        self.wait_for_queue()
        global sceneid
        scene = network.get_scenes()[sceneid]
        for node in network.nodes:
            for val in network.nodes[node].get_switches() :
                ret = scene.add_value(val, True)
                self.assertTrue(ret == True)

    def test_120_add_dimmers_to_scene(self):
        self.wait_for_queue()
        global sceneid
        global level
        scene = network.get_scenes()[sceneid]
        for node in network.nodes:
            for val in network.nodes[node].get_dimmers() :
                ret = scene.add_value(val, level)
                self.assertTrue(ret == True)

    def test_210_scene_exist(self):
        self.wait_for_queue()
        global sceneid
        self.assertTrue( network.scene_exists(sceneid) == True)

    def test_310_scene_activate(self):
        self.wait_for_queue()
        global sceneid
        scene = network.get_scenes()[sceneid]
        self.assertTrue( scene.activate() == True)

    def test_410_scene_count(self):
        self.wait_for_queue()
        global count
        self.assertTrue( network.scenes_count == count + 1)

#    def test_510_drop_scene(self):
#        self.wait_for_queue()
#        global sceneid
#        ret = network.remove_scene(sceneid)
#        self.assertTrue( ret == True)

    def test_610_add_scene(self):
        self.wait_for_queue()
        global sceneid
        sceneid = network.create_scene("TestUnit Scene")
        self.assertTrue( sceneid > 0)

    def test_710_add_switches_to_scene(self):
        self.wait_for_queue()
        global sceneid
        scene = network.get_scenes()[sceneid]
        for node in network.nodes:
            for val in network.nodes[node].get_switches() :
                ret = scene.add_value(val, False)
                self.assertTrue(ret == True)

    def test_720_add_dimmers_to_scene(self):
        self.wait_for_queue()
        global sceneid
        global level
        scene = network.get_scenes()[sceneid]
        for node in network.nodes:
            for val in network.nodes[node].get_dimmers() :
                ret = scene.add_value(val, 0)
                self.assertTrue(ret == True)

    def test_810_scene_activate(self):
        self.wait_for_queue()
        global sceneid
        scene = network.get_scenes()[sceneid]
        self.assertTrue( scene.activate() == True)

#    def test_820_scene_count(self):
#        self.wait_for_queue()
#        global count
#        self.assertTrue( network.scenes_count == count + 1)

#    def test_830_drop_scene(self):
#        self.wait_for_queue()
#        global sceneid
#        ret = network.remove_scene(sceneid)
#        self.assertTrue( ret == True)

#    def test_910_scene_count(self):
#        self.wait_for_queue()
#        global count
#        self.assertTrue( network.scenes_count == count)

class ControllerCommandTestCase(WaitTestCase):

    def test_010_command_send_node_information_nodeid_2(self):
        ret = network.controller.begin_command_send_node_information(2)
        self.assertTrue(ret)
        current = None
        for i in range(0,self.max_delay):
            #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                current = self.ctrl_command_result
                #print(current)
                self.ctrl_command_result = None
                break
            else:
                time.sleep(1.0)
        self.assertTrue(current == "Completed")

    def test_020_command_send_node_information_nodeid_1(self):
        ret = network.controller.begin_command_send_node_information(1)
        self.assertTrue(ret)
        current = None
        for i in range(0,self.max_delay):
            #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                current = self.ctrl_command_result
                #print(current)
                self.ctrl_command_result = None
                break
            else:
                time.sleep(1.0)
        self.assertTrue(current == "Completed")

    def test_110_command_request_network_update(self):
        ret = network.controller.begin_command_request_network_update()
        self.assertTrue(ret)
        current = None
        for i in range(0,self.max_delay):
            #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                current = self.ctrl_command_result
                #print(current)
                self.ctrl_command_result = None
                break
            else:
                time.sleep(1.0)
        self.assertTrue(current == "Completed")

    def test_210_command_request_node_neigbhor_update_node(self):
        ret = network.controller.begin_command_request_node_neigbhor_update(2)
        self.assertTrue(ret)
        current = None
        for i in range(0,self.max_delay):
            #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                current = self.ctrl_command_result
                print(current)
                self.ctrl_command_result = None
                break
            else:
                time.sleep(1.0)
        self.assertTrue(current == "Completed")

    def test_220_command_request_node_neigbhor_update_controller(self):
        ret = network.controller.begin_command_request_node_neigbhor_update(1)
        self.assertTrue(ret)
        current = None
        for i in range(0,self.max_delay):
            #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
            if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
                current = self.ctrl_command_result
                #print(current)
                self.ctrl_command_result = None
                break
            else:
                time.sleep(1.0)
        self.assertTrue(current == "Failed")

#    def test_910_command_command_replication_send(self):
#        ret = network.controller.begin_command_replication_send(1)
#        self.assertTrue(ret)
#        current = None
#        for i in range(0,self.max_delay):
#            #print("self.ctrl_command_result = %s" % self.ctrl_command_result)
#            if self.ctrl_command_result != None and self.ctrl_command_result != "InProgress":
#                current = self.ctrl_command_result
#                print(current)
#                self.ctrl_command_result = None
#                break
#            else:
#                time.sleep(1.0)
#        self.assertTrue(current == "Completed")

if __name__ == '__main__':
    device="/dev/zwave-aeon-s2"
    log="Debug"

    scenid = 0
    level = 70
    count = 0

    for arg in sys.argv:
        if arg.startswith("--device"):
            temp,device = arg.split("=")
        elif arg.startswith("--log"):
            temp,log = arg.split("=")
        elif arg.startswith("--help"):
            print("help : ")
            print("  --device=/dev/yourdevice ")
            print("  --log=Info|Debug")

    print "----------------------------------------------------------------------"
    print "Waiting for network : "
    options = ZWaveOption(device, \
      config_path="../openzwave/config", \
      user_path=".", cmd_line="")
    options.set_log_file("OZW_Log.log")
    options.set_append_log_file(False)
    options.set_console_output(False)
    options.set_save_log_level("Debug")
    options.set_logging(True)
    options.lock()
    network = ZWaveNetwork(options, log=None)
    for i in range(0,300):
        if network.state>=network.STATE_AWAKED:
            break
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1.0)
    print ""
    print "Awake"
    ready = False
    for i in range(0,300):
        if network.state>=network.STATE_READY:
            ready = True
            break
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1.0)
    if ready :
        print "Ready"
    else :
        print "Network is not ready but continue anyway"
    print "----------------------------------------------------------------------"
    print "Run tests : "

    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(NetworkTestCase)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ControllerTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(NodesTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ValuesTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SwitchesTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DimmersTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SensorsTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SwitchesAllTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ProtectionTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(BatteryTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SceneTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ControllerCommandTestCase))
    unittest.TextTestRunner(verbosity=2).run(suite)

    print "----------------------------------------------------------------------"

    network.stop()
