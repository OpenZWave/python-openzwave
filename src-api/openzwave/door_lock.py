# -*- coding: utf-8 -*-
"""
.. module:: openzwave.door_lock

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

import threading

from .object import ZWaveNodeInterface
from .user_codes import ZWaveUserCodes
from ._utils import deprecated


class ZWaveNodeDoorLock(ZWaveNodeInterface):
    """
    Represents an interface to door lock and user codes associated
    with door locks
    """

    @property
    def door_locks(self):
        """
        Retrieves the list of values to consider as doorlocks.

        The command 0x62 (COMMAND_CLASS_DOOR_LOCK) of this node.

        :return: The list of door locks on this node
        :rtype: dict
        """
        if 0x62 not in self._value_index_mapping:
            return {}

        res = {}
        for value in self._value_index_mapping[0x62]:
            if value is None:
                continue

            res[value.value_id] = value

        return res

    @property
    def door_lock(self):
        """
        Get/Set the door lock state.

        The command 0x62 (COMMAND_CLASS_DOOR_LOCK) of this node.

        * Getter:

            returns: `True` if locked `False` otherwise

            return type: bool

        * Setter:

            value: `True` to lock `False` to unlock

            value type: bool
        """
        if 0x62 not in self._value_index_mapping:
            return None

        return self._value_index_mapping[0x62].lock.data

    @door_lock.setter
    def door_lock(self, value):
        if 0x62 not in self._value_index_mapping:
            return

        self._value_index_mapping[0x62].lock.data = value

    @property
    def user_codes(self):
        """
        Gets user code list

        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.

        :return: class:`openzwave.user_codes.ZWaveUserCodes` instance, None
        """
        if 0x63 not in self._value_index_mapping:
            return

        return ZWaveUserCodes(self._value_index_mapping[0x63])

    @property
    def doorlock_logs(self):
        """
        Retrieves a list of log entries

        The command 0x4c (COMMAND_CLASS_DOOR_LOCK_LOGGING) of this node.

        :return: a list of log entries
        :rtype: list
        """
        res = []

        if 0x4c not in self._value_index_mapping:
            return res

        event = threading.Event()
        indices = self._value_index_mapping[0x4c]

        for i in range(indices.system_config_max_records.data):
            indices.get_record_no.data = i
            if indices.log_record.data in res:
                event.wait(0.2)

            if indices.log_record.data not in res:
                res += [indices.log_record.data]
        return res

    def get_doorlocks(self):
        """
        The command 0x62 (COMMAND_CLASS_DOOR_LOCK) of this node.
        Retrieves the list of values to consider as doorlocks.
        Filter rules are :

            command_class = 0x62
            genre = "User"
            type = "Bool"
            readonly = False
            writeonly = False

        :return: The list of door locks on this node
        :rtype: dict()

        """
        return self.get_values(class_id=0x62, genre='User', type='Bool',
            readonly=False, writeonly=False)

    get_doorlocks = deprecated(
        get_doorlocks,
        'use property "door_locks"'
    )

    def set_doorlock(self, value_id, value):
        """
        The command 0x62 (COMMAND_CLASS_DOOR_LOCK) of this node.
        Sets doorlock to value (using value_id).

        :param value_id: The value to retrieve state from
        :type value_id: int
        :param value: True or False
        :type value: bool

        """
        if value_id in self.get_doorlocks():
            self.values[value_id].data = value
            return True
        return False

    set_doorlock = deprecated(
        set_doorlock,
        'use property "door_lock"'
    )

    def get_usercode(self, index):
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
        usercode = self.get_usercodes(index)
        if len(usercode) == 0:
            return None
        return list(usercode.values())[0]

    get_usercode = deprecated(
        get_usercode,
        'use property "user_codes"'
    )

    def get_usercodes(self, index='All'):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
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
        return self.get_values(class_id=0x63, type='Raw', genre='User',
            readonly=False, writeonly=False, index=index)

    get_usercodes = deprecated(
        get_usercodes,
        'use property "user_codes"'
    )

    def set_usercode(self, value_id, value):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Sets usercode to value (using value_id).

        :param value_id: The value to retrieve state from
        :type value_id: int
        :param value: User Code as string
        :type value: str

        """
        if value_id in self.get_usercodes():
            self.values[value_id].data = value
            return True
        return False

    set_usercode = deprecated(
        set_usercode,
        'use property "user_codes"'
    )

    def set_usercode_at_index(self, index, value):
        """
        The command 0x63 (COMMAND_CLASS_USER_CODE) of this node.
        Sets usercode to value (using index of value)

        :param index: The index of value to retrieve state from
        :type index: int
        :param value: User Code as string
        :type value: str

        """
        usercode = self.get_usercode(index)
        if usercode:
            usercode.data = value
            return True
        return False

    set_usercode_at_index = deprecated(
        set_usercode_at_index,
        'use property "user_codes"'
    )

    def get_doorlock_logs(self):
        """
        The command 0x4c (COMMAND_CLASS_DOOR_LOCK_LOGGING) of this node.
        Retrieves the value consisting of log records.
        Filter rules are :

            command_class = 0x4c
            genre = "User"
            type = "String"
            readonly = True

        :return: The dict of log records with value_id as key
        :rtype: dict()

        """
        return self.get_values(class_id=0x4c, type='String', genre='User',
            readonly=True)

    get_doorlock_logs = deprecated(
        get_doorlock_logs,
        'use property "doorlock_logs"'
    )
