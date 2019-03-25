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

# Powerlevel Command Class - Active
# Network-Protocol
COMMAND_CLASS_POWERLEVEL = 0x73


# noinspection PyAbstractClass
class Powerlevel(CommandClassBase):

    POWER_LEVEL = [
        'Normal',
        '-1dB',
        '-2dB',
        '-3dB',
        '-4dB',
        '-5dB',
        '-6dB',
        '-7dB',
        '-8dB',
        '-9dB',
        'Unknown'
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_POWERLEVEL]

    __power_level_doc = """
        Power Level (`property`)
        
        Values:
        <br></br>
        * `'Normal'`
        * `'-1dB'`
        * `'-2dB'`
        * `'-3dB'`
        * `'-4dB'`
        * `'-5dB'`
        * `'-6dB'`
        * `'-7dB'`
        * `'-8dB'`
        * `'-9dB'`
        * `'Unknown'`
        * `None``
        
        :param value: level
        :type value: int, str
        :return: level or None if command failed
        :rtype: str, None
    """

    def __power_level_get(self):
        key = ('Powerlevel', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __power_level_set(self, value):
        if isinstance(value, int):
            try:
                value = self.POWER_LEVEL[value]
            except IndexError:
                return

        if value in self.POWER_LEVEL:

            key = ('Powerlevel', COMMAND_CLASS_POWERLEVEL)
            try:
                self[key].data = value
            except KeyError:
                pass

    power_level = property(
        __power_level_get,
        __power_level_set,
        doc=__power_level_doc
    )

    __power_level_timeout_doc = """
        Power Level Timeout (`property`)

        :param value: timeout
        :type value: int
        :return: timeout or None if command failed
        :rtype: int, None
    """

    def __power_level_timeout_get(self):
        key = ('Timeout', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __power_level_timeout_set(self, value):
        key = ('Timeout', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    power_level_timeout = property(
        __power_level_timeout_get,
        __power_level_timeout_set,
        doc=__power_level_timeout_doc
    )

    __power_level_test_node_doc = """
        Power Level Test Node (`property`)

        :param value: node id
        :type value: int
        :return: node id or None if command failed
        :rtype: int, None
    """

    def __power_level_test_node_get(self):
        key = ('Test Node', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __power_level_test_node_set(self, value):
        key = ('Test Node', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    power_level_test_node = property(
        __power_level_test_node_get,
        __power_level_test_node_set,
        doc=__power_level_test_node_doc
    )

    __power_level_test_doc = """
        Power Level Test (`property`)
        
        Values:
        <br></br>
        * `'Normal'`
        * `'-1dB'`
        * `'-2dB'`
        * `'-3dB'`
        * `'-4dB'`
        * `'-5dB'`
        * `'-6dB'`
        * `'-7dB'`
        * `'-8dB'`
        * `'-9dB'`
        * `'Unknown'`
        * `None``
        
        :param value: level
        :type value: int, str
        :return: level or None if command failed
        :rtype: str, None
    """

    def __power_level_test_get(self):
        key = ('Test Powerlevel', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def __power_level_test_set(self, value):

        if isinstance(value, int):
            try:
                value = self.POWER_LEVEL[value]
            except IndexError:
                return

        if value in self.POWER_LEVEL:

            key = ('Test Powerlevel', COMMAND_CLASS_POWERLEVEL)
            try:
                self[key].data = value
            except KeyError:
                pass

    power_level_test = property(
        __power_level_test_get,
        __power_level_test_set,
        doc=__power_level_test_doc
    )

    @property
    def power_level_frame_count(self):
        """
        Power Level Frame Count (`property`)

        :return: number of frames or None if command failed
        :rtype: int, None
        """
        key = ('Frame Count', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def power_level_acked_frames(self):
        """
        Power Level Acknowledged Frames (`property`)

        :return: number of frames or None if command failed
        :rtype: int, None
        """
        key = ('Acked Frames', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def power_level_test_results(self):
        """
        Power Level Test Results (`property`)

        Values:
        <br></br>
        * `'Failed'`
        * `'Success'`
        * `'In Progress'`
        * `'Unknown'`

        :return: test status or None if command failed
        :rtype: str, None
        """
        key = ('Test Status', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def power_level_save(self):
        """
        Power Level Save

        :return: command successful `True`/`False`
        :rtype: bool
        """
        key = ('Set Powerlevel', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def power_level_start_test(self):
        """
        Power Level Start Test

        :return: command successful `True`/`False`
        :rtype: bool
        """
        key = ('Test', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def power_level_report(self):
        """
        Power Level Report

        :return: command successful `True`/`False`
        :rtype: bool
        """
        key = ('Report', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False


