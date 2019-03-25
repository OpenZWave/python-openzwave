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

from ..group import ZWaveGroup
from .command_class_base import CommandClassBase

# Association Command Class - Active
# Management
COMMAND_CLASS_ASSOCIATION = 0x85


# noinspection PyAbstractClass
class Association(CommandClassBase):
    """
    Association Command Class

    symbol: `COMMAND_CLASS_ASSOCIATION`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += [COMMAND_CLASS_ASSOCIATION]

    @property
    def num_groups(self):
        """
        Gets the number of association groups reported by this node.

        :rtype: int

        """
        return self.network.manager.getNumGroups(self.home_id, self.id)

    @property
    def groups(self):
        """
        Get the association groups reported by this node

        In Z-Wave, groups are numbered starting from one.  For example, if a call to
        GetNumGroups returns 4, the _groupIdx value to use in calls to GetAssociations
        AddAssociation and RemoveAssociation will be a number between 1 and 4.

        :rtype: dict()

        """
        groups = dict()
        groups_added = 0
        i = 1
        while groups_added < self.num_groups and i < 256:
            if self.get_max_associations(i) > 0:
                groups[i] = ZWaveGroup(
                    i,
                    network=self.network,
                    node_id=self.id
                )
                groups_added += 1
            i += 1
        return groups

    def groups_to_dict(self, extras=['all']):
        """
        Return a dict representation of the groups.

        :param extras: The extra inforamtions to add
        :type extras: []
        :returns: A dict
        :rtype: dict()

        """
        groups = self.groups
        ret = {}
        for gid in groups.keys():
            ret[gid] = groups[gid].to_dict(extras=extras)
        return ret

    def get_max_associations(self, groupidx):
        """
        Gets the maximum number of associations for a group.

        :param groupidx: The group to query
        :type groupidx: int
        :rtype: int

        """

        return self.network.manager.getMaxAssociations(
            self.home_id,
            self.id,
            groupidx
        )
