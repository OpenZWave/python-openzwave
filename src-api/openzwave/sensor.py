# -*- coding: utf-8 -*-
"""
.. module:: openzwave.sensor

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

from .object import ZWaveNodeInterface
from ._utils import deprecated


class ZWaveNodeSensor(ZWaveNodeInterface):
    """
    Represents an interface to Sensor Commands
    """

    @property
    def sensors(self):
        """
        Retrieve the list of values to consider as sensors.

        The command 0x30 (COMMAND_CLASS_SENSOR_BINARY) of this node.
        The command 0x31 (COMMAND_CLASS_SENSOR_MULTILEVEL) of this node.
        The command 0x32 (COMMAND_CLASS_METER) of this node.

        :return: values
        :rtype: dict
        """
        values = {}

        for command_class in range(0x30, 0x33):
            if command_class in self._value_index_mapping:
                break
        else:
            return

        indices = self._value_index_mapping[command_class]

        for i in range(indices.indexes.start, indices.indexes.end + 1):
            if self._value_index_mapping[command_class][i] is not None:
                value = self._value_index_mapping[command_class][i]
                values[value.value_id] = value

    @property
    def sensor_value(self):
        """
        Get the data that a sensor holds.

        The command 0x30 (COMMAND_CLASS_SENSOR_BINARY) of this node.
        The command 0x31 (COMMAND_CLASS_SENSOR_MULTILEVEL) of this node.
        The command 0x32 (COMMAND_CLASS_METER) of this node.

        :return: The state of the sensors
        :rtype: any
        """

        for command_class in range(0x30, 0x33):
            if command_class in self._value_index_mapping:
                break
        else:
            return

        indices = self._value_index_mapping[command_class]

        for i in range(indices.indexes.start, indices.indexes.end + 1):
            if self._value_index_mapping[command_class][i] is not None:
                return self._value_index_mapping[command_class][i].data

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

    get_sensors = deprecated(get_sensors, 'use property "sensors"')

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

    get_sensor_value = deprecated(get_sensor_value, 'use property "sensor_value"')
