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

    __replication_node_id_doc = """
        Replication Node Id (`property`)

        :param value: new node id
        :type value: int
        :return: node id or None if command failed
        :rtype: int, None
    """

    def __replication_node_id_get(self):
        try:
            return self[('Node', COMMAND_CLASS_CONTROLLER_REPLICATION)].data
        except KeyError:
            return None

    def __replication_node_id_set(self, value):
        try:
            self[('Node', COMMAND_CLASS_CONTROLLER_REPLICATION)].data = value
        except KeyError:
            pass

    replication_node_id = property(
        __replication_node_id_get,
        __replication_node_id_set,
        doc=__replication_node_id_doc
    )

    __replication_function_doc = """
        Replication Function (`property`)
        
        Values:
        <br><br\>
        * `'Groups'`
        * `'Group Names'`
        * `'Scenes'`
        * `'Scene Names'`
        * `None`

        :param value: function
        :type value: str
        :return: current function or None if command failed
        :rtype: str, None
    """

    def __replication_function_get(self):
        try:
            return (
                self[('Functions', COMMAND_CLASS_CONTROLLER_REPLICATION)].data
            )
        except KeyError:
            return None

    def __replication_function_set(self, value):
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

    replication_function = property(
        __replication_function_get,
        __replication_function_set,
        doc=__replication_function_doc
    )

    def replicate(self):
        """
        Replicate

        starts the replication process.

        :return: if command was successful `True`/`False`
        :rtype: bool
        """
        key = ('Replicate', COMMAND_CLASS_CONTROLLER_REPLICATION)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False


