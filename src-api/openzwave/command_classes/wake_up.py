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

# Wake Up Command Class - Active
# Management
COMMAND_CLASS_WAKE_UP = 0x84


# noinspection PyAbstractClass
class WakeUp(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_WAKE_UP]

    @property
    def wakeup_interval_min(self):
        key = ('Minimum Wake-up Interval', COMMAND_CLASS_WAKE_UP)
        try:
            return self[key].data
        except KeyError:
            return None

    @wakeup_interval_min.setter
    def wakeup_interval_min(self, value):
        key = ('Minimum Wake-up Interval', COMMAND_CLASS_WAKE_UP)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def wakeup_interval_max(self):
        key = ('Maximum Wake-up Interval', COMMAND_CLASS_WAKE_UP)
        try:
            return self[key].data
        except KeyError:
            return None

    @wakeup_interval_max.setter
    def wakeup_interval_max(self, value):
        key = ('Maximum Wake-up Interval', COMMAND_CLASS_WAKE_UP)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def wakeup_interval_default(self):
        key = ('Default Wake-up Interval', COMMAND_CLASS_WAKE_UP)
        try:
            return self[key].data
        except KeyError:
            return None

    @wakeup_interval_default.setter
    def wakeup_interval_default(self, value):
        key = ('Default Wake-up Interval', COMMAND_CLASS_WAKE_UP)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def wakeup_interval_step(self):
        key = ('Wake-up Interval Step', COMMAND_CLASS_WAKE_UP)
        try:
            return self[key].data
        except KeyError:
            return None

    @wakeup_interval_step.setter
    def wakeup_interval_step(self, value):
        key = ('Wake-up Interval Step', COMMAND_CLASS_WAKE_UP)
        try:
            self[key].data = value
        except KeyError:
            pass

