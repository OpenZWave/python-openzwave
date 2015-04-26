# -*- coding: utf-8 -*-
"""
.. module:: openzwave.controller
.. _openzwaveController:

This file is part of **python-openzwave** project https://github.com/bibi21000/python-openzwave.
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
from louie import dispatcher
import time
from openzwave.object import ZWaveObject
from libopenzwave import PyStatDriver

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

class ZWaveController(ZWaveObject):
    '''
    The controller manager.

    Allows to retrieve informations about the library, statistics, ...
    Also used to send commands to the controller

    Commands :

        - Driver::ControllerCommand_AddController : Add a new secondary controller to the Z-Wave network.
        - Driver::ControllerCommand_AddDevice : Add a new device (but not a controller) to the Z-Wave network.
        - Driver::ControllerCommand_CreateNewPrimary : (Not yet implemented)
        - Driver::ControllerCommand_ReceiveConfiguration :
        - Driver::ControllerCommand_RemoveController : remove a controller from the Z-Wave network.
        - Driver::ControllerCommand_RemoveDevice : remove a device (but not a controller) from the Z-Wave network.
        - Driver::ControllerCommand_RemoveFailedNode : move a node to the controller's list of failed nodes.  The node must actually
                                                       have failed or have been disabled since the command will fail if it responds.  A node must be in the controller's failed nodes list
                                                       or ControllerCommand_ReplaceFailedNode to work.
        - Driver::ControllerCommand_HasNodeFailed : Check whether a node is in the controller's failed nodes list.
        - Driver::ControllerCommand_ReplaceFailedNode : replace a failed device with another. If the node is not in
                                                        the controller's failed nodes list, or the node responds, this command will fail.
        - Driver:: ControllerCommand_TransferPrimaryRole : (Not yet implemented) - Add a new controller to the network and
                                                           make it the primary.  The existing primary will become a secondary controller.
        - Driver::ControllerCommand_RequestNetworkUpdate : Update the controller with network information from the SUC/SIS.
        - Driver::ControllerCommand_RequestNodeNeighborUpdate : Get a node to rebuild its neighbour list.  This method also does ControllerCommand_RequestNodeNeighbors afterwards.
        - Driver::ControllerCommand_AssignReturnRoute : Assign a network return route to a device.
        - Driver::ControllerCommand_DeleteAllReturnRoutes : Delete all network return routes from a device.
        - Driver::ControllerCommand_CreateButton : Create a handheld button id.
        - Driver::ControllerCommand_DeleteButton : Delete a handheld button id.

    Callbacks :

        - Driver::ControllerState_Waiting : The controller is waiting for a user action.  A notice should be displayed
                                            to the user at this point, telling them what to do next.
                                            For the add, remove, replace and transfer primary role commands, the user needs to be told to press the
                                            inclusion button on the device that  is going to be added or removed.  For ControllerCommand_ReceiveConfiguration,
                                            they must set their other controller to send its data, and for ControllerCommand_CreateNewPrimary, set the other
                                            controller to learn new data.
        - Driver::ControllerState_InProgress : the controller is in the process of adding or removing the chosen node.  It is now too late to cancel the command.
        - Driver::ControllerState_Complete : the controller has finished adding or removing the node, and the command is complete.
        - Driver::ControllerState_Failed : will be sent if the command fails for any reason.

    '''
    SIGNAL_CTRL_NORMAL = 'Normal'
    SIGNAL_CTRL_STARTING = 'Starting'
    SIGNAL_CTRL_CANCEL = 'Cancel'
    SIGNAL_CTRL_ERROR = 'Error'
    SIGNAL_CTRL_WAITING = 'Waiting'
    SIGNAL_CTRL_SLEEPING = 'Sleeping'
    SIGNAL_CTRL_INPROGRESS = 'InProgress'
    SIGNAL_CTRL_COMPLETED = 'Completed'
    SIGNAL_CTRL_FAILED = 'Failed'
    SIGNAL_CTRL_NODEOK = 'NodeOK'
    SIGNAL_CTRL_NODEFAILED = 'NodeFailed'

    SIGNAL_CONTROLLER = 'Message'

    CMD_NONE = 0
    CMD_ADDDEVICE = 1
    CMD_CREATENEWPRIMARY = 2
    CMD_RECEIVECONFIGURATION = 3
    CMD_REMOVEDEVICE = 4
    CMD_REMOVEFAILEDNODE = 5
    CMD_HASNODEFAILED = 6
    CMD_REPLACEFAILEDNODE = 7
    CMD_TRANSFERPRIMARYROLE = 8
    CMD_REQUESTNETWORKUPDATE = 9
    CMD_REQUESTNODENEIGHBORUPDATE = 10
    CMD_ASSIGNRETURNROUTE = 11
    CMD_DELETEALLRETURNROUTES = 12
    CMD_SENDNODEINFORMATION = 13
    CMD_REPLICATIONSEND = 14
    CMD_CREATEBUTTON = 15
    CMD_DELETEBUTTON = 16

    def __init__(self, controller_id, network, options=None):
        """
        Initialize controller object

        :param controller_id: The Id of the controller
        :type controller_id: int
        :param network: The network the controller is attached to
        :type network: ZwaveNetwork
        :param options: options of the manager
        :type options: str

        """
        if controller_id is None:
            controller_id = 1
        ZWaveObject.__init__(self, controller_id, network)
        self._node = None
        self._options = options
        self._library_type_name = None
        self._library_version = None
        self._python_library_version = None
        self.ctrl_last_state = self.SIGNAL_CTRL_NORMAL
        self.ctrl_last_message = ""

    def __str__(self):
        """
        The string representation of the node.

        :rtype: str

        """
        return 'home_id: [%s] id: [%s] name: [%s] product: [%s] capabilities: %s library: [%s]' % \
          (self._network.home_id_str, self._object_id, self._node.name, self._node.product_name, self.capabilities, self.library_description)

    @property
    def node(self):
        """
        The node controller on the network.

        :return: The node controller on the network
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

    @property
    def node_id(self):
        """
        The node Id of the controller on the network.

        :return: The node id of the controller on the network
        :rtype: int

        """
        if self.node is not None:
            return self.node.object_id
        else:
            return None

    @property
    def name(self):
        """
        The node name of the controller on the network.

        :return: The node's name of the controller on the network
        :rtype: str

        """
        if self.node is not None:
            return self.node.name
        else:
            return None

    @property
    def library_type_name(self):
        """
        The name of the library.

        :return: The cpp library name
        :rtype: str

        """
        return self._network.manager.getLibraryTypeName(self._network.home_id)

    @property
    def library_description(self):
        """
        The description of the library.

        :return: The library description (name and version)
        :rtype: str

        """
        return '%s version %s' % (self.library_type_name, self.library_version)

    @property
    def library_version(self):
        """
        The version of the library.

        :return: The cpp library version
        :rtype: str

        """
        return self._network.manager.getLibraryVersion(self._network.home_id)

    @property
    def python_library_version(self):
        """
        The version of the python library.

        :return: The python library version
        :rtype: str

        """
        return self._network.manager.getPythonLibraryVersionNumber()

    @property
    def ozw_library_version(self):
        """
        The version of the openzwave library.

        :return: The openzwave library version
        :rtype: str

        """
        return self._network.manager.getOzwLibraryVersion()

    @property
    def library_config_path(self):
        """
        The library Config path.

        :return: The library config directory
        :rtype: str

        """
        if self._options is not None:
            return self._options.config_path
        else:
            return None

    @property
    def library_user_path(self):
        """
        The library User path.

        :return: The user directory to store user configuration
        :rtype: str

        """
        if self._options is not None:
            return self._options.user_path
        else:
            return None

    @property
    def device(self):
        """
        The device path.

        :return: The device (ie /dev/zwave)
        :rtype: str

        """
        if self._options is not None:
            return self._options.device
        else:
            return None

    @property
    def options(self):
        """
        The starting options of the manager.

        :return: The options used to start the manager
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

        :return: Statistics of the controller
        :rtype: dict()

        """
        return self._network.manager.getDriverStatistics(self.home_id)

    def get_stats_label(self, stat):
        """
        Retrieve label of the statistic from driver.

        :param stat: The code of the stat label to retrieve.
        :type stat:
        :return: The label or the stat.
        :rtype: str

        """
        #print "stat = %s" % stat
        return PyStatDriver[stat]

    @property
    def capabilities(self):
        """
        The capabilities of the controller.

        :return: The capabilities of the controller
        :rtype: set

        """
        caps = set()
        if self.is_primary_controller:
            caps.add('primaryController')
        if self.is_static_update_controller:
            caps.add('staticUpdateController')
        if self.is_bridge_controller:
            caps.add('bridgeController')

        return caps

    @property
    def is_primary_controller(self):
        """
        Is this node a primary controller of the network.

        :rtype: bool

        """
        return self._network.manager.isPrimaryController(self.home_id)

    @property
    def is_static_update_controller(self):
        """
        Is this controller a static update controller (SUC).

        :rtype: bool

        """
        return self._network.manager.isStaticUpdateController(self.home_id)

    @property
    def is_bridge_controller(self):
        """
        Is this controller using the bridge controller library.

        :rtype: bool

        """
        return self._network.manager.isBridgeController(self.home_id)

    @property
    def send_queue_count(self):
        """
        Get count of messages in the outgoing send queue.

        :return: Thr count of messages in the outgoing send queue.
        :rtype: int

        """
        return self._network.manager.getSendQueueCount(self.home_id)

    def hard_reset(self):
        """
        Hard Reset a PC Z-Wave Controller.
        Resets a controller and erases its network configuration settings.
        The controller becomes a primary controller ready to add devices to a new network.

        This command fires a lot of louie signals.
        Louie's clients must disconnect from nodes and values signals

        .. code-block:: python

                dispatcher.send(self._network.SIGNAL_NETWORK_RESETTED, **{'network': self._network})

        """
        self._network.state = self._network.STATE_RESETTED
        dispatcher.send(self._network.SIGNAL_NETWORK_RESETTED, \
            **{'network': self._network})
        self._network.manager.resetController(self._network.home_id)
        time.sleep(5)

    def soft_reset(self):
        """
        Soft Reset a PC Z-Wave Controller.
        Resets a controller without erasing its network configuration settings.

        """
        self._network.manager.softResetController(self._network.home_id)

    def begin_command_send_node_information(self, node_id):
        """
        Send a node information frame.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_SENDNODEINFORMATION, self.zwcallback, nodeId=node_id)

    def begin_command_replication_send(self, high_power=False):
        """
        Send information from primary to secondary.

        :param high_power: Usually when adding or removing devices, the controller operates at low power so that the controller must
                           be physically close to the device for security reasons.  If _highPower is true, the controller will
                           operate at normal power levels instead.  Defaults to false.
        :type high_power: bool
        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REPLICATIONSEND, self.zwcallback, highPower=high_power)

    def begin_command_request_network_update(self):
        """
        Update the controller with network information from the SUC/SIS.

        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REQUESTNETWORKUPDATE, self.zwcallback)

    def begin_command_add_device(self, high_power=False):
        """
        Add a new device to the Z-Wave network.

        :param high_power: Used only with the AddDevice, AddController, RemoveDevice and RemoveController commands.
                           Usually when adding or removing devices, the controller operates at low power so that the controller must
                           be physically close to the device for security reasons.  If _highPower is true, the controller will
                           operate at normal power levels instead.  Defaults to false.
        :type high_power: bool
        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_ADDDEVICE, self.zwcallback, highPower=high_power)

    def begin_command_remove_device(self, high_power=False):
        """
        Remove a device from the Z-Wave network.

        :param high_power: Used only with the AddDevice, AddController, RemoveDevice and RemoveController commands.
                           Usually when adding or removing devices, the controller operates at low power so that the controller must
                           be physically close to the device for security reasons.  If _highPower is true, the controller will
                           operate at normal power levels instead.  Defaults to false.
        :type high_power: bool
        :return: True if the command was accepted and has started.
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
        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REMOVEFAILEDNODE, self.zwcallback, nodeId=node_id)

    def begin_command_has_node_failed(self, node_id):
        """
        Check whether a node is in the controller's failed nodes list.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :return: True if the command was accepted and has started.
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
        :return: True if the command was accepted and has started.
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
        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_REQUESTNODENEIGHBORUPDATE, self.zwcallback, nodeId=node_id)

    def begin_command_create_new_primary(self):
        """
        Add a new controller to the Z-Wave network. Used when old primary fails. Requires SUC.

        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_CREATENEWPRIMARY, self.zwcallback)

    def begin_command_transfer_primary_role(self, high_power=False):
        """
        Make a different controller the primary.
        The existing primary will become a secondary controller.

        :param high_power: Used only with the AddDevice, AddController, RemoveDevice and RemoveController commands.
                           Usually when adding or removing devices, the controller operates at low power so that the controller must
                           be physically close to the device for security reasons.  If _highPower is true, the controller will
                           operate at normal power levels instead.  Defaults to false.
        :type high_power: bool
        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_TRANSFERPRIMARYROLE, self.zwcallback, highPower=high_power)

    def begin_command_receive_configuration(self):
        """
        -

        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_RECEIVECONFIGURATION, self.zwcallback)

    def begin_command_assign_return_route(self, from_node_id, to_node_id):
        """
        Assign a network return route from a node to another one.

        :param from_node_id: The node that we will use the route.
        :type from_node_id: int
        :param to_node_id: The node that we will change the route
        :type to_node_id: int
        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_ASSIGNRETURNROUTE, self.zwcallback, nodeId=from_node_id, arg=to_node_id)

    def begin_command_delete_all_return_routes(self, node_id):
        """
        Delete all network return routes from a device.

        :param node_id: Used only with the ReplaceFailedNode command, to specify the node that is going to be replaced.
        :type node_id: int
        :return: True if the command was accepted and has started.
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
        :return: True if the command was accepted and has started.
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
        :return: True if the command was accepted and has started.
        :rtype: bool

        """
        return self._network.manager.beginControllerCommand(self._network.home_id, \
            self.CMD_DELETEBUTTON, self.zwcallback, nodeId=node_id, arg=arg)

    def cancel_command(self):
        """
        Cancels any in-progress command running on a controller.

        """
        return self._network.manager.cancelControllerCommand(self._network.home_id)

    def zwcallback(self, args):
        """
        The Callback Handler used when sendig commands to the controller.
        Dispatch a louie message.

        To do : add node in signal when necessary

        :param args: A dict containing informations about the state of the controller
        :type args: dict()

        """
        logger.debug('Controller state change : %s', args)
        state = args['state']
        message = args['message']
        self.ctrl_last_state = state
        self.ctrl_last_message = message
        if state == self.SIGNAL_CTRL_WAITING:
            dispatcher.send(self.SIGNAL_CTRL_WAITING, \
                **{'state': state, 'message': message, 'network': self._network, 'controller': self})
        dispatcher.send(self.SIGNAL_CONTROLLER, \
            **{'state': state, 'message': message, 'network': self._network, 'controller': self})

    def to_dict(self):
        """
        Return a dict representation of the controller.

        :rtype: dict()

        """
        ret=self.node.to_dict()
        ret["zw_version"] = self.library_version
        ret["zw_description"] = self.library_description
        ret["oz_version"] = self.ozw_library_version
        ret["py_version"] = self.python_library_version
        return ret



