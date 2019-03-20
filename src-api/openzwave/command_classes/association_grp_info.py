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

# Association Group Information (AGI) Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION_GRP_INFO = 0x59


# noinspection PyAbstractClass
class AssociationGrpInfo(CommandClassBase):
    """
    Association Group Info Command Class

    symbol: `COMMAND_CLASS_ASSOCIATION_GRP_INFO`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ASSOCIATION_GRP_INFO]

    @property
    def groups(self):
        """
        Groups

        :return: groups

        """
        return self.groups()

    def groups_to_dict(self, extras=('all',)):
        """
        Groups to a python dictionary

        :param extras: extra group fields to add to the dictionary
        :type extras: tuple of str
        :return: dictionary of groups
        :rtype: dict
        """
        return self.groups_to_dict(extras)
