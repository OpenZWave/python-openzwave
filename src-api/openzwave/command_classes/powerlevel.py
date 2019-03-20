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

# Powerlevel Command Class - Active
# Network-Protocol
COMMAND_CLASS_POWERLEVEL = 0x73


# noinspection PyAbstractClass
class Powerlevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_POWERLEVEL]

    @property
    def power_level(self):
        key = ('Powerlevel', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @power_level.setter
    def power_level(self, value):
        key = ('Powerlevel', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def power_level_timeout(self):
        key = ('Timeout', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @power_level_timeout.setter
    def power_level_timeout(self, value):
        key = ('Timeout', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def power_level_test_node(self):
        key = ('Test Node', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @power_level_test_node.setter
    def power_level_test_node(self, value):
        key = ('Test Node', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def power_level_test(self):
        key = ('Test Powerlevel', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @power_level_test.setter
    def power_level_test(self, value):
        key = ('Test Powerlevel', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def power_level_frame_count(self):
        key = ('Frame Count', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @power_level_frame_count.setter
    def power_level_frame_count(self, value):
        key = ('Frame Count', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = value
        except KeyError:
            pass

    @property
    def power_level_acked_frames(self):
        key = ('Acked Frames', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def power_level_test_results(self):
        key = ('Test Status', COMMAND_CLASS_POWERLEVEL)
        try:
            return self[key].data
        except KeyError:
            return None

    def power_level_save(self):
        key = ('Set Powerlevel', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def power_level_start_test(self):
        key = ('Test', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    def power_level_reeport(self):
        key = ('Report', COMMAND_CLASS_POWERLEVEL)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False


