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

# Thermostat Setpoint Command Class - Active
# Application
COMMAND_CLASS_THERMOSTAT_SETPOINT = 0x43


# noinspection PyAbstractClass
class ThermostatSetpoint(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_THERMOSTAT_SETPOINT]

    @property
    def away_heating(self):
        key = ('Away Heating', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            return self[key].data
        except KeyError:
            return None

    @away_heating.setter
    def away_heating(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Away Heating'
            ):
                val.data = value

    @property
    def cooling_econ(self):
        key = ('Cooling Econ', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            return self[key].data
        except KeyError:
            return None

    @cooling_econ.setter
    def cooling_econ(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Cooling Econ'
            ):
                val.data = value

    @property
    def heating_econ(self):
        key = ('Heating Econ', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            return self[key].data
        except KeyError:
            return None

    @heating_econ.setter
    def heating_econ(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Heating Econ'
            ):
                val.data = value

    @property
    def auto_changeover(self):
        key = ('Auto Changeover', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            return self[key].data
        except KeyError:
            return None

    @auto_changeover.setter
    def auto_changeover(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Auto Changeover'
            ):
                val.data = value

    @property
    def moist_air(self):
        try:
            return self[('Moist Air', COMMAND_CLASS_THERMOSTAT_SETPOINT)].data
        except KeyError:
            return None

    @moist_air.setter
    def moist_air(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Moist Air'
            ):
                val.data = value

    @property
    def dry_air(self):
        try:
            return self[('Dry Air', COMMAND_CLASS_THERMOSTAT_SETPOINT)].data
        except KeyError:
            return None

    @dry_air.setter
    def dry_air(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Dry Air'
            ):
                val.data = value

    @property
    def furnace(self):
        try:
            return self[('Furnace', COMMAND_CLASS_THERMOSTAT_SETPOINT)].data
        except KeyError:
            return None

    @furnace.setter
    def furnace(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Furnace'
            ):
                val.data = value

    @property
    def heat(self):
        try:
            return self[('Heating 1', COMMAND_CLASS_THERMOSTAT_SETPOINT)].data
        except KeyError:
            return None

    @heat.setter
    def heat(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Heating 1'
            ):
                val.data = value

    @property
    def cool(self):
        try:
            return self[('Cooling 1', COMMAND_CLASS_THERMOSTAT_SETPOINT)].data
        except KeyError:
            return None

    @cool.setter
    def cool(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Cooling 1'
            ):
                val.data = value

