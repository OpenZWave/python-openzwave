# -*- coding: utf-8 -*-
"""
.. module:: openzwave.group

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
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
from openzwave.object import ZWaveObject

# Set default logging handler to avoid "No handler found" warnings.
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass
logger = logging.getLogger('openzwave')
logger.addHandler(NullHandler())

class ZWaveGroup(ZWaveObject):
    """
    The driver object.
    Hold options of the manager
    Also used to retrieve information about the library, ...
    """

    def __init__(self, group_index, network=None, node_id=None):
        """
        Initialize driver object

        :param group_index: index of the group
        :type group_index: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        :param node_id: ID of node
        :type node_id: int

        """

        ZWaveObject.__init__(self, group_index, network)

        self._node_id = node_id
        self._index = group_index

    def __str__(self):
        """
        The string representation of the group.

        :rtype: str

        """
        return 'index: [%s] label: [%s]' % (self.index, self.label)

    @property
    def index(self):
        """
        The index of the group.

        :rtype: int

        """
        return self._index

    @property
    def label(self):
        """
        The label of the group.

        :rtype: int

        """
        return self._network.manager.getGroupLabel(self.home_id, self._node_id, self.index)

    @property
    def max_associations(self):
        """
        The number of associations.

        :rtype: int

        """
        return self._network.manager.getMaxAssociations(self.home_id, self._node_id, self.index)

    @property
    def associations(self):
        """
        The members of associations.

        :rtype: set()

        """
        return self._network.manager.getAssociations(self.home_id, self._node_id, self.index)

    @property
    def associations_instances(self):
        """
        The members of associations with theirs instances.
        Nodes that does not support multi-instances have an instanceid equal to 0.

        :rtype: set() of tuples (nodeid,instanceid)

        """
        return self._network.manager.getAssociationsInstances(self.home_id, self._node_id, self.index)

    def add_association(self, target_node_id, instance=0x00):
        """
        Adds a node to an association group.

        Due to the possibility of a device being asleep, the command is assumed to
        complete with success, and the association data held in this class is updated directly.  This
        will be reverted by a future Association message from the device if the Z-Wave
        message actually failed to get through.  Notification callbacks will be sent in
        both cases.

        :param target_node_id: Identifier for the node that will be added to the association group.
        :type target_node_id: int
        :param instance: The instance that will be added to the association group.
        :type instance: int

        """
        self._network.manager.addAssociation(self.home_id, self._node_id, self.index, target_node_id, instance)

    def remove_association(self, target_node_id, instance=0x00):
        """
        Removes a node from an association group.

        Due to the possibility of a device being asleep, the command is assumed to
        succeed, and the association data held in this class is updated directly.  This
        will be reverted by a future Association message from the device if the Z-Wave
        message actually failed to get through.   Notification callbacks will be sent
        in both cases.

        :param target_node_id: Identifier for the node that will be removed from the association group.
        :type target_node_id: int
        :param instance: The instance that will be added to the association group.
        :type instance: int

        """
        self._network.manager.removeAssociation(self._network.home_id, self._node_id, self.index, target_node_id, instance)

    def to_dict(self, extras=['all']):
        """
        Return a dict representation of the group.

        :param extras: The extra inforamtions to add
        :type extras: []
        :returns: A dict
        :rtype: dict()

        """
        if 'all' in extras:
            extras = ['associations']
        ret = {}
        ret['label'] = self.label
        if 'associations' in extras:
            ret['associations'] = dict.fromkeys(self.associations, 0)
        return ret
