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

# User Code Command Class - Active
# Application
COMMAND_CLASS_USER_CODE = 0x63


# noinspection PyAbstractClass
class UserCode(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_USER_CODE]

    @property
    def codes(self):
        """
        Retrieves the list of value to consider as usercodes.
        Filter rules are :

            command_class = 0x63
            genre = "User"
            type = "Raw"
            readonly = False
            writeonly = False

        :return: The list of user codes on this node
        :rtype: dict()

        """

        res = []
        for value in self[(None, COMMAND_CLASS_USER_CODE)]:
            if (
                value.type == 'Raw' and
                value.genre == 'User' and
                value.readonly is False and
                value.writeonly is False
            ):
                res += [value.data]

        return res

    def get_code(self, index):
        """
        Retrieve particular usercode value by index.
        Certain values such as user codes have index start from 0
        to max number of usercode supported and is useful for getting
        usercodes by the index.

        :param index: The index of usercode value
        :type index: int
        :return: The user code at given index on this node
        :rtype: ZWaveValue

        """
        for value in self[(None, COMMAND_CLASS_USER_CODE)]:
            if value.index == index:
                return value.data

    def set_code(self, value_id, value):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Sets usercode to value (using value_id).

        :param value_id: The value to retrieve state from
        :type value_id: int
        :param value: User Code as string
        :type value: str

        """

        try:
            self[(value_id, COMMAND_CLASS_USER_CODE)].data = value
            return True
        except (KeyError, IndexError):
            return False

    def set_code_at_index(self, index, value):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Sets usercode to value (using index of value)

        :param index: The index of value to retrieve state from
        :type index: int
        :param value: User Code as string
        :type value: str

        """

        for val in self[(None, COMMAND_CLASS_USER_CODE)]:
            if val.index == index:
                val.data = value
                return True
        return False

