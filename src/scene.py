# -*- coding: utf-8 -*-
"""
.. module:: openzwave.scene

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

import libopenzwave
from collections import namedtuple
import thread
import time
import openzwave
import logging
from openzwave.object import ZwaveObject

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveScene(ZwaveObject):
    '''
    Represents a single scene within the Z-Wave Network
    '''

    def __init__(self, sceneId, network=None):
        '''
        Initialize zwave scene

        :param sceneId: ID of the scene
        :type sceneId: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        '''
        self.objectId = sceneId
        self.logDebug("Create object scene (sceneId:%s)" % (sceneId))
        self._values = dict()
        self._label = ''
        super(ZWaveScene, self).__init__(sceneId, network)

    @property
    def label(self):
        """
        The label of the scene.
        """
        return self._label

    @property
    def values(self):
        """
        The values used in the scene.
        """
        if self.outdated :
            self.refresh()
        return self._values

    def create(self, name):
        '''
        Create a new zwave scene and update the objectId field
        '''
        self._sceneId = sceneId
        self._name = ''

    def addValue(self, valueid, valueData):
        '''
        Add a value to the zwave scene.
        '''

    def setValue(self, valueid, valueData):
        '''
        Set a value to the zwave scene.
        '''

    def activate(self):
        '''
        Activate the zwave scene.
        '''
