# -*- coding: utf-8 -*-
"""
.. module:: openzwave.notification

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


class ZWaveNodeNotification(ZWaveNodeInterface):
    """
    Represents an interface to Security Commands
    """

    @property
    def alarm_state(self):
        """
        Get Alarm States

        The command 0x71 COMMAND_CLASS_NOTIFICATION (COMMAND_CLASS_ALARM)
        of this node.

        :return: list of class:`openzwave.value.ZWaveValue` instances
        :rtype: list
        """
        if 0x71 not in self._value_index_mapping:
            return

        start = self._value_index_mapping[0x71].indexes.start
        end = self._value_index_mapping[0x71].indexes.end + 1

        res = []

        for i in range(start, end):
            if self._value_index_mapping[0x71][i] is not None:
                res += [self._value_index_mapping[0x71][i]]

        return res

    @property
    def alarm_level(self):
        """
        Get Alarm Level

        The command 0x71 COMMAND_CLASS_NOTIFICATION (COMMAND_CLASS_ALARM)
        of this node.

        :return: level
        :rtype: str
        """
        if 0x71 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x71].level_v1.data

    @property
    def alarm_type(self):
        """
        Get Alarm Type

        The command 0x71 COMMAND_CLASS_NOTIFICATION (COMMAND_CLASS_ALARM) of
        this node.

        :return: alarm type
        :rtype: str
        """
        if 0x71 not in self._value_index_mapping:
            return []

        return self._value_index_mapping[0x71].type_v1.data

    @property
    def alarm_parameters(self):
        """
        Get Alarm Parameters

        The command 0x71 COMMAND_CLASS_NOTIFICATION (COMMAND_CLASS_ALARM)
        of this node.

        :return: list of class:`openzwave.value.ZWaveValue` instances
        :rtype: list
        """
        if 0x71 not in self._value_index_mapping:
            return []

        res = []

        start = self._value_index_mapping[0x71].indexes.param_start
        end = self._value_index_mapping[0x71].indexes.param_end + 1

        for i in range(start, end):
            if self._value_index_mapping[0x71][i] is not None:
                res += [self._value_index_mapping[0x71][i]]

        return res
