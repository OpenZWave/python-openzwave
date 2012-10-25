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
    The controller manager.

    Allows to retrieve informations about the library, statistics, ...
    Also used to send commands to the controller

    Commands :

        - Driver::ControllerCommand_AddController - Add a new secondary controller to the Z-Wave network.
        - Driver::ControllerCommand_AddDevice - Add a new device (but not a controller) to the Z-Wave network.
        - Driver::ControllerCommand_CreateNewPrimary (Not yet implemented)
        - Driver::ControllerCommand_ReceiveConfiguration -
        - Driver::ControllerCommand_RemoveController - remove a controller from the Z-Wave network.
        - Driver::ControllerCommand_RemoveDevice - remove a device (but not a controller) from the Z-Wave network.
        - Driver::ControllerCommand_RemoveFailedNode - move a node to the controller's list of failed nodes.  The node must actually
        have failed or have been disabled since the command will fail if it responds.  A node must be in the controller's failed nodes list
        for ControllerCommand_ReplaceFailedNode to work.
        - Driver::ControllerCommand_HasNodeFailed - Check whether a node is in the controller's failed nodes list.
        - Driver::ControllerCommand_ReplaceFailedNode - replace a failed device with another. If the node is not in
        the controller's failed nodes list, or the node responds, this command will fail.
        - Driver:: ControllerCommand_TransferPrimaryRole    (Not yet implemented) - Add a new controller to the network and
        make it the primary.  The existing primary will become a secondary controller.
        - Driver::ControllerCommand_RequestNetworkUpdate - Update the controller with network information from the SUC/SIS.
        - Driver::ControllerCommand_RequestNodeNeighborUpdate - Get a node to rebuild its neighbour list.  This method also does ControllerCommand_RequestNodeNeighbors afterwards.
        - Driver::ControllerCommand_AssignReturnRoute - Assign a network return route to a device.
        - Driver::ControllerCommand_DeleteAllReturnRoutes - Delete all network return routes from a device.
        - Driver::ControllerCommand_CreateButton - Create a handheld button id.
        - Driver::ControllerCommand_DeleteButton - Delete a handheld button id.

    Callbacks :

        - Driver::ControllerState_Waiting, the controller is waiting for a user action.  A notice should be displayed
        to the user at this point, telling them what to do next.
        For the add, remove, replace and transfer primary role commands, the user needs to be told to press the
        inclusion button on the device that  is going to be added or removed.  For ControllerCommand_ReceiveConfiguration,
        they must set their other controller to send its data, and for ControllerCommand_CreateNewPrimary, set the other
        controller to learn new data.
        - Driver::ControllerState_InProgress - the controller is in the process of adding or removing the chosen node.  It is now too late to cancel the command.
        - Driver::ControllerState_Complete - the controller has finished adding or removing the node, and the command is complete.
        - Driver::ControllerState_Failed - will be sent if the command fails for any reason.

    '''
    SIGNAL_CTRL_NORMAL = 'Normal'
    SIGNAL_CTRL_WAITING = 'Waiting'
    SIGNAL_CTRL_INPROGRESS = 'InProgress'
    SIGNAL_CTRL_COMPLETED = 'Completed'
    SIGNAL_CTRL_FAILED = 'Failed'
    SIGNAL_CTRL_NODEOK = 'NodeOK'
    SIGNAL_CTRL_NODEFAILED = 'NodeFailed'

    SIGNAL_CONTROLLER = 'Message'

    CMD_NONE = 0
    CMD_ADDCONTROLLER = 1
    CMD_ADDDEVICE = 2
    CMD_CREATENEWPRIMARY = 3
    CMD_RECEIVECONFIGURATION = 4
    CMD_REMOVECONTROLLER = 5
    CMD_REMOVEDEVICE = 6
    CMD_REMOVEFAILEDNODE = 7
    CMD_HASNODEFAILED = 8
    CMD_REPLACEFAILEDNODE = 9
    CMD_TRANSFERPRIMARYROLE = 10
    CMD_REQUESTNETWORKUPDATE = 11
    CMD_REQUESTNODENEIGHBORUPDATE = 12
    CMD_ASSIGNRETURNROUTE = 13
    CMD_DELETEALLRETURNROUTES = 14
    CMD_CREATEBUTTON = 15
    CMD_DELETEBUTTON = 16

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
        :rtype: int

        """
        caps = set()
        if self.node.is_primary_controller:
            caps.add('primaryController')
        if self.node.is_static_update_controller:
            caps.add('staticUpdateController')
        if self.node.is_bridge_controller:
            caps.add('bridgeController')
        if self.node.is_routing_device:
            caps.add('routing')
        if self.node.is_listening_device:
            caps.add('listening')
        if self.node.is_frequent_listening_device:
            caps.add('frequent')
        if self.node.is_security_device:
            caps.add('security')
        if self.node.is_beaming_device:
            caps.add('beaming')
        return caps

    @property
    def send_queue_count(self):
        """
        Get count of messages in the outgoing send queue.

        :returns: Thr count of messages in the outgoing send queue.
        :rtype: int

        """
        return self._network.manager.getSendQueueCount(self.home_id)

    def hard_reset(self):
        """
        Hard Reset a PC Z-Wave Controller.
        Resets a controller and erases its network configuration settings.  The
        controller becomes a primary controller ready to add devices to a new network.

        """
        self._network.manager.resetController(self._network.home_id)

    def soft_reset(self):
        """
        Soft Reset a PC Z-Wave Controller.
        Resets a controller without erasing its network configuration settings.

        """
        self._network.manager.softResetController(self._network.home_id)

    def begin_command_request_network_update(self):
        """
        Update the controller with network information from the SUC/SIS.

        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REQUESTNETWORKUPDATE, self.zwcallback)

    def begin_command_add_controller(self, high_power = False):
        """
        Add a new secondary controller to the Z-Wave network.

        :param high_power: Used only with the AddDevice, AddController, RemoveDevice and RemoveController commands.
        Usually when adding or removing devices, the controller operates at low power so that the controller must
        be physically close to the device for security reasons.  If _highPower is true, the controller will
        operate at normal power levels instead.  Defaults to false.
        :type high_power: bool
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_ADDCONTROLLER, self.zwcallback, highPower=high_power)

    def begin_command_add_device(self, high_power = False):
        """
        Add a new device (but not a controller) to the Z-Wave network.

        :param high_power: Used only with the AddDevice, AddController, RemoveDevice and RemoveController commands.
        Usually when adding or removing devices, the controller operates at low power so that the controller must
        be physically close to the device for security reasons.  If _highPower is true, the controller will
        operate at normal power levels instead.  Defaults to false.
        :type high_power: bool
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_ADDDEVICE, self.zwcallback, highPower=high_power)

    def begin_command_remove_controller(self, high_power = False):
        """
        Remove a controller from the Z-Wave network.

        :param high_power: Used only with the AddDevice, AddController, RemoveDevice and RemoveController commands.
        Usually when adding or removing devices, the controller operates at low power so that the controller must
        be physically close to the device for security reasons.  If _highPower is true, the controller will
        operate at normal power levels instead.  Defaults to false.
        :type high_power: bool
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REMOVECONTROLLER, self.zwcallback, highPower=high_power)

    def begin_command_remove_device(self, high_power = False):
        """
        Remove a device (but not a controller) from the Z-Wave network.

        :param high_power: Used only with the AddDevice, AddController, RemoveDevice and RemoveController commands.
        Usually when adding or removing devices, the controller operates at low power so that the controller must
        be physically close to the device for security reasons.  If _highPower is true, the controller will
        operate at normal power levels instead.  Defaults to false.
        :type high_power: bool
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REMOVEDEVICE, self.zwcallback, highPower=high_power)

    def begin_command_remove_failed_node(self, node_id):
        """
        Move a node to the controller's list of failed nodes.  The node must
        actually have failed or have been disabled since the command
        will fail if it responds.  A node must be in the controller's
        failed nodes list for ControllerCommand_ReplaceFailedNode to work.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REMOVEFAILEDNODE, self.zwcallback, nodeId=node_id)

    def begin_command_has_node_failed(self, node_id):
        """
        Check whether a node is in the controller's failed nodes list.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_HASNODEFAILED, self.zwcallback, nodeId=node_id)

    def begin_command_replace_failed_node(self, node_id):
        """
        Replace a failed device with another. If the node is not in
        the controller's failed nodes list, or the node responds, this command will fail.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REPLACEFAILEDNODE, self.zwcallback, nodeId=node_id)

    def begin_command_request_node_neigbhor_update(self, node_id):
        """
        Get a node to rebuild its neighbors list.
        This method also does ControllerCommand_RequestNodeNeighbors afterwards.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REQUESTNODENEIGHBORUPDATE, self.zwcallback, nodeId=node_id)

    def begin_command_create_new_primary(self):
        """
        (Not yet implemented)

        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_CREATENEWPRIMARY, self.zwcallback)

    def begin_command_transfer_primary_role(self):
        """
        (Not yet implemented)
        Add a new controller to the network and make it the primary.
        The existing primary will become a secondary controller.

        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_TRANSFERPRIMARYROLE, self.zwcallback)

    def begin_command_receive_configuration(self):
        """
        -

        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_RECEIVECONFIGURATION, self.zwcallback)

    def begin_command_assign_return_route(self, node_id):
        """
        Assign a network return route to a device.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_ASSIGNRETURNROUTE, self.zwcallback, nodeId=node_id)

    def begin_command_delete_all_return_routes(self, node_id):
        """
        Delete all network return routes from a device.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_DELETEALLRETURNROUTES, self.zwcallback, nodeId=node_id)

    def begin_command_create_button(self, node_id, arg=0):
        """
        Create a handheld button id

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :param arg:
        :type arg: int
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_CREATEBUTTON, self.zwcallback, nodeId=node_id, arg=arg)

    def begin_command_delete_button(self, node_id, arg=0):
        """
        Delete a handheld button id.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :param arg:
        :type arg: int
        :returns: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_DELETEBUTTON, self.zwcallback, nodeId=node_id, arg=arg)

    def cancel_command(self):
        """
        Cancels any in-progress command running on a controller.

        """
        self._network.manager.cancelControllerCommand(self._network.home_id)

    def zwcallback(self, args):
        """
        The Callback Handler used when sendig commands to the controller.
        Dispatch a louie message.

        To do : add node in signal when necessary

        :param args: A dict containing informations about the state of the controller
        :type args: dict()

        """
        logging.debug('Controller state change : %s' % (args))
        state = args['state']
        message = args['message']
        if state == self.SIGNAL_CTRL_WAITING:
            dispatcher.send(self.SIGNAL_CTRL_WAITING, \
                **{'state': state, 'message': message, 'network': self._network, 'controller': self})
        dispatcher.send(self.SIGNAL_CONTROLLER, \
            **{'state': state, 'message': message, 'network': self._network, 'controller': self})
