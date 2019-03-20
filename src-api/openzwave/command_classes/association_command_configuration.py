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

# Association Command Configuration Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION = 0x9B


# noinspection PyAbstractClass
class AssociationCommandConfiguration(CommandClassBase):
    """
    Association Command Configuration Command Class

    symbol: `COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION`
    """
    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION]

    @property
    def max_command_length(self):
        key = (
            'Max Command Length',
            COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION
        )
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def commands_are_values(self):
        key = (
            'Commands are Values',
            COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION
        )
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def commands_are_configurable(self):
        key = (
            'Commands are Configurable',
            COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION
        )
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def free_commands(self):
        key = (
            'Free Commands',
            COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION
        )
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def max_commands(self):
        key = (
            'Max Commands',
            COMMAND_CLASS_ASSOCIATION_COMMAND_CONFIGURATION
        )
        try:
            return self[key].data
        except KeyError:
            return None
