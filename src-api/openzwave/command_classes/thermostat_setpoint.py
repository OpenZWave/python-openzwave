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
    def thermostat_setpoint(self):
        key = ('Setpoint', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            value = self[key]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_setpoint.setter
    def thermostat_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Setpoint'
            ):
                val.data = value

    @property
    def thermostat_away_heating_setpoint(self):
        key = ('Away Heating', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            value = self[key]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_away_heating_setpoint.setter
    def thermostat_away_heating_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Away Heating'
            ):
                val.data = value

    @property
    def thermostat_cooling_econ_setpoint(self):
        key = ('Cooling Econ', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            value = self[key]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_cooling_econ_setpoint.setter
    def thermostat_cooling_econ_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Cooling Econ'
            ):
                val.data = value

    @property
    def thermostat_heating_econ_setpoint(self):
        key = ('Heating Econ', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            value = self[key]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_heating_econ_setpoint.setter
    def thermostat_heating_econ_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Heating Econ'
            ):
                val.data = value

    @property
    def thermostat_auto_changeover_setpoint(self):
        key = ('Auto Changeover', COMMAND_CLASS_THERMOSTAT_SETPOINT)
        try:
            value = self[key]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_auto_changeover_setpoint.setter
    def thermostat_auto_changeover_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Auto Changeover'
            ):
                val.data = value

    @property
    def thermostat_moist_air_setpoint(self):
        try:
            value = self[('Moist Air', COMMAND_CLASS_THERMOSTAT_SETPOINT)]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_moist_air_setpoint.setter
    def thermostat_moist_air_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Moist Air'
            ):
                val.data = value

    @property
    def thermostat_dry_air_setpoint(self):
        try:
            value = self[('Dry Air', COMMAND_CLASS_THERMOSTAT_SETPOINT)]
            return [value.data, value.unit]

        except KeyError:
            return None

    @thermostat_dry_air_setpoint.setter
    def thermostat_dry_air_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Dry Air'
            ):
                val.data = value

    @property
    def thermostat_furnace_setpoint(self):
        try:
            value = self[('Furnace', COMMAND_CLASS_THERMOSTAT_SETPOINT)]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_furnace_setpoint.setter
    def thermostat_furnace_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Furnace'
            ):
                val.data = value

    @property
    def thermostat_heat_setpoint(self):
        try:
            value = self[('Heating 1', COMMAND_CLASS_THERMOSTAT_SETPOINT)]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_heat_setpoint.setter
    def thermostat_heat_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Heating 1'
            ):
                val.data = value

    @property
    def thermostat_cool_setpoint(self):
        try:
            value = self[('Cooling 1', COMMAND_CLASS_THERMOSTAT_SETPOINT)]
            return [value.data, value.unit]
        except KeyError:
            return None

    @thermostat_cool_setpoint.setter
    def thermostat_cool_setpoint(self, value):
        for val in self.values.values():
            if (
                val == COMMAND_CLASS_THERMOSTAT_SETPOINT and
                val.label == 'Cooling 1'
            ):
                val.data = value

    @property
    def thermostat_setpoint_unit(self):
        values = [
            'Heating 1',
            'Cooling 1',
            'Furnace',
            'Dry Air',
            'Moist Air',
            'Auto Changeover',
            'Heating Econ',
            'Cooling Econ',
            'Away Heating'
        ]

        for value in values:
            try:
                return self[(value, COMMAND_CLASS_THERMOSTAT_SETPOINT)].unit
            except KeyError:
                pass

    @thermostat_setpoint_unit.setter
    def thermostat_setpoint_unit(self, value):
        values = [
            'Heating 1',
            'Cooling 1',
            'Furnace',
            'Dry Air',
            'Moist Air',
            'Auto Changeover',
            'Heating Econ',
            'Cooling Econ',
            'Away Heating'
        ]

        for val in values:
            try:
                self[(val, COMMAND_CLASS_THERMOSTAT_SETPOINT)].unit = value
            except KeyError:
                pass



