# -*- coding: utf-8 -*-
"""
.. module:: openzwave.controller
.. _openzwaveController:

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
from louie import dispatcher, All
import logging
import libopenzwave
import openzwave
from openzwave.object import ZWaveException, ZWaveTypeException, ZWaveObject
from openzwave.node import ZWaveNode

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveController(ZWaveObject):
    '''
    The driver objet.
    Hold options of the manager
    Also used to retrieve informations about the library, ...

    '''

    def __init__(self, controller_id, network, options=None):
        '''
        Initialize controller object

        :param controller_id: The Id of the controller
        :type controller_id: int
        :param network: The network the controller is attached to
        :type network: ZwaveNetwork
        :param options: options of the manager
        :type options: str

        '''
        if controller_id == None:
            controller_id = 1
        ZWaveObject.__init__(self, controller_id, network)
        self._node = None
        self._options = options
        self._library_type_name = None
        #self.cache_property("self.library_type_name")
        self._library_version = None
        #self.cache_property("self.library_version")
        self._python_library_version = None
        #self.cache_property("self.python_library_version")

    @property
    def node(self):
        """
        The node controller on the network.

        :returns: The node controller on the network
        :rtype: ZWaveNode

        """
        return self._node

    @node.setter
    def node(self, value):
        """
        The node controller on the network.

        :param value: The node of the controller on the network
        :type value: ZWaveNode

        """
        self._node = value
        #if value != None:
        #   self.home_id = self._node.home_id

    @property
    def node_id(self):
        """
        The node Id of the controller on the network.

        :returns: The node id of the controller on the network
        :rtype: int

        """
        if self.node != None:
            return self.node.object_id
        else:
            return None

    @property
    def name(self):
        """
        The node name of the controller on the network.

        :returns: The node's name of the controller on the network
        :rtype: str

        """
        if self.node != None:
            return self.node.name
        else:
            return None

    @property
    def library_type_name(self):
        """
        The name of the library.

        :returns: The cpp library name
        :rtype: str

        """
        if self.is_outdated("self.library_type_name"):
            self._library_type_name = self._network.manager.getLibraryTypeName(self.home_id)
            self.update("self.library_type_name")
        return self._library_type_name

    @property
    def library_description(self):
        """
        The description of the library.

        :returns: The cpp library description (name and version)
        :rtype: str

        """
        return '%s version %s' % (self.library_type_name, self.library_version)

    @property
    def library_version(self):
        """
        The version of the library.

        :returns: The cpp library version
        :rtype: str

        """
        if self.is_outdated("self.library_version"):
            self._library_version = self._network.manager.getLibraryVersion(self.home_id)
            self.update("self.library_version")
        return self._library_version

    @property
    def python_library_version(self):
        """
        The version of the python library.

        :returns: The python library version
        :rtype: str

        """
        if self.is_outdated("self.python_library_version"):
            self._python_library_version = self._network.manager.getPythonLibraryVersion()
            self.update("self.python_library_version")
        return self._python_library_version

    @property
    def ozw_library_version(self):
        """
        The version of the openzwave library.

        :returns: The openzwave library version
        :rtype: str

        """
        if self.is_outdated("self.ozw_library_version"):
            self._ozw_library_version = self._network.manager.getOzwLibraryVersion()
            self.update("self.ozw_library_version")
        return self._ozw_library_version

    @property
    def library_config_path(self):
        """
        The library Config path.

        :returns: The library config directory
        :rtype: str

        """
        if self._options != None :
            return self._options.config_path
        else :
            return None

    @property
    def library_user_path(self):
        """
        The library User path.

        :returns: The user directory to store user configuration
        :rtype: str

        """
        if self._options != None :
            return self._options.user_path
        else :
            return None

    @property
    def device(self):
        """
        The device path.

        :returns: The device (ie /dev/zwave)
        :rtype: str

        """
        if self._options != None :
            return self._options.device
        else :
            return None

    @property
    def options(self):
        """
        The starting options of the manager.

        :returns: The options used to start the manager
        :rtype: ZWaveOption

        """
        return self._options

    @property
    def stats(self):
        """
        Retrieve statistics from driver.

        Statistics:

            * s_SOFCnt                         : Number of SOF bytes received
            * s_ACKWaiting                     : Number of unsolicited messages while waiting for an ACK
            * s_readAborts                     : Number of times read were aborted due to timeouts
            * s_badChecksum                    : Number of bad checksums
            * s_readCnt                        : Number of messages successfully read
            * s_writeCnt                       : Number of messages successfully sent
            * s_CANCnt                         : Number of CAN bytes received
            * s_NAKCnt                         : Number of NAK bytes received
            * s_ACKCnt                         : Number of ACK bytes received
            * s_OOFCnt                         : Number of bytes out of framing
            * s_dropped                        : Number of messages dropped & not delivered
            * s_retries                        : Number of messages retransmitted
            * s_controllerReadCnt              : Number of controller messages read
            * s_controllerWriteCnt             : Number of controller messages sent

        :returns: Statistics of the controller
        :rtype: dict()

        """
        return self._network.manager.getDriverStatistics(self.home_id)

    @property
    def capabilities(self):
        """
        The capabilities of the controller.

        :returns: The capabilities of the controller
        :rtype: set()

        """
        caps = set()
        if self.node.is_primary_controller:
            caps.add('primaryController')
        if self.node.is_static_update_controller:
            caps.add('staticUpdateController')
        if self.node.is_bridge_controller:
            caps.add('bridgeController')
        return caps

    def hard_reset(self):
        """
        Hard Reset a PC Z-Wave Controller.
        Resets a controller and erases its network configuration settings.  The
        controller becomes a primary controller ready to add devices to a new network.

        """
        self._network.manager.resetController(self._network.home_id)
        self._network.state = self.STATE_RESET

    def soft_reset(self):
        """
        Soft Reset a PC Z-Wave Controller.
        Resets a controller without erasing its network configuration settings.

        """
        self._network.manager.softResetController(self._network.home_id)

    def cancel_command(self):
        """
        Cancels any in-progress command running on a controller.

        """
        self._network.manager.cancelControllerCommand(self._network.home_id)
