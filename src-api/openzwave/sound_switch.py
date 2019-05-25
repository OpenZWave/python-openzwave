# -*- coding: utf-8 -*-
"""
.. module:: openzwave.sound_switch

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


class ZWaveNodeSoundSwitch(ZWaveNodeInterface):
    """
    Represents an interface to Security Commands
    """

    @property
    def volume(self):
        """
        Get/Set Volume.

        The command 0x75 (COMMAND_CLASS_SOUND_SWITCH) of this node.

        * Getter:

            returns: volume

            return type: str

        * Setter:

            value: volume

            value type: str
        """
        if 0x79 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x79].volume.data

    @volume.setter
    def volume(self, value):
        if 0x79 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x79].volume.data = value

    @property
    def tone(self):
        """
        Get/Set Tone.

        The command 0x75 (COMMAND_CLASS_SOUND_SWITCH) of this node.

        * Getter:

            returns: tone

            return type: str

        * Setter:

            value: tone

            value type: str
        """
        if 0x79 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x79].tone.data

    @tone.setter
    def tone(self, value):
        if 0x79 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x79].tone.data = value

    @property
    def tone_items(self):
        """
        Get tone items.

        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.

        :return: list of tone items
        :rtype: list
        """

        if 0x79 not in self._value_index_mapping:
            return []

        return self._value_index_mapping[0x75].tone.data_items
