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

# Protection Command Class - Active
# Application
COMMAND_CLASS_PROTECTION = 0x75


# noinspection PyAbstractClass
class Protection(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_PROTECTION]

    @property
    def protections(self):
        """
        Retrieve the list of values to consider as protection.
        Filter rules are :

            command_class = 0x75
            genre = "User"
            readonly = True
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()

        """
        return self.get_values(
            class_id=COMMAND_CLASS_PROTECTION,
            genre='System',
            type='List',
            readonly=False,
            writeonly=False
        )

    def set_protection(self, value_id, value):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Set protection to value (using value value_id).

        :param value_id: The value to set protection
        :type value_id: int
        :param value: A predefined string
        :type value: str

        """
        protections = self.protections
        if value_id in protections:
            protections[value_id].data = value
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
        protections = self.protections
        if value_id in protections:
            return protections[value_id].data

    def get_protection_items(self, value_id):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Return the all the possible values (using value value_id) of a
        protection.

        :param value_id: The value to retrieve items list
        :type value_id: int
        :return: The value of the value
        :rtype: set()

        """
        protections = self.protections
        if value_id in protections:
            return protections[value_id].data_items
