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

    '''

    def __init__(self):
        '''
        Initialize zwave node

        :param node_id: ID of the node
        :type node_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        '''
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
                vdic = value.value_data
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

    @property
    def is_on(self):
        """
        Is this node On.
        Todo
        """
        return self.command_class_0x25()

    def command_class_0x25(self):
        """
        The command 0x25 (COMMAND_CLASS_SWITCH_BINARY) level of this node.
        Todo
        """
        values = self.get_values_for_command_class(0x25)  # COMMAND_CLASS_SWITCH_BINARY
        if values:
            for value in values:
                vdic = value.value_data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
                    return vdic['value'] == 'True'
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
                vdic = value.value_data
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
                vdic = value.value_data
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
                vdic = value.value_data
                if vdic and vdic.has_key('type') and vdic['type'] == 'Bool' and vdic.has_key('value'):
                    return vdic['value'] == 'True'
        return False
