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

# Multilevel Toggle Switch Command Class - Depreciated
# Application
COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL = 0x29


# noinspection PyAbstractClass
class SwitchToggleMultilevel(CommandClassBase):

    def __init__(self):
        CommandClassBase.__init__(self)

        self._cls_ids += [COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL]

    def switch_toggle(self):
        key = ('Level', COMMAND_CLASS_SWITCH_TOGGLE_MULTILEVEL)
        try:
            value = self[key].data
            if value.data:
                value.data = 0
            else:
                value.data = 255
            return True
        except KeyError:
            return False


