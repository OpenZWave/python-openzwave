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

    def __init__(self, groupIndex, network=None, nodeId=None):
        '''
        Initialize driver object

        :param devicePath: path to the ZWave Device
        :type devicePath: str
        :param userPath: path to user directory
        :type userPath: str
        :param configPath: path to the config path
        :type configPath: str
        :param options: options of the manager
        :type options: str
        '''

        super(ZWaveController, self).__init__(groupId, network)

        self._nodeId = nodeId
        self._index = groupIndex
        self._label = None
        self.cacheProperty(lambda: self.label)
        self._maxAssociations = list()
        self.cacheProperty(lambda: self.maxAssociations)
        self._members = list()
        self.cacheProperty(lambda: self.members)

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
        if self.isOutdated(lambda: self.label):
            self._label = self._network.manager.getGroupLabel(node._homeId, node._nodeId, self.index)
            self.update(lambda: self.label)
        return self._label

    @property
    def maxAssociations(self):
        """
        The number of associations.
        :rtype: int
        """
        if self.isOutdated(lambda: self.maxAssociations):
            self._maxAssociations = self._network.manager.getMaxAssociations(node._homeId, node._nodeId, self.index)
            self.update(lambda: self.maxAssociations)
        return self._maxAssociations

    @property
    def members(self):
        """
        The members of associations.
        :rtype: int
        """
        if self.isOutdated(lambda: self.members):
            self._members = self._network.manager.getAssociations(node._homeId, node._nodeId, self.index)
            self.update(lambda: self.members)
        return self._members

    def addAssociation(self, targetNodeId):
        """
        The members of associations.
        :rtype: int
        """
        self._network.manager.addAssociation(node._homeId, node._nodeId, self.index, targetNodeId)
        self.outdate(lambda: self.members)
        self.outdate(lambda: self.maxAssociations)

    def removeAssociation(self, targetNodeId):
        """
        The members of associations.
        :rtype: int
        """
        self._network.manager.removeAssociation(node._homeId, node._nodeId, self.index, targetNodeId)
        self.outdate(lambda: self.members)
        self.outdate(lambda: self.maxAssociations)
