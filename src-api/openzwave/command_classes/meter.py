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

# Meter Command Class - Active
# Application
COMMAND_CLASS_METER = 0x32


# noinspection PyAbstractClass
class Meter(CommandClassBase):
    """
    Meter Command Class

    symbol: `COMMAND_CLASS_METER`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_METER]

    def meter_reset(self):
        """
        Reset Meter

        Resets meter to 0

        :return: command send successfully `True`\`False`
        :rtype: bool
        """
        key = ('Reset', COMMAND_CLASS_METER)
        try:
            self[key].data = True
            return True
        except KeyError:
            return False

    @property
    def meter_gas(self):
        """
        Gas Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Gas', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return value.data, value.units
        except KeyError:
            return None

    @property
    def meter_water(self):
        """
        Water Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Water', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return [value.data, value.units]
        except KeyError:
            return None

    @property
    def meter_exporting(self):
        """
        Gas Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Exporting', COMMAND_CLASS_METER)
        try:
            return self[key].data
        except KeyError:
            return None

    @property
    def meter_energy(self):
        """
        Energy Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Energy', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return [value.data, value.units]
        except KeyError:
            return None

    @property
    def meter_power(self):
        """
        Power Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Power', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return [value.data, value.units]
        except KeyError:
            return None

    @property
    def meter_count(self):
        """
        Count Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Count', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return [value.data, value.units]
        except KeyError:
            return None

    @property
    def meter_voltage(self):
        """
        Voltage Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Voltage', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return [value.data, value.units]
        except KeyError:
            return None

    @property
    def meter_amperage(self):
        """
        Amperage Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Current', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return [value.data, value.units]
        except KeyError:
            return None

    @property
    def meter_power_factor(self):
        """
        Power Factor Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Power Factor', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return [value.data, value.units]
        except KeyError:
            return None

    @property
    def meter_previous_reading(self):
        """
        Previous Reading (`property`)

        :return: (reading, unit of measure) or None if command
        not successful
        :rtype: (float, str) or None
        """
        key = ('Previous Reading', COMMAND_CLASS_METER)
        try:
            value = self[key]
            return [value.data, value.units]
        except KeyError:
            return None

    @property
    def meter_reading_interval(self):
        """
        Gas Reading (`property`)

        :return: interval or None if command not successful
        :rtype: int, None
        """
        key = ('Interval', COMMAND_CLASS_METER)
        try:
            return self[key].data
        except KeyError:
            return None
