# -*- coding: utf-8 -*-
"""
.. module:: openzwave.thermostat

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

import logging

from .object import ZWaveNodeInterface
from ._utils import deprecated


logger = logging.getLogger(__name__)


class ZWaveNodeThermostat(ZWaveNodeInterface):
    """
    Represents an interface to Thermostat Commands
    """

    @property
    def thermostats(self):
        """
        Retrieve the list of values to consider as thermostats.

        The command 0x40 (COMMAND_CLASS_THERMOSTAT_MODE) of this node.
        The command 0x42 (COMMAND_CLASS_THERMOSTAT_OPERATING_STATE) of this node.
        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.
        The command 0x44 (COMMAND_CLASS_THERMOSTAT_FAN_MODE) of this node.
        The command 0x45 (COMMAND_CLASS_THERMOSTAT_FAN_STATE) of this node.

        :return: values
        :rtype: dict
        """
        values = {}

        for value in self.values.values():
            if value.command_class in (0x40, 0x42, 0x43, 0x44, 0x45):
                values[value.value_id] = value

        return values

    @property
    def thermostat_state(self):
        """
        The Current settings and states of a thermostat

        The command 0x40 (COMMAND_CLASS_THERMOSTAT_MODE) of this node.
        The command 0x42 (COMMAND_CLASS_THERMOSTAT_OPERATING_STATE) of this node.
        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.
        The command 0x44 (COMMAND_CLASS_THERMOSTAT_FAN_MODE) of this node.
        The command 0x45 (COMMAND_CLASS_THERMOSTAT_FAN_STATE) of this node.

        :return: The state of the thermostat
        :rtype: dict
        """
        res = {}

        if 0x43 in self._value_index_mapping:
            value = self._value_index_mapping[0x43]
            set_points = []

            for i in range(value.max_entry + 1):
                if value[i] is not None:
                    set_points += [
                        [
                            value[i].label,
                            value[i].data,
                            value[i].unit
                        ]
                    ]

            res['setpoints'] = set_points[:]

        if 0x42 in self._value_index_mapping:
            res['operating_state'] = (
                self._value_index_mapping[0x42].operating_state.data
            )

        if 0x40 in self._value_index_mapping:
            res['operating_mode'] = self._value_index_mapping[0x40].mode.data

        if 0x45 in self._value_index_mapping:
            res['fan_state'] = self._value_index_mapping[0x45].fan_state.data

        if 0x44 in self._value_index_mapping:
            res['fan_mode'] = self._value_index_mapping[0x44].fan_mode.data

        return res

    @property
    def thermostat_operating_mode(self):
        """
        Get/Set the operating mode.

        The command 0x40 (COMMAND_CLASS_THERMOSTAT_MODE) of this node.

        * Getter:

            returns: current set mode

            return type: str

        * Setter:

            value: the mode

            value type: str
        """
        if 0x40 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x40].mode.data

    @thermostat_operating_mode.setter
    def thermostat_operating_mode(self, value):
        logger.debug("set_thermostat_mode value:%s", value)

        if 0x40 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x40].mode.data = value

    @property
    def thermostat_operating_state(self):
        """
        The command 0x42 (COMMAND_CLASS_THERMOSTAT_OPERATING_STATE) of this node.
        Get thermostat state.
        :rtype value: String
        """
        if 0x42 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x42].operating_state.data

    @property
    def thermostat_fan_mode(self):
        """
        Get/Set the fan mode.

        The command 0x44 (COMMAND_CLASS_THERMOSTAT_FAN_MODE) of this node.

        * Getter:

            returns: current set fan mode

            return type: str

        * Setter:

            value: the fan mode

            value type: str
        """
        if 0x44 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x44].fan_mode.data

    @thermostat_fan_mode.setter
    def thermostat_fan_mode(self, value):
        logger.debug("set_thermostat_fan_mode value:%s", value)

        if 0x44 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x44].fan_mode.data = value

    @property
    def thermostat_fan_state(self):
        """
        The command 0x45 (COMMAND_CLASS_THERMOSTAT_FAN_STATE) of this node.
        Get thermostat state.
        :rtype value: String
        """
        if 0x45 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x45].fan_state.data

    @property
    def thermostat_heating(self):
        """
        Get/Set the target heat temperature.

        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.

        * Getter:

            returns: current target temperature

            return type: float

        * Setter:

            value: new target temperature

            value type: float
        """
        if 0x43 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x43].heating.data

    @thermostat_heating.setter
    def thermostat_heating(self, value):
        if 0x43 not in self._value_index_mapping:
            return

        logger.debug("set_thermostat_heating value:%s", value)
        self._value_index_mapping[0x43].heating.data = value

    @property
    def thermostat_economy_heating(self):
        """
        Get/Set the target economy heat temperature.

        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.

        * Getter:

            returns: current target temperature

            return type: float

        * Setter:

            value: new target temperature

            value type: float
        """
        if 0x43 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x43].economy_heating.data

    @thermostat_economy_heating.setter
    def thermostat_economy_heating(self, value):
        if 0x43 not in self._value_index_mapping:
            return

        logger.debug("set_thermostat_economy_heating value:%s", value)
        self._value_index_mapping[0x43].economy_heating.data = value

    @property
    def thermostat_away_heating(self):
        """
        Get/Set the target away heat temperature.

        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.

        * Getter:

            returns: current target temperature

            return type: float

        * Setter:

            value: new target temperature

            value type: float
        """
        if 0x43 not in self._value_index_mapping:
            return
        return self._value_index_mapping[0x43].away_heating.data

    @thermostat_away_heating.setter
    def thermostat_away_heating(self, value):
        if 0x43 not in self._value_index_mapping:
            return

        logger.debug("set_thermostat_away_heating value:%s", value)
        self._value_index_mapping[0x43].away_heating.data = value

    @property
    def thermostat_cooling(self):
        """
        Get/Set the target cool temperature.

        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.

        * Getter:

            returns: current target temperature

            return type: float

        * Setter:

            value: new target temperature

            value type: float
        """
        if 0x43 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x43].cooling.data

    @thermostat_cooling.setter
    def thermostat_cooling(self, value):
        if 0x43 not in self._value_index_mapping:
            return

        logger.debug("set_thermostat_cooling value:%s", value)
        self._value_index_mapping[0x43].cooling.data = value

    @property
    def thermostat_economy_cooling(self):
        """
        Get/Set the target economy cool temperature.

        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.

        * Getter:

            returns: current target temperature

            return type: float

        * Setter:

            value: new target temperature

            value type: float
        """
        if 0x43 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x43].economy_cooling.data

    @thermostat_economy_cooling.setter
    def thermostat_economy_cooling(self, value):
        if 0x43 not in self._value_index_mapping:
            return

        logger.debug("set_thermostat_economy_cooling value:%s", value)
        self._value_index_mapping[0x43].economy_cooling.data = value

    @property
    def thermostat_away_cooling(self):
        """
        Get/Set the target away cool temperature.

        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.

        * Getter:

            returns: current target temperature

            return type: float

        * Setter:

            value: new target temperature

            value type: float
        """
        if 0x43 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x43].away_cooling.data

    @thermostat_away_cooling.setter
    def thermostat_away_cooling(self, value):
        if 0x43 not in self._value_index_mapping:
            return

        logger.debug("set_thermostat_away_cooling value:%s", value)
        self._value_index_mapping[0x43].away_cooling.data = value

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

    get_thermostats = deprecated(get_thermostats, 'use property "thermostats"')

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

    get_thermostat_value = deprecated(
        get_thermostat_value,
        'use property "thermostat_state"'
    )

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

    set_thermostat_mode = deprecated(
        set_thermostat_mode,
        'use property "thermostat_operating_mode"'
    )

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

    set_thermostat_fan_mode = deprecated(
        set_thermostat_fan_mode,
        'use property "thermostat_fan_mode"'
    )

    def set_thermostat_heating(self, value):
        """
        The command 0x43 (COMMAND_CLASS_THERMOSTAT_SETPOINT) of this node.
        Set Target Heat temperature.

        :param value: The Temperature.
        :type value: Decimal

        """
        logger.debug(u"set_thermostat_heating value:%s", value)
        for v in self.get_thermostats():
            if self.values[v].command_class == 0x43 and self.values[v].label in ('Heating 1', 'Heating'):
                self.values[v].data = value
                return True
        return False

    set_thermostat_heating = deprecated(
        set_thermostat_heating,
        'use property "thermostat_heating"'
    )

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
            if self.values[v].command_class == 0x43 and self.values[v].label in ('Cooling 1', 'Cooling'):
                self.values[v].data = value
                return True
        return False

    set_thermostat_cooling = deprecated(
        set_thermostat_cooling,
        'use property "thermostat_cooling"'
    )

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

    get_thermostat_state = deprecated(
        get_thermostat_state,
        'use property "thermostat_operating_state"'
    )

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

    get_thermostat_fan_state = deprecated(
        get_thermostat_fan_state,
        'use property "thermostat_fan_state"'
    )


