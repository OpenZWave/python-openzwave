# -*- coding: utf-8 -*-
"""
.. module:: openzwave.command

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
import libopenzwave
from collections import namedtuple
import thread
import time
import logging
from openzwave.object import ZWaveException, ZWaveCommandClassException
from openzwave.object import ZWaveObject, NullLoggingHandler, ZWaveNodeInterface
from openzwave.group import ZWaveGroup

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveNodeBasic(ZWaveNodeInterface):
    '''
    Represents an interface to BasicCommands
    I known it's not necessary as they can be included in the node directly.
    But it's a good starting point.

    What I want to do is provide an automatic mapping system hidding
    the mapping classes.

    First example, the battery level, it's not a basic command but don't care.
    Its command class is 0x80.

    A user should write
    if self.handle_command_class(class_id):
        ret=commandclass(...)

    The classic way to do it is a classique method of registering. But

    Another way : using heritage multiple

    ZWaveNode(ZWaveObject, ZWaveNodeBasic, ....)
    The interface will implement methods
    command_class_0x80(paramm1,param2,...)
    That's the first thing to do
    We also can define a property wtih a fiendly name

    handle_command_class will do the rest

    Another way to do it :
    A node can manage actuators (switch, dimmer, ...)
    and sensors (temperature, consommation, temperature)

    So we need a kind of mechanism to retrive commands in a user friendly way
    Same for sensors.

    A good use caser is the AN158 Plug-in Meter Appliance Module
    We will study the following command classes :
    'COMMAND_CLASS_SWITCH_ALL', 'COMMAND_CLASS_SWITCH_BINARY',
    'COMMAND_CLASS_METER',

    the associated values are :

    COMMAND_CLASS_SWITCH_ALL : {
        72057594101481476L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': '',
            'data': 'On and Off Enabled',
            'min': 0L,
            'writeonly': False,
            'label': 'Switch All',
            'readonly': False,
            'data_str': 'On and Off Enabled',
            'type': 'List'}
    }

    COMMAND_CLASS_SWITCH_BINARY : {
        72057594093060096L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': '',
            'data': False,
            'min': 0L,
            'writeonly': False,
            'label': 'Switch',
            'readonly': False,
            'data_str': False,
            'type': 'Bool'}
    }

    COMMAND_CLASS_METER : {
        72057594093273600L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': '',
            'data': False,
            'min': 0L,
            'writeonly': False,
            'label': 'Exporting',
            'readonly': True,
            'data_str': False,
            'type': 'Bool'},
        72057594101662232L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': '',
            'data': 'False',
            'min': 0L,
            'writeonly': True,
            'label': 'Reset',
            'readonly': False,
            'data_str': 'False',
            'type': 'Button'},
        72057594093273090L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': 'kWh',
            'data': 0.0,
            'min': 0L,
            'writeonly': False,
            'label': 'Energy',
            'readonly': True,
            'data_str': 0.0,
            'type': 'Decimal'},
        72057594093273218L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': 'W',
            'data': 0.0,
            'min': 0L,
            'writeonly': False,
            'label': 'Power',
            'readonly': True,
            'data_str': 0.0,
            'type': 'Decimal'}
    }

    Another example from an homepro dimmer (not congifured in openzwave):
    COMMAND_CLASS_SWITCH_MULTILEVEL : {
        72057594109853736L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': '',
            'data': 'False',
            'min': 0L,
            'writeonly': True,
            'label': 'Dim',
            'readonly': False,
            'data_str': 'False',
            'type': 'Button'},
        72057594109853697L: {
            'help': '',
            'max': 255L,
            'ispolled': False,
            'units': '',
            'data': 69,
            'min': 0L,
            'writeonly': False,
            'label': 'Level',
            'readonly': False,
            'data_str': 69,
            'type': 'Byte'},
        72057594118242369L: {
            'help': '',
            'max': 255L,
            'ispolled': False,
            'units': '',
            'data': 0,
            'min': 0L,
            'writeonly': False,
            'label': 'Start Level',
            'readonly': False,
            'data_str': 0,
            'type': 'Byte'},
        72057594109853720L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': '',
            'data': 'False',
            'min': 0L,
            'writeonly': True,
            'label': 'Bright',
            'readonly': False,
            'data_str': 'False',
            'type': 'Button'},
        72057594118242352L: {
            'help': '',
            'max': 0L,
            'ispolled': False,
            'units': '',
            'data': False,
            'min': 0L,
            'writeonly': False,
            'label': 'Ignore Start Level',
            'readonly': False,
            'data_str': False,
            'type': 'Bool'}
    }

    What about the conclusion :

        The COMMAND_CLASS_SWITCH_ALL is defined with the same label and
        use a list as parameter. This should be a configuration parameter.
        Don't know what to do for this command class

        The COMMAND_CLASS_SWITCH_BINARY use a bool as parameter while
        COMMAND_CLASS_SWITCH_MULTILEVEL use 2 buttons : Dim and Bright.
        Dim and Bright must be done in 2 steps : set the level and activate
        the button.

        So we must add one or more lines in the actuators :

        Switch : {setter:self.set_command_class_0xYZ(valueId, new), getter:}
        We must find a way to access the value directly

        Bright
        Dim

        So for the COMMAND_CLASS_SWITCH_BINARY we must define a function called
        Switch (=the label of the value). What happen if we have 2 switches
        on the node : 2 values I suppose.

        COMMAND_CLASS_SWITCH_MULTILEVEL uses 2 commands : 4 when 2 dimmers on the
        done ? Don't know but it can.

        COMMAND_CLASS_METER export many values : 2 of them sends a decimal
        and are readonly. They also have a Unit defined ans values are readonly

        COMMAND_CLASS_METER are used for sensors only. So we would map
        every values entries as defined before

        Programming :
        get_switches : retrieve the list of switches on the node
        is_switch (label) : says if the value with label=label is a switch
        get_switch (label) : retrive the value where label=label
    '''

    def __init__(self):
        '''
        Initialize zwave node

        :param node_id: ID of the node
        :type node_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        '''
        self._commands = dict()
        self._sensors = dict()
        logging.debug("Create object interface for Basic (node_id:%s)" % (self.node_id))
        ZWaveNodeInterface.__init__(self)

    @property
    def battery_level(self):
        """
        The battery level of this node.
        """
        return self.command_class_0x80()

    def command_class_0x80(self):
        """
        The command 0x80 (COMMAND_CLASS_BATTERY) level of this node.
        Todo
        """
        values = self.get_values_for_command_class(0x80)  # COMMAND_CLASS_BATTERY
        if values:
            for value in values:
                vdic = value.data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return -1

class ZWaveNodeSwitch(ZWaveNodeInterface):
    '''
    Represents an interface to Switch Commands

    '''

    def __init__(self):
        '''
        Initialize zwave interface

        :param node_id: ID of the node
        :type node_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        '''
        logging.debug("Create object interface for Switch (node_id:%s)" % (self.node_id))
        ZWaveNodeInterface.__init__(self)

    def get_switches(self):
        """
        The command 0x25 (COMMAND_CLASS_SWITCH_BINARY) of this node.
        Retrieve the list of values to consider as switches.
        Filter rules are :

            command_class = 0x25
            genre = "User"
            type = "Bool"
            readonly = False
            writeonly = False

        :param value: True or False
        :type value: bool

        """
        return self.get_values(class_id=0x25, genre='User', \
        type='Bool', readonly=False, writeonly=False)

    def set_switch(self, value_id, value):
        """
        The command 0x25 (COMMAND_CLASS_SWITCH_BINARY) of this node.
        Set switch to value (using value value_id).

        :param value: True or False
        :type value: bool

        """
        print value_id
        if value_id in self.get_switches():
            print "Ok"
            self.values[value_id].data = value
            return True
        return False


    @property
    def level(self):
        """
        The level of the node.
        Todo
        """
        return self.command_class_0x26()

    def command_class_0x26(self):
        """
        The command 0x26 (COMMAND_CLASS_SWITCH_MULTILEVEL) level of this node.
        Todo
        """
        values = self.get_values_for_command_class(0x26)  # COMMAND_CLASS_SWITCH_MULTILEVEL
        if values:
            for value in values:
                vdic = value.data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Byte' and vdic.has_key('value'):
                    return int(vdic['value'])
        return 0

class ZWaveNodeSensor(ZWaveNodeInterface):
    '''
    Represents an interface to Sensor Commands

    '''

    def __init__(self):
        '''
        Initialize zwave interface

        '''
        logging.debug("Create object interface for Sensor (node_id:%s)" % (self.node_id))
        ZWaveNodeInterface.__init__(self)

    def command_class_0x30(self):
        """
        The command 0x30 (COMMAND_CLASS_SENSOR_BINARY) level of this node.
        Todo
        """
        values = self.get_values_for_command_class(0x30)  # COMMAND_CLASS_SENSOR_BINARY
        if values:
            for value in values:
                vdic = value.data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
                    return vdic['value'] == 'True'
        return False

    def command_class_0x31(self):
        """
        The command 0x31 (COMMAND_CLASS_SENSOR_MULTILEVEL) level of this node.
        Todo
        """
        values = self.get_values_for_command_class(0x31)  # COMMAND_CLASS_SENSOR_MULTILEVEL
        if values:
            for value in values:
                vdic = value.data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
                    return vdic['value'] == 'True'
        return False
