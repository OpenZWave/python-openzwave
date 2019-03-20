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

# Controller Replication Command Class - Active
# Application
COMMAND_CLASS_CONTROLLER_REPLICATION = 0x21


# noinspection PyAbstractClass
class ControllerReplication(CommandClassBase):
    """
    Controller Replication Command Class

    symbol: `COMMAND_CLASS_CONTROLLER_REPLICATION`
    """

    FUNCTIONS = [
        'Groups',
        'Group Names',
        'Scenes',
        'Scene Names',
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CONTROLLER_REPLICATION]

    @property
    def replication_node_id(self):
        try:
            return self[('Node', COMMAND_CLASS_CONTROLLER_REPLICATION)].data
        except KeyError:
            return None

    @replication_node_id.setter
    def replication_node_id(self, value):
        try:
            self[('Node', COMMAND_CLASS_CONTROLLER_REPLICATION)].data = value
        except KeyError:
            pass

    @property
    def functions(self):
        try:
            return (
                self[('Functions', COMMAND_CLASS_CONTROLLER_REPLICATION)].data
            )
        except KeyError:
            return None

    @functions.setter
    def functions(self, value):
        if isinstance(value, int):
            try:
                value = self.FUNCTIONS[value]
            except IndexError:
                return

        if value in self.FUNCTIONS:
            key = ('Functions', COMMAND_CLASS_CONTROLLER_REPLICATION)
            try:
                self[key].data = value
            except KeyError:
                pass

    @property
    def replicate(self):
        try:
            return (
                self[('Replicate', COMMAND_CLASS_CONTROLLER_REPLICATION)].data
            )
        except KeyError:
            return None

    @replicate.setter
    def replicate(self, value):
        try:
            self[('Replicate', COMMAND_CLASS_CONTROLLER_REPLICATION)].data = (
                value
            )
        except KeyError:
            pass
