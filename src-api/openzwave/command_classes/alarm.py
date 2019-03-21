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

# Alarm Command Class - Depreciated
# Application
# Alarm has been renamed/overloaded by the Notification Command Class
COMMAND_CLASS_ALARM = 0x71


# noinspection PyAbstractClass
class Alarm(CommandClassBase):

    """
    Alarm Command Class

    symbol: `COMMAND_CLASS_ALARM`
    """

    ALARM_TYPES = [
        'General',
        'Smoke',
        'Carbon Monoxide',
        'Carbon Dioxide',
        'Heat',
        'Flood',
        'Access Control',
        'Burglar',
        'Power Management',
        'System',
        'Emergency',
        'Clock',
        'Appliance',
        'HomeHealth'
    ]

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ALARM]

    @property
    def alarm_source_node(self):
        """
        The device type

        This property will return the type of device.
        Possible returned values are:
        <br></br>
        * 'General'
        * 'Smoke'
        * 'Carbon Monoxide'
        * 'Carbon Dioxide'
        * 'Heat'
        * 'Flood'
        * 'Access Control'
        * 'Burglar'
        * 'Power Management'
        * 'System'
        * 'Emergency'
        * 'Clock'
        * 'Appliance'
        * 'HomeHealth'

        :return: device type
        :rtype: str
        """

        try:
            value = self[('SourceNodeId', COMMAND_CLASS_ALARM)]
        except KeyError:
            return None

        return self._network.nodes[value.data]

    @property
    def alarm_type(self):
        """
        Alarm Type

        :return: alarm type
        """

        try:
            alarm_type = self[('Alarm Type', COMMAND_CLASS_ALARM)].data
        except KeyError:
            return None

        for value in self[(None, COMMAND_CLASS_ALARM)]:
            if (
                value.label in self.ALARM_TYPES and
                value.data == alarm_type
            ):
                return value.label

        return None

    @property
    def alarm_level(self):
        """
        Alarm level

        :return: alarm level
        """
        try:
            return self[('Alarm Level', COMMAND_CLASS_ALARM)].data
        except KeyError:
            return None

