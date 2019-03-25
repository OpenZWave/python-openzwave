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

    __doorlock_locked_doc = """
        Door Lock Locked (`property`)

        :param value: locked state `True`/`False`
        :type value: bool
        :return: locked state `True`/`False` or None if command failed
        :rtype: bool, None
    """

    def __doorlock_locked_get(self):
        try:
            return self[('Locked', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    def __doorlock_locked_set(self, value):
        try:
            self[('Locked', COMMAND_CLASS_DOOR_LOCK)].data = value
        except KeyError:
            pass

    doorlock_locked = property(
        __doorlock_locked_get,
        __doorlock_locked_set,
        doc=__doorlock_locked_doc
    )

    __doorlock_locked_advanced_doc = """
        Door Lock Locked (Advanced) (`property`)
        
        Values:
        <br></br>
        * `'Unsecure'`
        * `'Unsecured with Timeout'`
        * `'Inside Handle Unsecured'`
        * `'Inside Handle Unsecured with Timeout'`
        * `'Outside Handle Unsecured'`
        * `'Outside Handle Unsecured with Timeout'`
        * `'Secured'`
        * `None`
        

        :param value: locked state
        :type value: str
        :return: locked state or None if command failed
        :rtype: str, None
    """

    def __doorlock_locked_advanced_get(self):
        try:
            return self[('Locked (Advanced)', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    def __doorlock_locked_advanced_set(self, value):

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

    doorlock_locked_advanced = property(
        __doorlock_locked_advanced_get,
        __doorlock_locked_advanced_set,
        doc=__doorlock_locked_advanced_doc
    )

    __doorlock_outside_handle_control_doc = """
        Outside Handle Control (`property`)
        
        Controls if the outside handle functions or not.

        :param value: handle state `True`/`False`
        :type value: bool
        :return: handle state `True`/`False` or None if command failed
        :rtype: bool, None
    """

    def __doorlock_outside_handle_control_get(self):
        key = ('Outside Handle Control', COMMAND_CLASS_DOOR_LOCK)
        try:
            return bool(self[key].data)
        except KeyError:
            return None

    def __doorlock_outside_handle_control_set(self, value):
        key = ('Outside Handle Control', COMMAND_CLASS_DOOR_LOCK)
        try:
            self[key].data = int(value)
        except KeyError:
            pass

    doorlock_outside_handle_control = property(
        __doorlock_outside_handle_control_get,
        __doorlock_outside_handle_control_set,
        doc=__doorlock_outside_handle_control_doc
    )

    __doorlock_inside_handle_control_doc = """
        Inside Handle Control (`property`)
        
        Controls if the inside handle functions or not.

        :param value: handle state `True`/`False`
        :type value: bool
        :return: handle state `True`/`False` or None if command failed
        :rtype: bool, None
    """

    def __doorlock_inside_handle_control_get(self):
        key = ('Inside Handle Control', COMMAND_CLASS_DOOR_LOCK)
        try:
            return bool(self[key].data)
        except KeyError:
            return None

    def __doorlock_inside_handle_control_set(self, value):
        key = ('Inside Handle Control', COMMAND_CLASS_DOOR_LOCK)
        try:
            self[key].data = bool(value)
        except KeyError:
            pass

    doorlock_inside_handle_control = property(
        __doorlock_inside_handle_control_get,
        __doorlock_inside_handle_control_set,
        doc=__doorlock_inside_handle_control_doc
    )

    __doorlock_timeout_mode_doc = """
        Door Lock Timeout Mode (`property`)
        
        Values:
        <br></br>
        * `'No Timeout'`
        * `'Secure Lock after Timeout'`
        * `None`
        
        :param value: timeout mode
        :type value: str
        :return: timeout mode or None if command failed
        :rtype: str, None
    """

    def __doorlock_timeout_mode_get(self):
        try:
            return self[('Timeout Mode', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    def __doorlock_timeout_mode_set(self, value):

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

    doorlock_timeout_mode = property(
        __doorlock_timeout_mode_get,
        __doorlock_timeout_mode_set,
        doc=__doorlock_timeout_mode_doc
    )

    __doorlock_timeout_minutes_doc = """
        Door Lock Timeout Minutes (`property`)

        :param value: minutes
        :type value: int
        :return: miniutes or None if command failed
        :rtype: int, None
    """

    def __doorlock_timeout_minutes_get(self):
        try:
            return self[('Timeout Minutes', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    def __doorlock_timeout_minutes_set(self, value):
        try:
            self[('Timeout Minutes', COMMAND_CLASS_DOOR_LOCK)].data = value
        except KeyError:
            pass

    doorlock_timeout_minutes = property(
        __doorlock_timeout_minutes_get,
        __doorlock_timeout_minutes_set,
        doc=__doorlock_timeout_minutes_doc
    )

    __doorlock_timeout_seconds_doc = """
        Door Lock Timeout Seconds (`property`)

        :param value: seconds
        :type value: int
        :return: seconds or None if command failed
        :rtype: int, None
    """

    def __doorlock_timeout_seconds_get(self):
        try:
            return self[('Timeout Seconds', COMMAND_CLASS_DOOR_LOCK)].data
        except KeyError:
            return None

    def __doorlock_timeout_seconds_set(self, value):
        try:
            self[('Timeout Seconds', COMMAND_CLASS_DOOR_LOCK)].data = value
        except KeyError:
            pass

    doorlock_timeout_seconds = property(
        __doorlock_timeout_seconds_get,
        __doorlock_timeout_seconds_set,
        doc=__doorlock_timeout_seconds_doc
    )
