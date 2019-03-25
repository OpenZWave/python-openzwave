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

# Protection Command Class - Active
# Application
COMMAND_CLASS_PROTECTION = 0x75


# noinspection PyAbstractClass
class Protection(CommandClassBase):

    PROTECTION_STATES = [
        'Unprotected',
        'Protection by Sequence',
        'No Operation Possible',
        'Unknown'
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_PROTECTION]

    @property
    def protections(self):
        """
        Protection states

        Retrieves a list of the set protection states

        :return: list of states
        :rtype: list
        """
        res = []
        for value in self[(None, COMMAND_CLASS_PROTECTION)]:
            if value.label != 'Protection':
                continue

            res += [value.data]
        return res

    def set_protection(self, value_id, value):
        """
        Set Protection State

        Values:
        <br></br>
        * `'Unprotected'`
        * `'Protection by Sequence'`
        * `'No Operation Possible'`
        * `'Unknown'`

        :param value_id: value id of the protection
        :type value_id: int
        :param value: protection state
        :type value: int, str
        :return: command successful `True`/`False`
        :rtype: bool
        """
        if isinstance(value, int):
            try:
                value = self.PROTECTION_STATES[value]
            except IndexError:
                return False

        if value in self.PROTECTION_STATES:

            key = (value_id, COMMAND_CLASS_PROTECTION)
            try:
                self[key].data = value
                return True
            except (IndexError, KeyError):
                pass

        return False

    def get_protection_state(self, value_id):
        """
        Get Protection State

        Values:
        <br></br>
        * `'Unprotected'`
        * `'Protection by Sequence'`
        * `'No Operation Possible'`
        * `'Unknown'`

        :param value_id: value id of the protection
        :type value_id: int
        :return: protection state or None if command failed
        :rtype: str, None
        """
        key = (value_id, COMMAND_CLASS_PROTECTION)
        try:
            return self[key].data
        except (IndexError, KeyError):
            return None
