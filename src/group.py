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
from openzwave.object import ZWaveException, ZwaveObject, NullLoggingHandler

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveGroup(ZwaveObject):
    '''
    The driver objet.
    Hold options of the manager
    Also used to retrieve informations about the library, ...
    '''

    def __init__(self, group_index, network=None, node_id=None):
        '''
        Initialize driver object

        :param devicePath: path to the ZWave Device
        :type devicePath: str
        :param userPath: path to user directory
        :type userPath: str
        :param config_path: path to the config path
        :type config_path: str
        :param options: options of the manager
        :type options: str

        '''

        super(ZWaveController, self).__init__(groupId, network)

        self._node_id = node_id
        self._index = group_index
        self._label = None
        self.cache_property(lambda: self.label)
        self._max_associations = list()
        self.cache_property(lambda: self.max_associations)
        self._members = list()
        self.cache_property(lambda: self.members)

    @property
    def index(self):
        """
        The index of the group.

        :rtype: int

        """
        return self._node

    @property
    def label(self):
        """
        The label of the group.

        :rtype: int

        """
        if self.is_outdated(lambda: self.label):
            self._label = self._network.manager.getGroupLabel(node._home_id, node._node_id, self.index)
            self.update(lambda: self.label)
        return self._label

    @property
    def max_associations(self):
        """
        The number of associations.

        :rtype: int

        """
        if self.is_outdated(lambda: self.max_associations):
            self._max_associations = self._network.manager.getMaxAssociations(node._home_id, node._node_id, self.index)
            self.update(lambda: self.max_associations)
        return self._max_associations

    @property
    def members(self):
        """
        The members of associations.

        :rtype: int

        """
        if self.is_outdated(lambda: self.members):
            self._members = self._network.manager.getAssociations(node._home_id, node._node_id, self.index)
            self.update(lambda: self.members)
        return self._members

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
        self._network.manager.addAssociation(node._home_id, node._node_id, self.index, target_node_id)
        self.outdate(lambda: self.members)
        self.outdate(lambda: self.max_associations)

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
        self._network.manager.removeAssociation(node._home_id, node._node_id, self.index, target_node_id)
        self.outdate(lambda: self.members)
        self.outdate(lambda: self.max_associations)
