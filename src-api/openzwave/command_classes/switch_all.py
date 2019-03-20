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

# All Switch Command Class - Obsolete
# Application
COMMAND_CLASS_SWITCH_ALL = 0x27


# noinspection PyAbstractClass
class SwitchAll(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_SWITCH_ALL]

    def set_switch_all(self, value_id, value):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Set switches_all to value (using value value_id).

        :param value_id: The value to retrieve state
        :type value_id: int
        :param value: A predefined string
        :type value: str

        """
        if value_id in self.values:
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
        if value_id in self.values:
            instance = self.values[value_id].instance
            for switch in self.values:
                if self.values[switch].instance == instance:
                    return self.values[switch].data
            for dimmer in self.values:
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
        if value_id in self.values:
            return self.values[value_id].data
        return None

    def get_switch_all_items(self, value_id):
        """
        The command 0x27 (COMMAND_CLASS_SWITCH_ALL) of this node.
        Return the all the possible values (using value value_id) of a
        switch_all.

        :param value_id: The value to retrieve items list
        :type value_id: int
        :return: The value of the value
        :rtype: set()

        """
        if value_id in self.values:
            return self.values[value_id].data_items
        return None

