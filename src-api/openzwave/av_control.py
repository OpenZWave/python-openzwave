# -*- coding: utf-8 -*-
"""
.. module:: openzwave.av_control

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


class ZWaveNodeSimpleAVControl(ZWaveNodeInterface):
    """
    Represents an interface to Security Commands
    """

    def av_command_send(self, command):
        """
        The command 0x94 (COMMAND_CLASS_SIMPLE_AV_CONTROL) of this node.
        :param command: one of the values returned from av_commands
        :type command: str
        """
        if 0x94 not in self._value_index_mapping:
            return False

        self._value_index_mapping[0x94].command.data = command
        return True

    @property
    def av_commands(self):
        """
        The command 0x94 (COMMAND_CLASS_SIMPLE_AV_CONTROL) of this node.
        Return available commands
        :return: list of available commands
        :rtype: list
        """
        if 0x94 not in self._value_index_mapping:
            return []

        return list(
            itm for itm in self._value_index_mapping[0x94].command.data_items
        )
