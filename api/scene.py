# -*- coding: utf-8 -*-
"""
.. module:: openzwave.scene

This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.
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
import libopenzwave
from collections import namedtuple
import thread
import time
import openzwave
import logging
from openzwave.object import ZWaveObject

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveScene(ZWaveObject):
    '''
    Represents a single scene within the Z-Wave Network
    '''

    def __init__(self, scene_id, network=None):
        '''
        Initialize zwave scene

        :param scene_id: ID of the scene
        :type scene_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        '''
        ZWaveObject.__init__(self, scene_id, network)
        logging.debug("Create object scene (scene_id:%s)" % (scene_id))
        self.values = dict()
        #self._label = ''

    @property
    def scene_id(self):
        """
        The id of the scene.

        :rtype: int

        """
        return self._object_id

    @property
    def label(self):
        """
        The label of the scene.

        :rtype: str

        """
#        if self.is_outdated("self.name"):
#            #print "No cache"
#            self._name = self._network.manager.getNodeName(self.home_id, self.object_id)
#            self.update("self.name")
#        #print "self._name"
#        return self._name
        return self._network.manager.getSceneLabel(self.object_id)

    @label.setter
    def label(self, value):
        """
        Set the label of the scene.

        :param value: The new label of the scene
        :type value: str

        """
        self._network.manager.setSceneLabel(self.object_id, value)
#        self.outdate("self.name")

    def create(self, label=None):
        '''
        Create a new zwave scene on the network and update the object_id field
        If label is set, also change the label of the scene

        :param label: The new label
        :type label: str or None
        :returns: return the id of scene on the network. Return 0 if fails
        :rtype: int

        '''
        sceneid = self._network.manager.createScene()
        if sceneid != 0 :
            self._object_id = sceneid
            if label != None:
                self.label = label
        return sceneid

    def delete(self):
        '''
        Delete the scene on the network
        '''
        return self._network.manager.removeScene(self.object_id)

    def add_value(self, value_id, value_data):
        '''
        Add a value to the zwave scene.

        :param value_id: The id of the value to add
        :type value_id: int
        :rtype: bool

        '''
        value = ZWaveValue(value_id, network=self.network, parent_id=self.node_id, command_class=command_class)
        self.values[value_id] = value
        #self.values[value_id].oudated = True

    def change_value(self, value_id):
        """
        Change a value of the node. Todo

        :param value_id: The id of the value to change
        :type value_id: int
        :rtype: bool

        """
#        self.values[value_id].oudated = True
        pass

    def refresh_value(self, value_id):
        """
        Change a value of the node. Todo

        :param value_id: The id of the value to change
        :type value_id: int
        :rtype: bool

        """
#        self.values[value_id].oudated = True
        pass

    def remove_value(self, value_id):
        """
        Change a value of the node. Todo

        :param value_id: The id of the value to change
        :type value_id: int
        :rtype: bool

        """
        del(self.values[value_id])

    def set_value(self, value_id, value_data):
        '''
        Set a value to the zwave scene.

        :param value_id: ID of the value
        :type value_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        '''

    def activate(self):
        '''
        Activate the zwave scene.
        '''
