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

# Configuration Command Class - Active
# Application
COMMAND_CLASS_CONFIGURATION = 0x70


# noinspection PyAbstractClass
class Configuration(CommandClassBase):
    """
    Configuration Command Class

    symbol: `COMMAND_CLASS_CONFIGURATION`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_CONFIGURATION]

    def get_configs(self, readonly='All', writeonly='All'):
        """
        Retrieve the list of configuration parameters.

        Filter rules are :
            command_class = 0x70
            genre = "Config"
            readonly = "All" (default) or as passed in arg

        :param readonly: whether to retrieve readonly configs
        :type readonly: bool, str
        :param writeonly: whether to retrieve writeonly configs
        :type writeonly: bool, str
        :return: a list of all configuration parameters
        :rtype: list
        """

        values = self[(None, COMMAND_CLASS_CONFIGURATION)]
        res = []

        for value in values:
            if value.genre != 'Config':
                continue

            if readonly == 'all':
                r_only = value.readonly
            else:
                r_only = readonly
            if writeonly == 'all':
                w_only = value.writeonly
            else:
                w_only = writeonly

            if value.readonly == r_only and value.writeonly == w_only:
                res += [value]

        return res

    def set_config(self, value_id, value):
        """
        Set config to value (using value value_id)

        :param value_id: The value to retrieve state
        :type value_id: int
        :param value: Appropriate value for given config
        :type value: any
        """

        try:
            self[(value_id, COMMAND_CLASS_CONFIGURATION)].data = value
            return True
        except (KeyError, IndexError):
            return False

    def get_config(self, value_id=None):
        """
        Set config to value (using value value_id)

        :param value_id: The value to retrieve data from. If None, retrieve the
        first value
        :type value_id: int
        :return: The level of this battery
        :rtype: int
        """

        if value_id is None:
            value_id = -1
        try:
            return self[(value_id, COMMAND_CLASS_CONFIGURATION)].data
        except (KeyError, IndexError):
            return None
