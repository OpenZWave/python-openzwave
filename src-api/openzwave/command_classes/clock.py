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

# Clock Command Class - Active
# Application
COMMAND_CLASS_CLOCK = 0x81


# noinspection PyAbstractClass
class Clock(CommandClassBase):
    """
    Clock Command Class

    symbol: `COMMAND_CLASS_CLOCK`
    """

    DAYS = [
        None,
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CLOCK]

    __clock_hour_doc = """
        Clock Hour (`property`)

        :param value: new clock hour
        :type value: int
        :return: hour the node is set to or None if command failed
        :rtype: int, None
    """

    def __clock_hour_get(self):
        try:
            return self[('Hour', COMMAND_CLASS_CLOCK)].data
        except KeyError:
            return None

    def __clock_hour_set(self, value):
        try:
            self[('Hour', COMMAND_CLASS_CLOCK)].data = value
        except KeyError:
            pass

    clock_hour = property(
        __clock_hour_get,
        __clock_hour_set,
        doc=__clock_hour_doc
    )

    __clock_day_doc = """
        Clock Day (`property`)
        
        Values:
        
        * `'Monday'`
        * `'Tuesday'`
        * `'Wednesday'`
        * `'Thursday'`
        * `'Friday'`
        * `'Saturday'`
        * `'Sunday'`

        :param value: new clock day
        :type value: str
        :return:  day the node is set to or None if command failed
        :rtype: str, None
    """

    def __clock_day_get(self):
        try:
            return self[('Day', COMMAND_CLASS_CLOCK)].data
        except KeyError:
            return None

    def __clock_day_set(self, value):
        if isinstance(value, int):
            try:
                value = self.DAYS[value]
            except IndexError:
                return

        if value in self.DAYS:
            try:
                self[('Day', COMMAND_CLASS_CLOCK)].data = value
            except KeyError:
                pass

    clock_day = property(
        __clock_day_get,
        __clock_day_set,
        doc=__clock_day_doc
    )

    __clock_minute_doc = """
        Clock Minute (`property`)

        :param value: new clock minute
        :type value: int
        :return: minute the node is set to or None if command failed
        :rtype: int, None
    """

    def __clock_minute_get(self):
        try:
            return self[('Minute', COMMAND_CLASS_CLOCK)].data
        except KeyError:
            return None

    def __clock_minute_set(self, value):
        try:
            self[('Minute', COMMAND_CLASS_CLOCK)].data = value
        except KeyError:
            pass

    clock_minute = property(
        __clock_minute_get,
        __clock_minute_set,
        doc=__clock_minute_doc
    )
