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

    def __init__(self, controller_id, network, options=None):
        '''
        Initialize driver object

        :param controller_id: The Id of the controller
        :type controller_id: int
        :param network: The network the controller is attached to
        :type network: ZwaveNetwork
        :param options: options of the manager
        :type options: str

        '''
        if controller_id == None:
            controller_id = 1
        ZwaveObject.__init__(controller_id, network)
        self._node = None
        self._options = options
        self._library_type_name = None
        self.cache_property(lambda: self.library_type_name)
        self._library_version = None
        self.cache_property(lambda: self.library_version)
        self._python_library_version = None
        self.cache_property(lambda: self.python_library_version)

    @property
    def node(self):
        """
        The node controller on the network.

        :rtype: ZWaveNode

        """
        return self._node

    @node.setter
    def node(self, value):
        """
        The node controller on the network.

        :rtype: ZWaveNode

        """
        if type(value) == type(ZWaveNode) or value == None:
            self._node = value
            self._home_id = self._node.home_id
        else:
            raise ZWaveException("Can't update node. Bad object type %s" % type(value))

    @property
    def node_id(self):
        """
        The node Id of the controller on the network.

        :rtype: int

        """
        return self.node.object_id if self.node != None else None

    @property
    def node_name(self):
        """
        The name of the controller on the network.

        :rtype: str

        """
        return self.node.name if self.node != None else None

    @property
    def library_type_name(self):
        """
        The name of the library.

        :rtype: str

        """
        if self.is_outdated(lambda: self.library_type_name):
            self._library_type_name = self._network.manager.getLibraryTypeName(self._home_id)
            self.update(lambda: self.library_type_name)
        return self._library_type_name

    @property
    def library_description(self):
        """
        The description of the library.

        :rtype: str

        """
        return '%s Version %s' % (self.library_type_name, self.library_version)

    @property
    def library_version(self):
        """
        The version of the library.

        :rtype: str

        """
        if self.is_outdated(lambda: self.library_version):
            self._library_version = self._network.manager.getLibraryVersion(self._home_id)
            self.update(lambda: self.library_version)
        return self._library_version

    @property
    def python_library_version(self):
        """
        The version of the python library.

        :rtype: str

        """
        if self.is_outdated(lambda: self.python_library_version):
            self._python_library_version = self._network.manager.getPythonLibraryVersion()
            self.update(lambda: self.python_library_version)
        return self._python_library_version

    @property
    def library_config_path(self):
        """
        The library Config path.

        :rtype: str

        """
        return self._library_config_path

    @library_config_path.setter
    def library_config_path(self, value):
        """
        Set the library config path.

        :param value: The new library config path
        :type value: str

        """
        if value == None :
            value = self._network.manager.getLibraryConfigPath()
            if value == None :
                raise ZWaveException("Can't retrieve config path from library")
            else:
                self._library_config_path = value
        else:
            if os.path.exists(value):
                self._library_config_path = value
            else:
                raise ZWaveException("Can't retrieve config from %s" % value)

    @property
    def library_user_path(self):
        """
        The library User path.

        :rtype: str

        """
        return self._library_user_path

    @library_user_path.setter
    def library_user_path(self, value):
        """
        Set the library User path.

        :param value: The new library user path
        :type value: str

        """
        if value == None :
            self._library_user_path = None
        elif os.path.exists(value):
            if os.access(value, os.W_OK):
                self._library_user_path = value
            else:
                raise ZWaveException("Can't write in user path %s" % value)
        else:
            raise ZWaveException("Can't find user path %s" % value)

    @property
    def device(self):
        """
        The device path.

        :rtype: str

        """
        return self._device

    @device.setter
    def device(self, value):
        """
        Set the device path.

        :param value: The new device.
        :type value: str

        """
        if value == None :
            self._device = None
        elif os.path.exists(value):
            if os.access(value, os.W_OK):
                self._device_path = value
            else:
                raise ZWaveException("Can't write to device %s" % value)
        else:
            raise ZWaveException("Can't find device %s" % value)

    @property
    def options_manager(self):
        """
        The options manager.

        :rtype: str

        """
        return self._options_manager

    @options_manager.setter
    def options_manager(self, value):
        """
        Set the options manager.

        :param value: The new option manager.
        :type value: str

        """
        self._options_manager = value

    @property
    def capabilities(self):
        """
        The capabilities of the controller.

        :rtype: list()

        """
        caps = list()
        if self.node.is_primary_controller():
            caps.append('primaryController')
        if self.node.is_static_update_controller():
            caps.append('staticUpdateController')
        if self.node.is_bridge_controller():
            caps.append('bridgeController')
        return caps
