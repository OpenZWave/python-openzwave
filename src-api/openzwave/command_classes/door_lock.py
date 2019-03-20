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

# Door Lock Command Class - Active
# Application
COMMAND_CLASS_DOOR_LOCK = 0x62


# noinspection PyAbstractClass
class DoorLock(CommandClassBase):
    """
    Door Lock Command Class

    symbol: `COMMAND_CLASS_DOOR_LOCK`
    """

    LOCKED_ADVANCED = [
        'Unsecure',
        'Unsecured with Timeout',
        'Inside Handle Unsecured',
        'Inside Handle Unsecured with Timeout',
        'Outside Handle Unsecured',
        'Outside Handle Unsecured with Timeout',
        'Secured'
    ]

    TIMEOUT_MODES = [
        'No Timeout',
        'Secure Lock after Timeout'
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_DOOR_LOCK]

    @property
    def locked(self):
        try:
            return self[('Locked', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    @locked.setter
    def locked(self, value):
        try:
            self[('Locked', COMMAND_CLASS_DOOR_LOCK)].data = value
        except KeyError:
            pass

    @property
    def locked_advanced(self):
        try:
            return self[('Locked (Advanced)', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    @locked_advanced.setter
    def locked_advanced(self, value):

        if isinstance(value, int):
            try:
                value = self.LOCKED_ADVANCED[value]
            except IndexError:
                return
        if value in self.LOCKED_ADVANCED:
            key = ('Locked (Advanced)', COMMAND_CLASS_DOOR_LOCK)
            try:
                self[key].data = value
            except KeyError:
                pass

    @property
    def outside_handle_control(self):
        key = ('Outside Handle Control', COMMAND_CLASS_DOOR_LOCK)
        try:
            return self[key].data
        except KeyError:
            return None

    @outside_handle_control.setter
    def outside_handle_control(self, value):
        key = ('Outside Handle Control', COMMAND_CLASS_DOOR_LOCK)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def inside_handle_control(self):
        key = ('Inside Handle Control', COMMAND_CLASS_DOOR_LOCK)
        try:
            return self[key].data
        except KeyError:
            return None

    @inside_handle_control.setter
    def inside_handle_control(self, value):
        key = ('Inside Handle Control', COMMAND_CLASS_DOOR_LOCK)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def timeout_mode(self):
        try:
            return self[('Timeout Mode', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    @timeout_mode.setter
    def timeout_mode(self, value):

        if isinstance(value, int):
            try:
                value = self.TIMEOUT_MODES[value]
            except IndexError:
                return
        if value in self.TIMEOUT_MODES:
            key = ('Timeout Mode', COMMAND_CLASS_DOOR_LOCK)
            try:
                self[key].data = value
            except KeyError:
                pass

    @property
    def timeout_minutes(self):
        try:
            return self[('Timeout Minutes', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    @timeout_minutes.setter
    def timeout_minutes(self, value):
        try:
            self[('Timeout Minutes', COMMAND_CLASS_DOOR_LOCK)].data = value
        except KeyError:
            pass

    @property
    def timeout_seconds(self):
        try:
            return self[('Timeout Seconds', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    @timeout_seconds.setter
    def timeout_seconds(self, value):
        try:
            self[('Timeout Seconds', COMMAND_CLASS_DOOR_LOCK)].data = value
        except KeyError:
            pass
