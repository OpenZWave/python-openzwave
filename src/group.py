# -*- coding: utf-8 -*-
"""
.. module:: openzwave.group

This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: bibi21000 aka Sébastien GALLET <bibi21000@gmail.com>

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
from collections import namedtuple
import thread
import os
import time
from louie import dispatcher, All
import logging
import libopenzwave
import openzwave
from openzwave.object import ZWaveException, ZWaveObject, NullLoggingHandler

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveGroup(ZWaveObject):
    '''
    The driver objet.
    Hold options of the manager
    Also used to retrieve informations about the library, ...
    '''

    def __init__(self, group_index, network=None, node_id=None):
        '''
        Initialize driver object

        :param group_index: index of the group
        :type group_index: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        :param node_id: ID of node
        :type node_id: int

        '''

        ZWaveObject.__init__(self, group_index, network)

        self._node_id = node_id
        self._index = group_index
        self._label = None
        self.cache_property("self.label")
        self._max_associations = set()
        self.cache_property("self.max_associations")
        #self._members = set()
        #self.cache_property("self.members")
        self._associations = set()
        self.cache_property("self.associations")

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
        if self.is_outdated("self.label"):
            self._label = self._network.manager.getGroupLabel(self.home_id, self._node_id, self.index)
            self.update("self.label")
        return self._label

    @property
    def max_associations(self):
        """
        The number of associations.

        :rtype: int

        """
        if self.is_outdated("self.max_associations"):
            self._max_associations = self._network.manager.getMaxAssociations(self.home_id, self._node_id, self.index)
            self.update("self.max_associations")
        return self._max_associations

#    @property
#    def members(self):
#        """
#        The members of associations.
#
#        :rtype: int
#
#        """
#        if self.is_outdated("self.members"):
#            self._members = self._network.manager.getAssociations(self.home_id, self._node_id, self.index)
#            self.update("self.members")
#        return self._members

    @property
    def associations(self):
        """
        The members of associations.

        :rtype: set()

        """
        if self.is_outdated("self.associations"):
            self._associations = self._network.manager.getAssociations(self.home_id, self._node_id, self.index)
            self.update("self.associations")
        return self._associations

    def addAssociation(self, target_node_id):
        """
        Adds a node to an association group.

        Due to the possibility of a device being asleep, the command is assumed to
        suceeed, and the association data held in this class is updated directly.  This
        will be reverted by a future Association message from the device if the Z-Wave
        message actually failed to get through.  Notification callbacks will be sent in
        both cases.

        :param target_node_id: Identifier for the node that will be added to the association group.
        :type target_node_id: int

        """
        self._network.manager.addAssociation(self.home_id, self._node_id, self.index, target_node_id)
        self.outdate("self.associations")
        self.outdate("self.max_associations")

    def removeAssociation(self, target_node_id):
        """
        Removes a node from an association group.

        Due to the possibility of a device being asleep, the command is assumed to
        succeed, and the association data held in this class is updated directly.  This
        will be reverted by a future Association message from the device if the Z-Wave
        message actually failed to get through.   Notification callbacks will be sent
        in both cases.

        :param target_node_id: Identifier for the node that will be removed from the association group.
        :type target_node_id: int

        """
        self._network.manager.removeAssociation(self._home_id, self._node_id, self.index, target_node_id)
        self.outdate("self.associations")
        self.outdate("self.max_associations")
