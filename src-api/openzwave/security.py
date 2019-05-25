# -*- coding: utf-8 -*-
"""
.. module:: openzwave.security

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


class ZWaveNodeSecurity(ZWaveNodeInterface):
    """
    Represents an interface to Security Commands
    """

    @property
    def protection(self):
        """
        Get/Set Protection.

        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.

        * Getter:

            returns: the current protection

            return type: str

        * Setter:

            value: new protection

            value type: str
        """
        if 0x75 not in self._value_index_mapping:
            return

        return self._value_index_mapping[0x75].protection.data

    @protection.setter
    def protection(self, value):
        if 0x75 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x75].protection.data = value

    @property
    def protections(self):
        """
        Retrieve the list of values to consider as protection.

        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.

        :return: values
        :rtype: dict
        """
        if 0x75 not in self._value_index_mapping:
            return {}

        res = {}
        for value in self._value_index_mapping[0x75]:
            if value is None:
                continue

            res[value.value_id] = value

        return res

    @property
    def protection_items(self):
        """
        List of protection values.

        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.

        :return: list of protection values
        :rtype: list
        """
        if 0x75 not in self._value_index_mapping:
            return []

        return self._value_index_mapping[0x75].protection.data_items

    def get_protections(self):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Retrieve the list of values to consider as protection.
        Filter rules are :

            command_class = 0x75
            genre = "User"
            readonly = True
            writeonly = False

        :return: The list of switches on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x75, genre='System', \
            type='List', readonly=False, writeonly=False)

    get_protections = deprecated(
        get_protections,
        'use property "protections"'
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
        if value_id in self.get_protections():
            self.values[value_id].data = value
            return True
        return False

    set_protection = deprecated(
        set_protection,
        'use property "protection"'
    )

    def get_protection_item(self, value_id):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Return the current value (using value value_id) of a protection.

        :param value_id: The value to retrieve protection value
        :type value_id: int
        :return: The value of the value
        :rtype: str

        """
        if value_id in self.get_protections():
            return self.values[value_id].data
        return None

    get_protection_item = deprecated(
        get_protection_item,
        'use property "protection"'
    )

    def get_protection_items(self, value_id):
        """
        The command 0x75 (COMMAND_CLASS_PROTECTION) of this node.
        Return the all the possible values (using value value_id) of a protection.

        :param value_id: The value to retrieve items list
        :type value_id: int
        :return: The value of the value
        :rtype: set()

        """
        if value_id in self.get_protections():
            return self.values[value_id].data_items
        return None

    get_protection_items = deprecated(
        get_protection_items,
        'use property "protection_items"'
    )
