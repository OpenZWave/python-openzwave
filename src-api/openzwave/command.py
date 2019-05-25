# -*- coding: utf-8 -*-
"""
.. module:: openzwave.command

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
from .object import ZWaveNodeInterface


logger = logging.getLogger(__name__)


class ZWaveNodeBasic(ZWaveNodeInterface):
    """
    Represents an interface to BasicCommands
    I known it's not necessary as they can be included in the node directly.
    But it's a good starting point.

    What I want to do is provide an automatic mapping system hidding
    the mapping classes.

    First example, the battery level, it's not a basic command but don't care.
    Its command class is 0x80.

    A user should write

    .. code-block:: python

        if self.handle_command_class(class_id):
            ret=command_Class(...)

    The classic way to do it is a classic method of registering. But

    Another way : using heritage multiple

    ZWaveNode(ZWaveObject, ZWaveNodeBasic, ....)
    The interface will implement methods
    command_class_0x80(param1,param2,...)
    That's the first thing to do
    We also can define a property with a friendly name

    handle_command_class will do the rest

    Another way to do it :
    A node can manage actuators (switch, dimmer, ...)
    and sensors (temperature, consummation, temperature)

    So we need a kind of mechanism to retrieve commands in a user friendly way
    Same for sensors.

    A good use case is the AN158 Plug-in Meter Appliance Module
    We will study the following command classes :
    'COMMAND_CLASS_SWITCH_ALL', 'COMMAND_CLASS_SWITCH_BINARY',
    'COMMAND_CLASS_METER',

    The associated values are :

    .. code-block:: python

        COMMAND_CLASS_SWITCH_ALL : {
            72057594101481476L: {
                'help': '',
                'max': 0L,
                'is_polled': False,
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
                'is_polled': False,
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
                'is_polled': False,
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
                'is_polled': False,
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
                'is_polled': False,
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
                'is_polled': False,
                'units': 'W',
                'data': 0.0,
                'min': 0L,
                'writeonly': False,
                'label': 'Power',
                'readonly': True,
                'data_str': 0.0,
                'type': 'Decimal'}
        }

    Another example from an homePro dimmer (not configured in openzwave):

    .. code-block:: python

        COMMAND_CLASS_SWITCH_MULTILEVEL : {
            72057594109853736L: {
                'help': '',
                'max': 0L,
                'is_polled': False,
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
                'is_polled': False,
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
                'is_polled': False,
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
                'is_polled': False,
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
                'is_polled': False,
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
        get_switch (label) : retrieve the value where label=label
    """


    def get_battery_level(self, value_id=None):
        """
        The battery level of this node.
        The command 0x80 (COMMAND_CLASS_BATTERY) of this node.

        :param value_id: The value to retrieve state. If None, retrieve the first value
        :type value_id: int
        :return: The level of this battery
        :rtype: int
        """
        if value_id is None:
            for val in self.get_battery_levels():
                return self.values[val].data
        elif value_id in self.get_battery_levels():
            return self.values[value_id].data
        return None

    def get_battery_levels(self):
        """
        The command 0x80 (COMMAND_CLASS_BATTERY) of this node.
        Retrieve the list of values to consider as batteries.
        Filter rules are :

            command_class = 0x80
            genre = "User"
            type = "Byte"
            readonly = True
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()
        """
        return self.get_values(class_id=0x80, genre='User', \
        type='Byte', readonly=True, writeonly=False)

    def get_power_level(self, value_id=None):
        """
        The power level of this node.
        The command 0x73 (COMMAND_CLASS_POWERLEVEL) of this node.

        :param value_id: The value to retrieve state. If None, retrieve the first value
        :type value_id: int
        :return: The level of this battery
        :rtype: int
        """
        if value_id is None:
            for val in self.get_power_levels():
                return self.values[val].data
        elif value_id in self.get_power_levels():
            return self.values[value_id].data
        return None

    def get_power_levels(self):
        """
        The command 0x73 (COMMAND_CLASS_POWERLEVEL) of this node.
        Retrieve the list of values to consider as power_levels.
        Filter rules are :

            command_class = 0x73
            genre = "User"
            type = "Byte"
            readonly = True
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()
        """
        return self.get_values(class_id=0x73, genre='User', \
        type='Byte', readonly=True, writeonly=False)

    def can_wake_up(self):
        """
        Check if node contain the command class 0x84 (COMMAND_CLASS_WAKE_UP).

        Filter rules are :

            command_class = 0x84

        :return: True if the node can wake up
        :rtype: bool
        """
        res = self.get_values(class_id=0x84)
        if res is not None and len(res) > 0:
            return True
        else:
            return False

    def get_configs(self, readonly='All', writeonly='All'):
        """
        The command 0x70 (COMMAND_CLASS_CONFIGURATION) of this node.
        Retrieve the list of configuration parameters.

        Filter rules are :
            command_class = 0x70
            genre = "Config"
            readonly = "All" (default) or as passed in arg

        :param readonly: whether to retrieve readonly configs
        :param writeonly: whether to retrieve writeonly configs
        :return: The list of configuration parameters
        :rtype: dict()
        """
        return self.get_values(class_id=0x70, genre='Config', readonly=readonly, writeonly=writeonly)

    def set_config(self, value_id, value):
        """
        The command 0x70 (COMMAND_CLASS_CONFIGURATION) of this node.
        Set config to value (using value value_id)

        :param value_id: The value to retrieve state
        :type value_id: int
        :param value: Appropriate value for given config
        :type value: any
        """
        if value_id in self.get_configs(readonly=False):
            self.values[value_id].data = value
            return True
        return False


    def get_config(self, value_id=None):
        """
        The command 0x70 (COMMAND_CLASS_CONFIGURATION) of this node.
        Set config to value (using value value_id)

        :param value_id: The value to retrieve value. If None, retrieve the first value
        :type value_id: int
        :return: The level of this battery
        :rtype: int
        """
        if value_id is None:
            for val in self.get_configs():
                return self.values[val].data
        elif value_id in self.get_configs():
            return self.values[value_id].data
        return None

    def can_set_indicator(self):
        """
        Check if node contain the command class 0x87 (COMMAND_CLASS_INDICATOR).

        Filter rules are :

            command_class = 0x87

        :return: True if the node can set the indicator
        :rtype: bool
        """
        res = self.get_values(class_id=0x87)
        if res is not None and len(res) > 0:
            return True
        else:
            return False


