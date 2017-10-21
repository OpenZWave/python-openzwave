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
from openzwave.object import ZWaveNodeInterface
from threading import Timer

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass
logger = logging.getLogger('openzwave')
logger.addHandler(NullHandler())

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

class ZWaveNodeSwitch(ZWaveNodeInterface):
    """
    Represents an interface to switches and dimmers Commands

    """

    def get_switches_all(self):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Retrieve the list of values to consider as switches_all.
        Filter rules are :

            command_class = 0x27
            genre = "System"
            type = "List"
            readonly = False
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x27, genre='System', type='List', readonly=False, writeonly=False)

    def set_switch_all(self, value_id, value):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Set switches_all to value (using value value_id).

        :param value_id: The value to retrieve state
        :type value_id: int
        :param value: A predefined string
        :type value: str

        """
        if value_id in self.get_switches_all():
            self.values[value_id].data = value
            return True
        return False

    def get_switch_all_state(self, value_id):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Return the state (using value value_id) of a switch or a dimmer.

        :param value_id: The value to retrieve state
        :type value_id: int
        :return: The state of the value
        :rtype: bool

        """
        if value_id in self.get_switches_all():
            instance = self.values[value_id].instance
            for switch in self.get_switches():
                if self.values[switch].instance == instance:
                    return self.values[switch].data
            for dimmer in self.get_dimmers():
                if self.values[dimmer].instance == instance:
                    if self.values[dimmer].data == 0:
                        return False
                    else:
                        return True
        return None

    def get_switch_all_item(self, value_id):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Return the current value (using value value_id) of a switch_all.

        :param value_id: The value to retrieve switch_all value
        :type value_id: int
        :return: The value of the value
        :rtype: str

        """
        if value_id in self.get_switches_all():
            return self.values[value_id].data
        return None

    def get_switch_all_items(self, value_id):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Return the all the possible values (using value value_id) of a switch_all.

        :param value_id: The value to retrieve items list
        :type value_id: int
        :return: The value of the value
        :rtype: set()

        """
        if value_id in self.get_switches_all():
            return self.values[value_id].data_items
        return None

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

        :return: The list of switches on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x25, genre='User', \
        type='Bool', readonly=False, writeonly=False)

    def set_switch(self, value_id, value):
        """
        The command 0x25 (COMMAND_CLASS_SWITCH_BINARY) of this node.
        Set switch to value (using value value_id).

        :param value_id: The value to retrieve state
        :type value_id: int
        :param value: True or False
        :type value: bool

        """
        if value_id in self.get_switches():
            self.values[value_id].data = value
            return True
        return False

    def get_switch_state(self, value_id):
        """
        The command 0x25 (COMMAND_CLASS_SWITCH_BINARY) of this node.
        Return the state (using value value_id) of a switch.

        :param value_id: The value to retrieve state
        :type value_id: int
        :return: The state of the value
        :rtype: bool

        """
        if value_id in self.get_switches():
            return self.values[value_id].data
        return None

    def get_dimmers(self):
        """
        The command 0x26 (COMMAND_CLASS_SWITCH_MULTILEVEL) of this node.
        Retrieve the list of values to consider as dimmers.
        Filter rules are :

            command_class = 0x26
            genre = "User"
            type = "Bool"
            readonly = False
            writeonly = False

        :return: The list of dimmers on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x26, genre='User', \
        type='Byte', readonly=False, writeonly=False)

    def set_dimmer(self, value_id, value):
        """
        The command 0x26 (COMMAND_CLASS_SWITCH_MULTILEVEL) of this node.
        Set switch to value (using value value_id).

        :param value_id: The value to retrieve state
        :type value_id: int
        :param value: The level : a value between 0-99 or 255. 255 set the level to the last value. \
        0 turn the dimmer off
        :type value: int

        """
        logger.debug(u"set_dimmer Level:%s", value)
        if value_id in self.get_dimmers():
            if 99 < value < 255:
                value = 99
            elif value < 0:
                value = 0
            self.values[value_id].data = value
            #Dimmers doesn't return the good level.
            #Add a Timer to refresh the value
            if value == 0:
                timer1 = Timer(1, self.values[value_id].refresh)
                timer1.start()
                timer2 = Timer(2, self.values[value_id].refresh)
                timer2.start()
            return True
        return False

    def get_dimmer_level(self, value_id):
        """
        The command 0x26 (COMMAND_CLASS_SWITCH_MULTILEVEL) of this node.
        Get the dimmer level (using value value_id).

        :param value_id: The value to retrieve level
        :type value_id: int
        :return: The level : a value between 0-99
        :rtype: int

        """
        if value_id in self.get_dimmers():
            return self.values[value_id].data
        return None

    def get_rgbbulbs(self):
        """
        The command 0x33 (COMMAND_CLASS_COLOR) of this node.
        Retrieve the list of values to consider as RGBW bulbs.
        Filter rules are :

            command_class = 0x33
            genre = "User"
            type = "String"
            readonly = False
            writeonly = False

        :return: The list of dimmers on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x33, genre='User', \
        type='String', readonly=False, writeonly=False)

    def set_rgbw(self, value_id, value):
        """
        The command 0x33 (COMMAND_CLASS_COLOR) of this node.
        Set RGBW to value (using value value_id).

        :param value_id: The value to retrieve state
        :type value_id: String
        :param value: The level : a RGBW value
        :type value: int

        """
        logger.debug(u"set_rgbw value:%s", value)
        if value_id in self.get_rgbbulbs():
            self.values[value_id].data = value
            return True
        return False

    def get_rgbw(self, value_id):
        """
        The command 0x33 (COMMAND_CLASS_COLOR) of this node.
        Get the RGW value (using value value_id).

        :param value_id: The value to retrieve level
        :type value_id: int
        :return: The level : a value between 0-99
        :rtype: int

        """
        if value_id in self.get_rgbbulbs():
            return self.values[value_id].data
        return None


class ZWaveNodeSensor(ZWaveNodeInterface):
    """
    Represents an interface to Sensor Commands

    """

    def get_sensors(self, type='All'):
        """
        The command 0x30 (COMMAND_CLASS_SENSOR_BINARY) of this node.
        The command 0x31 (COMMAND_CLASS_SENSOR_MULTILEVEL) of this node.
        The command 0x32 (COMMAND_CLASS_METER) of this node.
        Retrieve the list of values to consider as sensors.
        Filter rules are :

            command_class = 0x30-32
            genre = "User"
            readonly = True
            writeonly = False

        :param type: the type of value
        :type type: 'All' or PyValueTypes
        :return: The list of switches on this node
        :rtype: dict()

        """
        values = {}
        values.update(self.get_values(type=type, class_id=0x30, genre='User', \
            readonly=True, writeonly=False))
        values.update(self.get_values(type=type, class_id=0x31, genre='User', \
            readonly=True, writeonly=False))
        values.update(self.get_values(type=type, class_id=0x32, genre='User', \
            readonly=True, writeonly=False))
        return values

    def get_sensor_value(self, value_id):
        """
        The command 0x30 (COMMAND_CLASS_SENSOR_BINARY) of this node.
        The command 0x31 (COMMAND_CLASS_SENSOR_MULTILEVEL) of this node.
        The command 0x32 (COMMAND_CLASS_METER) of this node.

        :param value_id: The value to retrieve value
        :type value_id: int
        :return: The state of the sensors
        :rtype: variable

        """
        if value_id in self.get_sensors():
            return self.values[value_id].data
        return None


class ZWaveNodeThermostat(ZWaveNodeInterface):
    """
    Represents an interface to Thermostat Commands

    """

    def get_thermostats(self, type='All'):
        """
        The command 0x40 (COMMAND_CLASS_THERMOSTAT_MODE) of this node.
        The command 0x42 (COMMAND_CLASS_THERMOSTAT_OPERATING_STATE) of this node.
        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.
        The command 0x44 (COMMAND_CLASS_THERMOSTAT_FAN_MODE) of this node.
        The command 0x45 (COMMAND_CLASS_THERMOSTAT_FAN_STATE) of this node.
        Retrieve the list of values to consider as thermostats.
        Filter rules are :

            command_class = 0x40-45
            genre = "User"
            readonly = True/False
            writeonly = False

        :param type: the type of value
        :type type: 'All' or PyValueTypes
        :return: The list of switches on this node
        :rtype: dict()

        """
        values = {}
        values.update(self.get_values(type=type, class_id=0x40, genre='User', \
            readonly=False, writeonly=False))
        values.update(self.get_values(type=type, class_id=0x42, genre='User', \
            readonly=True, writeonly=False))
        values.update(self.get_values(type=type, class_id=0x43, genre='User', \
            readonly=False, writeonly=False))
        values.update(self.get_values(type=type, class_id=0x44, genre='User', \
            readonly=False, writeonly=False))
        values.update(self.get_values(type=type, class_id=0x45, genre='User', \
            readonly=True, writeonly=False))
        return values

    def get_thermostat_value(self, value_id):
        """
        The command 0x40 (COMMAND_CLASS_THERMOSTAT_MODE) of this node.
        The command 0x42 (COMMAND_CLASS_THERMOSTAT_OPERATING_STATE) of this node.
        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.
        The command 0x44 (COMMAND_CLASS_THERMOSTAT_FAN_MODE) of this node.
        The command 0x45 (COMMAND_CLASS_THERMOSTAT_FAN_STATE) of this node.

        :param value_id: The value to retrieve value
        :type value_id: int
        :return: The state of the thermostats
        :rtype: variable

        """
        if value_id in self.get_thermostats():
            return self.values[value_id].data
        return None

    def set_thermostat_mode(self, value):
        """
        The command 0x40 (COMMAND_CLASS_THERMOSTAT_MODE) of this node.
        Set MODE to value (using value).

        :param value: The mode : 'Off', 'Heat', 'Cool'
        :type value: String

        """
        logger.debug(u"set_thermostat_mode value:%s", value)
        for v in self.get_thermostats():
            if self.values[v].command_class == 0x40 and self.values[v].label == 'Mode':
                self.values[v].data = value
                return True
        return False

    def set_thermostat_fan_mode(self, value):
        """
        The command 0x44 (COMMAND_CLASS_THERMOSTAT_FAN_MODE) of this node.
        Set FAN_MODE to value (using value).

        :param value: The mode : 'On Low', 'Auto Low'
        :type value: String

        """
        logger.debug(u"set_thermostat_fan_mode value:%s", value)
        for v in self.get_thermostats():
            if self.values[v].command_class == 0x44 and self.values[v].label == 'Fan Mode':
                self.values[v].data = value
                return True
        return False

    def set_thermostat_heating(self, value):
        """
        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.
        Set Target Heat temperature.

        :param value: The Temperature.
        :type value: Decimal

        """
        logger.debug(u"set_thermostat_heating value:%s", value)
        for v in self.get_thermostats():
            if self.values[v].command_class == 0x43 and self.values[v].label == 'Heating 1':
                self.values[v].data = value
                return True
        return False

    def set_thermostat_cooling(self, value):
        """
        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.
        Set MODE to value (using value).
        Set Target Cool temperature.

        :param value: The Temperature.
        :type value: Decimal

        """
        logger.debug(u"set_thermostat_cooling value:%s", value)
        for v in self.get_thermostats():
            if self.values[v].command_class == 0x43 and self.values[v].label == 'Cooling 1':
                self.values[v].data = value
                return True
        return False

    def get_thermostat_state(self):
        """
        The command 0x42 (COMMAND_CLASS_THERMOSTAT_OPERATING_STATE) of this node.
        Get thermostat state.

        :param value: None
        :rtype value: String

        """
        for v in self.get_thermostats():
            if self.values[v].command_class == 0x42 and self.values[v].label == 'Operating State':
                return self.values[v].data
        return None

    def get_thermostat_fan_state(self):
        """
        The command 0x45 (COMMAND_CLASS_THERMOSTAT_FAN_STATE) of this node.
        Get thermostat state.

        :param value: None
        :rtype value: String

        """
        for v in self.get_thermostats():
            if self.values[v].command_class == 0x45 and self.values[v].label == 'Fan State':
                return self.values[v].data
        return None


class ZWaveNodeSecurity(ZWaveNodeInterface):
    """
    Represents an interface to Security Commands

    """

    def get_protections(self):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Retrieve the list of values to consider as protection.
        Filter rules are :

            command_class = 0x75
            genre = "User"
            readonly = True
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x75, genre='System', \
            type='List', readonly=False, writeonly=False)

    def set_protection(self, value_id, value):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Set protection to value (using value value_id).

        :param value_id: The value to set protection
        :type value_id: int
        :param value: A predefined string
        :type value: str

        """
        if value_id in self.get_protections():
            self.values[value_id].data = value
            return True
        return False

    def get_protection_item(self, value_id):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Return the current value (using value value_id) of a protection.

        :param value_id: The value to retrieve protection value
        :type value_id: int
        :return: The value of the value
        :rtype: str

        """
        if value_id in self.get_protections():
            return self.values[value_id].data
        return None

    def get_protection_items(self, value_id):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Return the all the possible values (using value value_id) of a protection.

        :param value_id: The value to retrieve items list
        :type value_id: int
        :return: The value of the value
        :rtype: set()

        """
        if value_id in self.get_protections():
            return self.values[value_id].data_items
        return None


class ZWaveNodeDoorLock(ZWaveNodeInterface):
    """
    Represents an interface to door lock and user codes associated with door locks
    """

    def get_doorlocks(self):
        """
        The command 0x62 (COMMAND_CLASS_DOOR_LOCK) of this node.
        Retrieves the list of values to consider as doorlocks.
        Filter rules are :

            command_class = 0x62
            genre = "User"
            type = "Bool"
            readonly = False
            writeonly = False

        :return: The list of door locks on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x62, genre='User', type='Bool', readonly=False, writeonly=False)

    def set_doorlock(self, value_id, value):
        """
        The command 0x62 (COMMAND_CLASS_DOOR_LOCK) of this node.
        Sets doorlock to value (using value_id).

        :param value_id: The value to retrieve state from
        :type value_id: int
        :param value: True or False
        :type value: bool

        """
        if value_id in self.get_doorlocks():
            self.values[value_id].data = value
            return True
        return False

    def get_usercode(self, index):
        """
        Retrieve particular usercode value by index.
        Certain values such as user codes have index start from 0
        to max number of usercode supported and is useful for getting
        usercodes by the index.

        :param index: The index of usercode value
        :type index: int
        :return: The user code at given index on this node
        :rtype: ZWaveValue

        """
        usercode = self.get_usercodes(index)
        if len(usercode) == 0:
            return None
        return list(usercode.values())[0]

    def get_usercodes(self, index='All'):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Retrieves the list of value to consider as usercodes.
        Filter rules are :

            command_class = 0x63
            genre = "User"
            type = "Raw"
            readonly = False
            writeonly = False

        :return: The list of user codes on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x63, type='Raw', genre='User', readonly=False, writeonly=False, index=index)

    def set_usercode(self, value_id, value):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Sets usercode to value (using value_id).

        :param value_id: The value to retrieve state from
        :type value_id: int
        :param value: User Code as string
        :type value: str

        """
        if value_id in self.get_usercodes():
            self.values[value_id].data = value
            return True
        return False

    def set_usercode_at_index(self, index, value):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Sets usercode to value (using index of value)

        :param index: The index of value to retrieve state from
        :type index: int
        :param value: User Code as string
        :type value: str

        """
        usercode = self.get_usercode(index)
        if usercode:
            usercode.data = value
            return True
        return False


    def get_doorlock_logs(self):
        """
        The command 0x4c (COMMAND_CLASS_DOOR_LOCK_LOGGING) of this node.
        Retrieves the value consisting of log records.
        Filter rules are :

            command_class = 0x4c
            genre = "User"
            type = "String"
            readonly = True

        :return: The dict of log records with value_id as key
        :rtype: dict()

        """
        return self.get_values(class_id=0x4c, type='String', genre='User', readonly=True)
