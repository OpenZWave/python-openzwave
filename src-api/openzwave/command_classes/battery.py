# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :synopsis: openzwave API

.. moduleauthor: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com> &
 kdschlosser aka Kevin Schlosser

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

# Battery Command Class - Active
# Management
COMMAND_CLASS_BATTERY = 0x80


# noinspection PyAbstractClass
class Battery(CommandClassBase):
    """
    Battery Command Class

    symbol: `COMMAND_CLASS_BATTERY`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_BATTERY]

    def get_battery_level(self, value_id=None):
        """
        The battery level of this node.

        :param value_id: The value to retrieve state. If None, retrieve the
        first value
        :type value_id: int
        :return: The level of this battery
        :rtype: int
        """

        if value_id is None:
            value_id = -1
        try:
            return self[(value_id, COMMAND_CLASS_BATTERY)].data
        except (KeyError, IndexError):
            return None

    @property
    def battery_levels(self):
        """
        Retrieve the list of values to consider as batteries.
        Filter rules are :

            command_class = COMMAND_CLASS_BATTERY
            genre = "User"
            type = "Byte"
            readonly = True
            writeonly = False

        :return: list of levels
        :rtype: list
        """

        res = []

        for value in self[(None, COMMAND_CLASS_BATTERY)]:
            if (
                value.genre == 'User' and
                value.type == 'byte' and
                value.readonly is True
            ):
                res += [value.data]

        return res
