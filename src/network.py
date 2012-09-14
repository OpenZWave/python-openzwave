# -*- coding: utf-8 -*-
"""
.. module:: openzwave.network

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
import time
from louie import dispatcher, All
import logging
import libopenzwave
import openzwave
from openzwave.object import ZWaveException, ZwaveObject, NullLoggingHandler
from openzwave.controller import ZWaveController
from openzwave.node import ZWaveNode
from openzwave.option import ZWaveOption

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveNetwork(ZwaveObject):
    '''
    The network objet = homeid.
    It contains a reference to the manager
    '''
    SIGNAL_DRIVER_FAILED = 'driverFailed'
    SIGNAL_DRIVER_READY = 'driverReady'
    SIGNAL_DRIVER_RESET = 'driverReset'
    SIGNAL_NODE_ADDED = 'nodeAdded'
    SIGNAL_NODE_EVENT = 'nodeEvent'
    SIGNAL_NODE_NAMING = 'nodeNaming'
    SIGNAL_NODE_NEW = 'nodeNew'
    SIGNAL_NODE_PROTOCOL_INFO = 'nodeProtocolInfo'
    SIGNAL_NODE_READY = 'nodeReady'
    SIGNAL_NODE_REMOVED = 'nodeRemoved'
    SIGNAL_VALUE_ADDED = 'valueAdded'
    SIGNAL_VALUE_CHANGED = 'valueChanged'
    SIGNAL_VALUE_REFRESHED = 'valueRefreshed'
    SIGNAL_VALUE_REMOVED = 'valueRemoved'
    SIGNAL_POLLING_ENABLED = 'pollingEnabled'
    SIGNAL_POLLING_DISABLED = 'pollingDisabled'
    SIGNAL_CREATE_BUTTON = 'createButton'
    SIGNAL_DELETE_BUTTON = 'deleteButton'
    SIGNAL_BUTTON_ON = 'buttonOn'
    SIGNAL_BUTTON_OFF = 'buttonOff'
    SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE = 'essentialNodeQueriesComplete'
    SIGNAL_NODE_QUERIES_COMPLETE = 'nodeQueriesComplete'
    SIGNAL_AWAKE_NODE_QUERIES_COMPLETE = 'awakeNodeQueriesComplete'
    SIGNAL_ALLNODE_QUERIES_COMPLETE = 'allNodeQueriesComplete'
    SIGNAL_MSG_COMPLETE = 'msgComplete'
    SIGNAL_ERROR = 'error'

    ignoreSubsequent = True

    def __init__(self, options, log=None):
        '''
        Initialize zwave network

        :param networkId: ID of the network
        :type networkId: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        '''
        logging.debug("Create network object.")
        self.log = log
        super(ZWaveNetwork, self).__init__(None, self)
        self._controller = ZWaveController(1, self, options)
        self._manager = libopenzwave.PyManager()
        self._manager.create()
        self._manager.addWatcher(self.zwcallback)
        self._manager.addDriver(options.device)
        self._nodes = dict()
        self._started = False

    @property
    def home_id(self):
        """
        The home_id of the network.

        :rtype: int

        """
        return self._object_id

    @property.setter
    def home_id(self, value):
        """
        The home_id of the network.

        :param value: new home_id
        :type value: int

        """
        self._object_id = value

    @property
    def controller(self):
        """
        The controller of the network.

        :rtype: ZWaveController

        """
        return self._controller

#    @controller.setter
#    def controller(self, value):
#        """
#        The controller of the network.
#        :rtype:
#        """
#        if type(value) == type(ZWaveController) or value == None:
#            self._controller = value
#        else:
#            raise ZWaveException("Can't update controller. Bad object type %s" % type(value))

    @property
    def nodes(self):
        """
        The nodes of the network.

        :rtype: list()

        """
        return self._nodes

    @property
    def nodesCount(self):
        """
        The nodes count of the network.

        :rtype: int

        """
        return len(self.nodes)

    @property
    def sleeping_nodes_count(self):
        """
        The count of sleeping nodes on the network.

        :rtype: int

        """
        retval = 0
        for node in self.nodes:
            if node.isSleeping:
                retval += 1
        return retval - 1 if retval > 0 else 0

    def zwcallback(self, args):
        """
        The callback function used with the libopenzwave.

        n['valueId'] = {'home_id' : v.GetHomeId(),
                'node_id' : v.GetNodeId(),
                'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
                'instance' : v.GetInstance(),
                'index' : v.GetIndex(),
                'id' : v.GetId(),
                'genre' : PyGenres[v.GetGenre()],
                'type' : PyValueTypes[v.GetType()],
#                    'value' : value.c_str(),
                'value' : getValueFromType(manager,v.GetId()),
                'label' : label.c_str(),
                'units' : units.c_str(),
                'readOnly': manager.IsValueReadOnly(v),
                }

        :param args: Callback parameters
        :type args: dict()

        """
        try:
            notifyType = args['notificationType']
            if notifyType == 'DriverFailed':
                self._handle_driver_failed(args)
            elif notifyType == 'DriverReady':
                self._handle_driver_ready(args)
            elif notifyType == 'DriverReset':
                self._handleDriverReset(args)
            elif notifyType in 'NodeAdded':
                self._handleNodeAdded(args)
            elif notifyType in 'NodeChanged':
                self._handleNodeChanged(args)
            elif notifyType in 'NodeEvent':
                self._handleNodeEvent(args)
            elif notifyType in 'NodeNaming':
                self._handleNodeNaming(args)
            elif notifyType in 'NodeNew':
                self._handleNodeNew(args)
            elif notifyType in 'NodeProtocolInfo':
                self._handleNodeProtocolInfo(args)
            elif notifyType in 'NodeReady':
                self._handleNodeReady(args)
            elif notifyType in 'NodeRemoved':
                self._handleNodeRemoved(args)
            elif notifyType == 'ValueAdded':
                self._handleValueAdded(args)
            elif notifyType == 'ValueChanged':
                self._handleValueChanged(args)
            elif notifyType == 'valueRefreshed':
                self._handleValueRefreshed(args)
            elif notifyType == 'ValueRemoved':
                self._handleValueRemoved(args)
            elif notifyType in 'PollingDisabled':
                self._handlePollingDisabled(args)
            elif notifyType in 'PollingEnabled':
                self._handlePollingEnabled(args)
            elif notifyType in 'CreateButton':
                self._handleCreateButton(args)
            elif notifyType in 'DeleteButton':
                self._handleDeleteButton(args)
            elif notifyType in 'ButtonOn':
                self._handleButtonOn(args)
            elif notifyType in 'ButtonOff':
                self._handleButtonOff(args)
            elif notifyType in 'AllNodesQueried':
                self._handleAllNodesQueried(args)
            elif notifyType in 'AwakeNodesQueried':
                self._handleAwakeNodesQueried(args)
            elif notifyType == 'EssentialNodeQueriesComplete':
                self._handleEssentialNodeQueriesComplete(args)
            elif notifyType == 'NodeQueriesComplete':
                self._handleNodeQueriesComplete(args)
            elif notifyType in 'MsgComplete':
                self._handleMsgComplete(args)
            elif notifyType in 'Error':
                self._handleError(args)
            else:
                logging.warning('Skipping unhandled notification type [%s]', notifyType)
        except:
            import sys, traceback
            raise ZWaveException("Callback exception %s" % traceback.format_exception(*sys.exc_info()))

    def _zwcallback(self, args):
        '''
        Callback Handler

        n['valueId'] = {'home_id' : v.GetHomeId(),
                'node_id' : v.GetNodeId(),
                'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
                'instance' : v.GetInstance(),
                'index' : v.GetIndex(),
                'id' : v.GetId(),
                'genre' : PyGenres[v.GetGenre()],
                'type' : PyValueTypes[v.GetType()],
#                    'value' : value.c_str(),
                'value' : getValueFromType(manager,v.GetId()),
                'label' : label.c_str(),
                'units' : units.c_str(),
                'readOnly': manager.IsValueReadOnly(v),
                }

        :param args: Callback function
        :type args: dict()

        '''

    def _handle_driver_failed(self, args):
        '''
        Driver failed to load.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.error('Z-Wave Notification DriverFailed : %s' % (args))
        raise ZWaveException("Fail to load driver %s" % 1)

    def _handle_driver_ready(self, args):
        '''
        A driver for a PC Z-Wave controller has been added and is ready to use.
        The notification will contain the controller's Home ID,
        which is needed to call most of the Manager methods.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification DriverReady : %s' % (args))
        self._object_id = args['home_id']
        self._controller.node = ZWaveNode(args['node_id'], network=self)
        self.nodes = list()
        self.nodes.append(self._controller.node)
        logging.info('Driver ready using library %s' % self._controller.library_description )
        logging.info('home_id 0x%0.8x, controller node id is %d' % (self.home_id, self._controller.node_id))

    def _handleDriverReset(self, args):
        '''
        All nodes and values for this driver have been removed.
        This is sent instead of potentially hundreds of individual node
        and value notifications.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification Driver Reset : %s' % (args))

    def _handleNodeAdded(self, args):
        '''
        A new node has been added to OpenZWave's list.
        This may be due to a device being added to the Z-Wave network,
        or because the application is initializing itself.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeAdded : %s' % (args))

    def _handleNodeEvent(self, args):
        '''
        A node has triggered an event.  This is commonly caused when a
        node sends a Basic_Set command to the controller.
        The event value is stored in the notification.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeEvent : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleNodeNaming(self, args):
        '''
        One of the node names has changed (name, manufacturer, product).

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeNaming : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleNodeNew(self, args):
        '''
        A new node has been found (not already stored in zwcfg*.xml file).

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeNew : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleNodeProtocolInfo(self, args):
        '''
        Basic node information has been received, such as whether
        the node is a listening device, a routing device and its baud rate
        and basic, generic and specific types.
        It is after this notification that you can call Manager::GetNodeType
        to obtain a label containing the device description.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeProtocolInfo : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleNodeRemoved(self, args):
        '''
        A node has been removed from OpenZWave's list.
        This may be due to a device being removed from the Z-Wave network,
        or because the application is closing.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeRemoved : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleAllNodesQueried(self, args):
        '''
        All nodes have been queried, so client application can expected
        complete data.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification AllNodesQueried : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleAwakeNodesQueried(self, args):
        '''
        All awake nodes have been queried, so client application can
        expected complete data for these nodes.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification AwakeNodesQueried : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleEssentialNodeQueriesComplete(self, args):
        '''
        The queries on a node that are essential to its operation have
        been completed. The node can now handle incoming messages.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification EssentialNodeQueriesComplete : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleNodeQueriesComplete(self, args):
        '''
        All the initialisation queries on a node have been completed.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeQueriesComplete : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handlePollingDisabled(self, args):
        '''
        Polling of a node has been successfully turned off by a call
        to Manager::DisablePoll.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification PollingDisabled : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handlePollingEnabled(self, args):
        '''
        Polling of a node has been successfully turned on by a call
        to Manager::EnablePoll.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification PollingEnabled : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleCreateButton(self, args):
        '''
        Handheld controller button event created.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification CreateButton : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleDeleteButton(self, args):
        '''
        Handheld controller button event deleted.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification DeleteButton : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleButtonOn(self, args):
        '''
        Handheld controller button on pressed event.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ButtonOn : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleButtonOff(self, args):
        '''
        Handheld controller button off pressed event.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ButtonOff : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleValueAdded(self, args):
        '''
        A new node value has been added to OpenZWave's list.
        These notifications occur after a node has been discovered,
        and details of its command classes have been received.
        Each command class may generate one or more values depending
        on the complexity of the item being represented.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ValueAdded : %s' % (args))
        home_id = args['home_id']
        controllerNodeId = args['node_id']
        valueId = args['valueId']
        node = self._fetchNode(home_id, controllerNodeId)
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(home_id, controllerNodeId, valueId)
        valueNode.update(args)

    def _handleValueChanged(self, args):
        '''
        A node value has been updated from the Z-Wave network and it is
        different from the previous value.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ValueChanged : %s' % (args))
        home_id = args['home_id']
        controllerNodeId = args['node_id']
        valueId = args['valueId']
        node = self._fetchNode(home_id, controllerNodeId)
        node._sleeping = False
        node._lastUpdate = time.time()
        valueNode = self._getValueNode(home_id, controllerNodeId, valueId)
        valueNode.update(args)
        #if self._initialized:
        #    dispatcher.send(self.SIGNAL_VALUE_CHANGED, \
        #    **{'home_id': home_id, 'node_id': controllerNodeId, 'valueId': valueId})

    def _handleValueRefreshed(self, args):
        '''
        A node value has been updated from the Z-Wave network.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ValueRefreshed : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleValueRemoved(self, args):
        '''
        A node value has been removed from OpenZWave's list.
        This only occurs when a node is removed.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ValueRemoved : %s' % (args))
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleError(self, args):
        '''
        Called when a node query is complete.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification Error : %s' % (args))
        #dispatcher.send(self.SIGNAL_ERROR, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _handleMsgComplete(self, args):
        '''
        The last message that was sent is now complete.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification MsgComplete : %s' % (args))
        #dispatcher.send(self.SIGNAL_ERROR, **{'home_id': self._home_id, 'node_id': args['node_id']})

    def _getValueNode(self, home_id, node_id, valueId):
        """
        """
        node = self._getNode(home_id, node_id)
        if node is None:
            raise ZWaveException('Value received before node creation node_id %d' % (node_id))
        vid = valueId['id']
        if node._values.has_key(vid):
            retval = node._values[vid]
        else:
            retval = ZWaveValueNode(home_id, node_id, valueId)
            self._log.debug('Created new value node with home_id %0.8x, ' + \
                'node_id %d, valueId %s' % (home_id, node_id, valueId))
            node._values[vid] = retval
        return retval

    def _updateNodeCommandClasses(self, node):
        '''
        Update node's command classes.
        '''
        classSet = list()()
        for cls in PyManager.COMMAND_CLASS_DESC:
            if self._manager.getNodeClassInformation(node._home_id, node._node_id, cls):
                classSet.add(cls)
        node._commandClasses = classSet
        self._log.debug('Node [%d] command classes are: %s' % \
            (node._node_id, node._commandClasses))
        # TODO: add command classes as string

    def _handleInitializationComplete(self, args):
        """
        """
        logging.debug('Controller capabilities are: %s' % self.manager.controller.capabilities)
        logging.info("Initialization completed.  Found %s Z-Wave Device Nodes (%s sleeping)" % \
            (self.nodesCount, self.sleeping_nodes_count))
        self._initialized = True
        #dispatcher.send(self.SIGNAL_SYSTEM_READY, **{'home_id': self._home_id})
        self.manager.writeConfig(self._home_id)
        # TODO: write config on shutdown as well

    def setNodeOn(self, node):
        """
        """
        self._log.debug('Requesting setNodeOn for node {0}'.format(node.id))
        self._manager.setNodeOn(node.home_id, node.id)

    def setNodeOff(self, node):
        """
        """
        self._log.debug('Requesting setNodeOff for node {0}'.format(node.id))
        self._manager.setNodeOff(node.home_id, node.id)

    def setNodeLevel(self, node, level):
        """
        """
        self._log.debug('Requesting setNodeLevel for node {0} with new level {1}'.format(node.id, level))
        self._manager.setNodeLevel(node.home_id, node.id, level)

    def getCommandClassName(self, commandClassCode):
        """
        """
        return PyManager.COMMAND_CLASS_DESC[commandClassCode]

    def getCommandClassCode(self, commandClassName):
        """
        """
        for k, v in PyManager.COMMAND_CLASS_DESC.iteritems():
            if v == commandClassName:
                return k
        return None

# commands:
# - refresh node
# - request node state
# - request config param/request all config params
# - set node level
# - set node on/off
# - switch all on/off
# - add node, remove node (needs command support)

# editing:
# - add association, remove association
# - set config param
# - set node manufacturer name
# - set node name
# - set node location
# - set node product name
# - set poll interval
# - set wake up interval (needs command support)

# questions:
# - can powerlevel be queried directly? See PowerLevel.cpp in command classes
# - need more detail about notification events!
# - what is COMMAND_CLASS_HAIL used for?
# - what is COMMAND_CLASS_INDICATOR used for?
# - wake up duration sent via COMMAND_CLASS_WAKE_UP

#   initialization callback sequence:
#
#   [driverReady]
#
#   [nodeAdded] <-------------------------+ This cycle is extremely quick, well under one second.
#       [nodeProtocolInfo]                |
#       [nodeNaming]                      |
#       [valueAdded] <---------------+    |
#                                    |    |
#       {REPEATS FOR EACH VALUE} ----+    |
#                                         |
#       [group] <--------------------+    |
#                                    |    |
#       {REPEATS FOR EACH GROUP} ----+    |
#                                         |
#   {REPEATS FOR EACH NODE} --------------+
#
#   [? (no notification)] <---------------+ (no notification announces the beginning of this cycle)
#                                         |
#       [valueChanged] <-------------+    | This cycle can take some time, especially if some nodes
#                                    |    | are sleeping or slow to respond.
#       {REPEATS FOR EACH VALUE} ----+    |
#                                         |
#       [group] <--------------------+    |
#                                    |    |
#       {REPEATS FOR EACH GROUP} ----+    |
#                                         |
#   [nodeQueriesComplete]                 |
#                                         |
#   {REPEATS FOR EACH NODE} --------------+
#
#   [awakeNodesQueried] or [allNodesQueried] (with node_id 255)
