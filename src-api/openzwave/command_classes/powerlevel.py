# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave API

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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

from .command_class_base import CommandClassBase

# Powerlevel Command Class - Active
# Network-Protocol
COMMAND_CLASS_POWERLEVEL = 0x73


# noinspection PyAbstractClass
class Powerlevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_POWERLEVEL]

    def get_power_level(self, value_id=None):
        """
        The power level of this node.

        :param value_id: The value to retrieve state. If None, retrieve the
        first value
        :type value_id: int
        :return: The power level
        :rtype: int
        """

        if value_id is None:
            return self.power_levels[0]
        try:
            value = self[(value_id, COMMAND_CLASS_POWERLEVEL)]
            if (
                value.genre == 'User' and
                value.type == 'Byte' and
                value.readonly is True and
                value.writeonly is False
            ):
                return value.data
            else:
                return None

        except (KeyError, IndexError):
            return None

    @property
    def power_levels(self):
        """
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

        res = []

        for value in self[(None, COMMAND_CLASS_POWERLEVEL)]:
            if (
                value.genre == 'User' and
                value.type == 'Byte' and
                value.readonly is True and
                value.writeonly is False
            ):
                res += [value.data]

        return res

    def test_power_level(self, db):
        try:
            self[('Test Powerlevel', COMMAND_CLASS_POWERLEVEL)].data = db
        except KeyError:
            pass

    def test_node(self):
        for value in self[(None, COMMAND_CLASS_POWERLEVEL)]:
            if value.label == 'Test Node':
                value.data = 1

    @property
    def acked_frames(self):
        try:
            return self[('Acked Frames', COMMAND_CLASS_POWERLEVEL)].data
        except KeyError:
            return None

    @property
    def frame_count(self):
        try:
            return self[('Frame Count', COMMAND_CLASS_POWERLEVEL)].data
        except KeyError:
            return None
