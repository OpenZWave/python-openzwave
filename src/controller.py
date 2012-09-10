# -*- coding: utf-8 -*-
"""
.. module:: openzwave.controller

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
from openzwave.node import ZWaveNode

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveController(ZwaveObject):
    '''
        The driver objet.
        Hold options of the manager
        Also used to retrieve informations about the library, ...
    '''

    def __init__(self, network, controllerId=None, devicePath=None, userPath=None\
        , configPath=None, options=None):
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
        if controllerId == None:
            controllerId = 1

        super(ZWaveController, self).__init__(controllerId, network)

        self._node = None
        self._homeId = 0

        self._libraryConfigPath = None
        self._libraryUserPath = None
        self._devicePath = None
        self._optionsManager = None

        self.libraryConfigPath = configPath
        if userPath != None:
            self.libraryUserPath = userPath
        if devicePath !=None:
            self.devicePath = devicePath
        if options!=None:
            self.optionsManager = options

        self._libraryTypeName = None
        self.cacheProperty(lambda: self.libraryTypeName)
        self._libraryVersion = None
        self.cacheProperty(lambda: self.libraryVersion)
        self._pythonLibraryVersion = None
        self.cacheProperty(lambda: self.pythonLibraryVersion)

    @property
    def node(self):
        """
        The node controller on the network.
        :rtype: ZWaveNode
        """
        return self._node

    @node.setter
    def node(self,value):
        """
        The node controller on the network.
        :rtype: ZWaveNode
        """
        if type(value) == type(ZWaveNode) or value == None:
            self._node = value
            self._homeId = self._node.homeId
        else:
            raise ZWaveException("Can't update node. Bad object type %s" % type(value))

    @property
    def nodeId(self):
        """
        The node Id of the controller on the network.
        :rtype: int
        """
        return self.node.objectId if self.node != None else None

    @property
    def nodeName(self):
        """
        The name of the controller on the network.
        :rtype: str
        """
        return self.node.Name if self.node != None else None

    @property
    def libraryTypeName(self):
        """
        The name of the library.
        :rtype: str
        """
        if self.isOutdated(lambda: self.libraryTypeName):
            self._libraryTypeName = self._network.manager.getLibraryTypeName(self._homeId)
            self.update(lambda: self.libraryTypeName)
        return self._libraryTypeName

    @property
    def libraryDescription(self):
        """
        The description of the library.
        :rtype: str
        """
        return '%s Version %s' % (self.libraryTypeName, self.libraryVersion)

    @property
    def libraryVersion(self):
        """
        The version of the library.
        :rtype: str
        """
        if self.isOutdated(lambda: self.libraryVersion):
            self._libraryVersion = self._network.manager.getLibraryVersion(self._homeId)
            self.update(lambda: self.libraryVersion)
        return self._libraryVersion

    @property
    def pythonLibraryVersion(self):
        """
        The version of the python library.
        :rtype: str
        """
        if self.isOutdated(lambda: self.pythonLibraryVersion):
            self._pythonLibraryVersion = self._network.manager.getPythonLibraryVersion()
            self.update(lambda: self.pythonLibraryVersion)
        return self._pythonLibraryVersion

    @property
    def libraryConfigPath(self):
        """
        The library Config path.
        :rtype: str
        """
        return self._libraryConfigPath

    @libraryConfigPath.setter
    def libraryConfigPath(self,value):
        """
        Set the library config path.
        """
        if value == None :
            value = self._network.manager.getLibraryConfigPath()
            if value == None :
                raise ZWaveException("Can't retrieve config path from library")
            else:
                self._libraryConfigPath = value
        else:
            if os.path.exists(value):
                self._libraryConfigPath = value
            else:
                raise ZWaveException("Can't retrieve config from %s" % value)

    @property
    def libraryUserPath(self):
        """
        The library User path.
        :rtype: str
        """
        return self._libraryUserPath

    @libraryUserPath.setter
    def libraryUserPath(self,value):
        """
        Set the library User path.
        """
        if value == None :
            self._libraryUserPath = None
        elif os.path.exists(value):
            if os.access(value, os.W_OK):
                self._libraryUserPath = value
            else:
                raise ZWaveException("Can't write in user path %s" % value)
        else:
            raise ZWaveException("Can't find user path %s" % value)

    @property
    def devicePath(self):
        """
        The device path.
        :rtype: str
        """
        return self._devicePath

    @devicePath.setter
    def devicePath(self,value):
        """
        Set the device path.
        """
        if value == None :
            self._devicePath = None
        elif os.path.exists(value):
            if os.access(value, os.W_OK):
                self._devicePath = value
            else:
                raise ZWaveException("Can't write to device %s" % value)
        else:
            raise ZWaveException("Can't find device %s" % value)

    @property
    def optionsManager(self):
        """
        The options manager.
        :rtype: str
        """
        return self._optionsManager

    @optionsManager.setter
    def optionsManager(self,value):
        """
        Set the options manager.
        """
        self._optionsManager = value

    @property
    def capabilities(self):
        """
        The capabilities of the controller.
        :rtype: list()
        """
        caps = list()
        if self.node.isPrimaryController(): caps.add('primaryController')
        if self.node.isStaticUpdateController(): caps.add('staticUpdateController')
        if self.node.isBridgeController(): caps.add('bridgeController')
        return caps
