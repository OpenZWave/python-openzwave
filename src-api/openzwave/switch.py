# -*- coding: utf-8 -*-
"""
.. module:: openzwave.switch

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: Kevin Schlosser (@kdschlosser)

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
import threading
import logging

from .object import ZWaveNodeInterface
from ._utils import deprecated


logger = logging.getLogger(__name__)


class ZWaveNodeSwitch(ZWaveNodeInterface):
    """
    Represents an interface to switches and dimmers Commands
    """

    @property
    def switches_all(self):
        """
        Retrieve the list of values to consider as switches_all.

        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.

        Filter rules are :

            command_class = 0x27
            genre = "System"
            type = "List"
            readonly = False
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict
        """
        res = {}
        for value in self.values.values():
            if value.command_class == 0x27:
                res[value.value_id] = value

        return res

    @property
    def switch_all_state(self):
        """
        Get/Set the switch all state of a switch or a dimmer.

        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.

        * Getter:

            returns: The state of the value

            return type: ???

        * Setter:

            value: ???

            value type: ???
        """
        if 0x27 not in self._value_index_mapping:
            return

        for command_class in range(0x25, 0x27):
            if command_class in self._value_index_mapping:
                break
        else:
            return

        indices = self._value_index_mapping[command_class]
        instance = self._value_index_mapping[0x27].switch_all.instance

        if indices.level.instance == instance:
            return indices.level.data

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

    @switch_all_state.setter
    def switch_all_state(self, value):
        if 0x27 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x27].switch_all.data = value

    @property
    def switch_all_items(self):
        """
        Return the all the possible values of a switch_all.

        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.

        :return: list of possible switch all states
        :rtype: set
        """
        if 0x27 not in self._value_index_mapping:
            return []

        return self._value_index_mapping[0x27].switch_all.data_items

    @property
    def switches(self):
        """
        Retrieve the list of values to consider as switches.

        The command 0x25 (COMMAND_CLASS_SWITCH_BINARY) of this node.

        Filter rules are :

            command_class = 0x25
            genre = "User"
            type = "Bool"
            readonly = False
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict
        """
        values = {}

        for value in self.values.values():
            if value.command_class == 0x25:
                values[value.value_id] = value

        return values

    @property
    def switch_state(self):
        """
        Get/Set the state of a switch or a dimmer.

        The command 0x25 (COMMAND_CLASS_SWITCH_BINARY) of this node.

        * Getter:

            returns: The state of the value

            return type: bool

        * Setter:

            value: The state you want to set to `True`/`False`

            value type: bool
        """
        if 0x25 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x25].level.data

    @switch_state.setter
    def switch_state(self, value):
        if 0x25 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x25].level.data = value

    @property
    def dimmers(self):
        """
        Retrieve the list of values to consider as dimmers.

        The command 0x26 (COMMAND_CLASS_SWITCH_MULTILEVEL) of this node.

        Filter rules are :

            command_class = 0x26
            genre = "User"
            type = "Bool"
            readonly = False
            writeonly = False

        :return: The list of dimmers on this node
        :rtype: dict
        """
        values = {}

        for value in self.values.values():
            if value.command_class == 0x26:
                values[value.value_id] = value

        return values

    @property
    def dimmer_level(self):
        """
        Get/Set the level of a dimmer.

        The command 0x26 (COMMAND_CLASS_SWITCH_MULTILEVEL) of this node.

        * Getter:

            returns: The level : a value between 0-99

            return type: int

        * Setter:

            value: TThe level :a value between 0-99 or 255. 255 set the
            level to the last value. 0 turn the dimmer off.

            value type: int
        """
        if 0x26 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x26].level.data

    @dimmer_level.setter
    def dimmer_level(self, value):
        logger.debug("set_dimmer Level:%s", value)

        if 0x26 not in self._value_index_mapping:
            return

        if 99 < value < 255:
            value = 99
        elif value < 0:
            value = 0

        event = threading.Event()

        if self._value_index_mapping[0x26].target_value is not None:
            while self._value_index_mapping[0x26].target_value != value:
                self._value_index_mapping[0x26].level.data = value
                event.wait(0.1)

        else:
            self._value_index_mapping[0x26].level.data = value
            # Dimmers doesn't return the good level.
            # Add a Timer to refresh the value
            if value == 0:
                timer1 = threading.Timer(1, self._value_index_mapping[0x26].level.refresh)
                timer1.start()
                timer2 = threading.Timer(2, self._value_index_mapping[0x26].level.refresh)
                timer2.start()

    @property
    def rgb_bulbs(self):
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
        :rtype: dict
        """
        values = {}

        for value in self.values.values():
            if value.command_class == 0x33:
                values[value.value_id] = value

        return values

    @property
    def rgbw(self):
        """
        Get/Set the RGW value.

        The command 0x33 (COMMAND_CLASS_COLOR) of this node.

        * Getter:

            returns: ???

            return type: ???

        * Setter:

            value: ???

            value type: ???
        """
        if 0x33 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x33].color.data

    @rgbw.setter
    def rgbw(self, value):
        if 0x33 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x33].color.data = value

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

    get_switches_all = deprecated(get_switches_all, 'use property "switches_all"')

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

    set_switch_all = deprecated(set_switch_all, 'use property "switch_all_state"')

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

    get_switch_all_state = deprecated(get_switch_all_state, 'use property "switch_all_state"')

    @deprecated
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

    get_switch_all_items = deprecated(get_switch_all_items, 'use property "switch_all_items"')

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

    get_switches = deprecated(get_switches, 'use property "switches"')

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

    set_switch = deprecated(set_switch, 'use property "switch_state"')

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

    get_switch_state = deprecated(get_switch_state, 'use property "switch_state"')

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

    get_dimmers = deprecated(get_dimmers, 'use property "dimmers"')

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
                timer1 = threading.Timer(1, self.values[value_id].refresh)
                timer1.start()
                timer2 = threading.Timer(2, self.values[value_id].refresh)
                timer2.start()
            return True
        return False

    set_dimmer = deprecated(set_dimmer, 'use property "dimmer_level"')

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

    get_dimmer_level = deprecated(get_dimmer_level, 'use property "dimmer_level"')

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

    get_rgbbulbs = deprecated(get_rgbbulbs, 'use property "rgbbulbs"')

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

    set_rgbw = deprecated(set_rgbw, 'use property "rgbw"')

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

    get_rgbw = deprecated(get_rgbw, 'use property "rgbw"')
