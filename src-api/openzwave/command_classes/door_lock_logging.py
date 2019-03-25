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

# Door Lock Logging Command Class - Active
# Application
COMMAND_CLASS_DOOR_LOCK_LOGGING = 0x4C


# noinspection PyAbstractClass
class DoorLockLogging(CommandClassBase):
    """
    Door Lock Logging Command Class

    symbol: `COMMAND_CLASS_DOOR_LOCK_LOGGING`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_DOOR_LOCK_LOGGING]

    @property
    def doorlock_logging_max_number_of_records(self):
        """
        Door Lock Logging Max Number of Records (`property`)

        :return: max number of records or None if command failed
        :rtype: int, None
        """
        key = ('Max Number of Record', COMMAND_CLASS_DOOR_LOCK_LOGGING)
        try:
            return self[key].data
        except KeyError:
            return None

    __doorlock_logging_current_record_number_doc = """
        Door Lock Logging Current Record Number (`property`)

        :param value: record number
        :type value: int
        :return: record number or None if command failed
        :rtype: int, None
    """

    def __doorlock_logging_current_record_number_get(self):
        key = ('Current Record Number', COMMAND_CLASS_DOOR_LOCK_LOGGING)
        try:
            return self[key].data
        except KeyError:
            return None

    def __doorlock_logging_current_record_number_set(self, value):
        key = ('Current Record Number', COMMAND_CLASS_DOOR_LOCK_LOGGING)
        try:
            self[key].data = value
        except KeyError:
            pass

    doorlock_logging_current_record_number = property(
        __doorlock_logging_current_record_number_get,
        __doorlock_logging_current_record_number_set,
        doc=__doorlock_logging_current_record_number_doc
    )

    @property
    def doorlock_logging_door_lock_records(self):
        """
        Door Lock Logging Records (`property`)

        List of door lock change records

        :return: list of records
        :rtype: list
        """

        res = []
        for i in range(self.doorlock_logging_max_number_of_records):
            res += [self.doorlock_logging_log_record(i)]

        return res

    def doorlock_logging_log_record(self, record_num):
        """
        Door Lock Logging Record

        :param record_num: record number to retrieve
        :type record_num: int
        :return: logging entry
        :rtype: str
        """

        if record_num <= self.doorlock_logging_max_number_of_records:
            self.doorlock_logging_current_record_number = record_num

            key = ('Log Record', COMMAND_CLASS_DOOR_LOCK_LOGGING)
            try:
                return self[key].data
            except KeyError:
                return None
