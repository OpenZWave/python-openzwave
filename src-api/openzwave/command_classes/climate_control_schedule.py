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

# Climate Control Schedule Command Class - Depreciated
# Application
COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE = 0x46


# noinspection PyAbstractClass
class ClimateControlSchedule(CommandClassBase):
    """
    Climate Control Schedule Command Class

    symbol: `COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE`
    """

    OVERRIDES = [
        None,
        'Temporary',
        'Permanent',
        None
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE]

    @property
    def monday(self):
        key = ('Monday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @monday.setter
    def monday(self, value):
        key = ('Monday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def tuesday(self):
        key = ('Tuesday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @tuesday.setter
    def tuesday(self, value):
        key = ('Tuesday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def wednesday(self):
        key = ('Wednesday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @wednesday.setter
    def wednesday(self, value):
        key = ('Wednesday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def thursday(self):
        key = ('Thursday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @thursday.setter
    def thursday(self, value):
        key = ('Thursday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def friday(self):
        key = ('Friday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @friday.setter
    def friday(self, value):
        key = ('Friday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def saturday(self):
        key = ('Saturday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @saturday.setter
    def saturday(self, value):
        key = ('Saturday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def sunday(self):
        key = ('Sunday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @sunday.setter
    def sunday(self, value):
        key = ('Sunday', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def override_state(self):
        key = ('Override State', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @override_state.setter
    def override_state(self, value):
        key = ('Override State', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)

        if isinstance(value, int):
            try:
                value = self.OVERRIDES[value]
            except IndexError:
                return

        if value in self.OVERRIDES:
            try:
                self[key].data = value
            except KeyError:
                pass

    @property
    def override_setback(self):
        key = ('Override Setback', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            return self[key].data
        except KeyError:
            return None

    @override_setback.setter
    def override_setback(self, value):
        key = ('Override Setback', COMMAND_CLASS_CLIMATE_CONTROL_SCHEDULE)
        try:
            self[key].data = value
        except KeyError:
            pass
