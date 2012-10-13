# -*- coding: utf-8 -*-
"""
.. module:: openzwave.network

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
from collections import namedtuple
import thread
import time
from louie import dispatcher, All
import logging
import threading
import libopenzwave
import openzwave
from openzwave.object import ZWaveException, ZWaveTypeException, ZWaveObject, NullLoggingHandler
from openzwave.controller import ZWaveController
from openzwave.node import ZWaveNode
from openzwave.option import ZWaveOption

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class ZWaveNetwork(ZWaveObject):
    '''
    The network objet = homeid.
    It contains a reference to the manager and the controller.

    It dispatch the following louie signals :

        * SIGNAL_NETWORK_FAILED = 'NetworkFailed'
        * SIGNAL_NETWORK_READY = 'NetworkReady'
        * SIGNAL_DRIVER_FAILED = 'DriverFailed'
        * SIGNAL_DRIVER_READY = 'DriverReady'
        * SIGNAL_DRIVER_RESET = 'DriverReset'
        * SIGNAL_NODE_ADDED = 'NodeAdded'
        * SIGNAL_NODE_EVENT = 'NodeEvent'
        * SIGNAL_NODE_NAMING = 'NodeNaming'
        * SIGNAL_NODE_NEW = 'NodeNew'
        * SIGNAL_NODE_PROTOCOL_INFO = 'NodeProtocolInfo'
        * SIGNAL_NODE_READY = 'NodeReady'
        * SIGNAL_NODE_REMOVED = 'NodeRemoved'
        * SIGNAL_VALUE_ADDED = 'ValueAdded'
        * SIGNAL_VALUE_CHANGED = 'ValueChanged'
        * SIGNAL_VALUE_REFRESHED = 'ValueRefreshed'
        * SIGNAL_VALUE_REMOVED = 'ValueRemoved'
        * SIGNAL_POLLING_ENABLED = 'PollingEnabled'
        * SIGNAL_POLLING_DISABLED = 'PollingDisabled'
        * SIGNAL_CREATE_BUTTON = 'CreateButton'
        * SIGNAL_DELETE_BUTTON = 'DeleteButton'
        * SIGNAL_BUTTON_ON = 'ButtonOn'
        * SIGNAL_BUTTON_OFF = 'ButtonOff'
        * SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE = 'EssentialNodeQueriesComplete'
        * SIGNAL_NODE_QUERIES_COMPLETE = 'NodeQueriesComplete'
        * SIGNAL_AWAKE_NODES_QUERIES_COMPLETE = 'AwakeNodeQueriesComplete'
        * SIGNAL_ALL_NODES_QUERIES_COMPLETE = 'AllNodeQueriesComplete'
        * SIGNAL_MSG_COMPLETE = 'MsgComplete'
        * SIGNAL_ERROR = 'Error'

    The table presented below sets notifications in the order they might typically be received,
    and grouped into a few logically related categories.  Of course, given the variety
    of ZWave controllers, devices and network configurations the actual sequence will vary (somewhat).
    The descriptions below the notification name (in square brackets) identify whether the
    notification is always sent (unless there’s a significant error in the network or software)
    or potentially sent during the execution sequence.

    Driver Initialization Notification

    The notification below is sent when OpenZWave has successfully connected
    to a physical ZWave controller.

    * DriverReady

    [always sent]   Sent when the driver (representing a connection between OpenZWave
    and a Z-Wave controller attached to the specified serial (or HID) port) has been initialized.
    At the time this notification is sent, only certain information about the controller itself is known:

        * Controller Z-Wave version
        * Network HomeID
        * Controller capabilities
        * Controller Application Version & Manufacturer/Product ID
        * Nodes included in the network

    Node Initialization Notifications

    As OpenZWave starts, it identifies and reads information about each node in the network.
    The following notifications may be sent during the initialization process.

    * NodeNew

    [potentially sent]  Sent when a new node has been identified as part of the Z-Wave network.
    It is not sent if the node was identified in a prior execution of the OpenZWave library
    and stored in the zwcfg*.xml file.
    At the time this notification is sent, very little is known about the node itself...
    only that it is new to OpenZWave. This message is sent once for each new node identified.

    * NodeAdded

    [always sent (for each node associated with the controller)]
    Sent when a node has been added to OpenZWave’s set of nodes.  It can be
    triggered either as the zwcfg*.xml file is being read, when a new node
    is found on startup (see NodeNew notification above), or if a new node
    is included in the network while OpenZWave is running.
    As with NodeNew, very little is known about the node at the time the
    notification is sent…just the fact that a new node has been identified
    and its assigned NodeID.

    * NodeProtocolInfo

    [potentially sent]  Sent after a node’s protocol information has been
    successfully read from the controller.
    At the time this notification is sent, only certain information about the node is known:

        * Whether it is a “listening” or “sleeping” device
        * Whether the node is capable of routing messages
        * Maximum baud rate for communication
        * Version number
        * Security byte

    NodeNaming

    [potentially sent]  Sent when a node’s name has been set or changed
    (although it may be “set” to “” or NULL).

    * ValueAdded

    [potentially sent]  Sent when a new value has been associated with the node.
    At the time this notification is sent, the new value may or may not
    have “live” data associated with it. It may be populated, but it may
    alternatively just be a placeholder for a value that has not been read
    at the time the notification is sent.

    * NodeQueriesComplete

    [always sent (for each node associated with the controller that has been successfully queried)]     Sent when a node’s values and attributes have been fully queried. At the time this notification is sent, the node’s information has been fully read at least once.  So this notification might trigger “full” display of the node’s information, values, etc. If this notification is not sent, it indicates that there has been a problem initializing the device.  The most common issue is that the node is a “sleeping” device.  The NodeQueriesComplete notification will be sent when the node wakes up and the query process completes.

    Initialization Complete Notifications

    As indicated above, when OpenZWave starts it reads certain information
    from a file, from the controller and from the network.  The following
    notifications identify when this initialization/querying process is complete.

    * AwakeNodesQueried

    [always sent]   Sent when all “listening” -always-on-devices have been
    queried successfully.  It also indicates, by implication, that there
    are some “sleeping” nodes that will not complete their queries until
    they wake up. This notification should be sent relatively quickly
    after start-up. (Of course, it depends on the number of devices on
    the ZWave network and whether there are any messages that “time out”
    without a proper response.)

    * AllNodesQueried

    [potentially sent]  Sent when all nodes have been successfully queried.

    This notification should be sent relatively quickly if there are
    no “sleeping” nodes. But it might be sent quite a while after start-up
    if there are sleeping nodes and at least one of these nodes has a long “wake-up” interval.

    Other Notifications

    In addition to the notifications described above, which are primarily
    “initialization” notifications that are sent during program start-up,
    the following notifications may be sent as a result of user actions,
    external program control, etc.

    * ValueChanged  Sent when a value associated with a node has changed. Receipt of this notification indicates that it may be a good time to read the new value and display or otherwise process it accordingly.
    * ValueRemoved  Sent when a value associated with a node has been removed.
    * Group     Sent when a node’s group association has changed.
    * NodeRemoved   Sent when a node has been removed from the ZWave network.
    * NodeEvent     Sent when a node sends a Basic_Set command to the controller.  This notification can be generated by certain sensors, for example, motion detectors, to indicate that an event has been sensed.
    * PollingEnabled    Sent when node/value polling has been enabled.
    * PollingDisabled   Sent when node/value polling has been disabled.
    * DriverReset   Sent to indicate when a controller has been reset.  This notification is intended to replace the potentially hundreds of notifications representing each value and node removed from the network.

    '''
    SIGNAL_NETWORK_FAILED = 'NetworkFailed'
    SIGNAL_NETWORK_READY = 'NetworkReady'
    SIGNAL_DRIVER_FAILED = 'DriverFailed'
    SIGNAL_DRIVER_READY = 'DriverReady'
    SIGNAL_DRIVER_RESET = 'DriverReset'
    SIGNAL_GROUP = 'Group'
    SIGNAL_NODE_ADDED = 'NodeAdded'
    SIGNAL_NODE_EVENT = 'NodeEvent'
    SIGNAL_NODE_NAMING = 'NodeNaming'
    SIGNAL_NODE_NEW = 'NodeNew'
    SIGNAL_NODE_PROTOCOL_INFO = 'NodeProtocolInfo'
    SIGNAL_NODE_READY = 'NodeReady'
    SIGNAL_NODE_REMOVED = 'NodeRemoved'
    SIGNAL_VALUE_ADDED = 'ValueAdded'
    SIGNAL_VALUE_CHANGED = 'ValueChanged'
    SIGNAL_VALUE_REFRESHED = 'ValueRefreshed'
    SIGNAL_VALUE_REMOVED = 'ValueRemoved'
    SIGNAL_POLLING_ENABLED = 'PollingEnabled'
    SIGNAL_POLLING_DISABLED = 'PollingDisabled'
    SIGNAL_CREATE_BUTTON = 'CreateButton'
    SIGNAL_DELETE_BUTTON = 'DeleteButton'
    SIGNAL_BUTTON_ON = 'ButtonOn'
    SIGNAL_BUTTON_OFF = 'ButtonOff'
    SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE = 'EssentialNodeQueriesComplete'
    SIGNAL_NODE_QUERIES_COMPLETE = 'NodeQueriesComplete'
    SIGNAL_AWAKE_NODES_QUERIES_COMPLETE = 'AwakeNodesQueriesComplete'
    SIGNAL_ALL_NODES_QUERIES_COMPLETE = 'AllNodeQueriesComplete'
    SIGNAL_MSG_COMPLETE = 'MsgComplete'
    SIGNAL_ERROR = 'Error'

    STATE_STOPPED = 0
    STATE_FAILED = 1
    STATE_RESET = 3
    STATE_INITIALISED = 5
    STATE_AWAKE = 7
    STATE_READY = 10

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
        ZWaveObject.__init__(self, None, self)
        self._controller = ZWaveController(1, self, options)
        self._manager = libopenzwave.PyManager()
        self._manager.create()
        self._manager.addWatcher(self.zwcallback)
        self._manager.addDriver(options.device)
        self._state = False
        #self._initialised = False
        #self._started = False
        #self._ready = False
        self._semaphore_nodes = threading.Semaphore()
        self.nodes = None
        #self._started = False

        #self._semaphore_on_ready = threading.Semaphore()
        #self._callback_on_ready = set()
        #self._semaphore_on_fail = threading.Semaphore()
        #self._callback_on_fail = set()

    @property
    def home_id(self):
        """
        The home_id of the network.

        :rtype: int

        """
        return self._object_id

    @home_id.setter
    def home_id(self, value):
        """
        The home_id of the network.

        :param value: new home_id
        :type value: int

        """
        self._object_id = value

#    @property
#    def initialised(self):
#        """
#        Says if the driver is ready.
#
#        :rtype: bool
#
#        """
#        return self._initialised
#
#    @property
#    def started(self):
#        """
#        Says if all the nodes are queried.
#
#        :rtype: bool
#
#        """
#        return self._started

    @property
    def is_ready(self):
        """
        Says if the network is ready for operations.

        :rtype: bool

        """
        return self._state>=self.STATE_READY

    @property
    def state(self):
        """
        The state of the network. Values may be changed in the future,
        only order is important.
        You can safely ask node informations when state >= STATE_READY

        * STATE_STOPPED = 0
        * STATE_FAILED = 1
        * STATE_RESET = 3
        * STATE_INITIALISED = 5
        * STATE_AWAKE = 7
        * STATE_READY = 10

        :rtype: int

        """
        return self._state

    @state.setter
    def state(self, value):
        """
        The state of the network. Values may be changed in the future,
        only order is important.

        * STATE_STOPPED = 0
        * STATE_FAILED = 1
        * STATE_RESET = 3
        * STATE_INITIALISED = 5
        * STATE_AWAKE = 7
        * STATE_READY = 10

        :param value: new state
        :type value: int

        """
        self._state = value

    @property
    def state_str(self):
        """
        The state of the network. Values may be changed in the future,
        only order is important.
        You can safely ask node informations when state >= STATE_READY

        :rtype: int

        """
        if self._state == 0:
            return "Network is stopped"
        elif self._state == 1:
            return "Driver failed"
        elif self._state == 2:
            return "Driver initialised"
        elif self._state == 4:
            return "Driver reseted"
        elif self._state == 7:
            return "Topology loaded"
        elif self._state == 10:
            return "Network ready"
        else:
            return "Unkown state"

    @property
    def manager(self):
        """
        The manager to use to communicate with the lib c++.

        :rtype: ZWaveManager

        """
        if self._manager != None and self._controller.node != None:
            return self._manager
        else:
            raise ZWaveException("Manager not initialised")

    @property
    def controller(self):
        """
        The controller of the network.

        :returns: The controller of the network
        :rtype: ZWaveController

        """
        if self._controller != None:
            return self._controller
        else:
            raise ZWaveException("Controller not initialised")

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

        :rtype: dict()

        """
        return self._nodes

    @nodes.setter
    def nodes(self, value):
        """
        The nodes of the network.

        :param value: The new value
        :type value: dict() or None

        """
        if value == None:
            self._nodes = dict()
        else:
            self._nodes = value

    @property
    def nodes_count(self):
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
            if node.is_sleeping:
                retval += 1
        return retval
#        return retval - 1 if retval > 0 else 0

    def zwcallback(self, args):
        """
        The Callback Handler used with the libopenzwave.

        n['valueId'] = {

            * 'home_id' : v.GetHomeId(),
            * 'node_id' : v.GetNodeId(),
            * 'commandClass' : PyManager.COMMAND_CLASS_DESC[v.GetCommandClassId()],
            * 'instance' : v.GetInstance(),
            * 'index' : v.GetIndex(),
            * 'id' : v.GetId(),
            * 'genre' : PyGenres[v.GetGenre()],
            * 'type' : PyValueTypes[v.GetType()],
            * #'value' : value.c_str(),
            * 'value' : getValueFromType(manager,v.GetId()),
            * 'label' : label.c_str(),
            * 'units' : units.c_str(),
            * 'readOnly': manager.IsValueReadOnly(v)

        }

        :param args: Callback function
        :type args: dict()

        """
        try:
            notify_type = args['notificationType']
            if notify_type == 'DriverFailed':
                self._handle_driver_failed(args)
            elif notify_type == 'DriverReady':
                self._handle_driver_ready(args)
            elif notify_type == 'DriverReset':
                self._handle_driver_reset(args)
            elif notify_type == 'NodeAdded':
                self._handle_node_added(args)
            elif notify_type == 'NodeChanged':
                self._handleNodeChanged(args)
            elif notify_type == 'NodeEvent':
                self._handle_node_event(args)
            elif notify_type == 'NodeNaming':
                self._handle_node_naming(args)
            elif notify_type == 'NodeNew':
                self._handle_node_new(args)
            elif notify_type == 'NodeProtocolInfo':
                self._handle_node_protocol_info(args)
            elif notify_type == 'NodeReady':
                self._handleNodeReady(args)
            elif notify_type == 'NodeRemoved':
                self._handle_node_removed(args)
            elif notify_type == 'Group':
                self._handle_group(args)
            elif notify_type == 'ValueAdded':
                self._handle_value_added(args)
            elif notify_type == 'ValueChanged':
                self._handle_value_changed(args)
            elif notify_type == 'valueRefreshed':
                self._handle_value_refreshed(args)
            elif notify_type == 'ValueRemoved':
                self._handle_value_removed(args)
            elif notify_type == 'PollingDisabled':
                self._handle_polling_disabled(args)
            elif notify_type == 'PollingEnabled':
                self._handle_polling_enabled(args)
            elif notify_type == 'CreateButton':
                self._handle_create_button(args)
            elif notify_type == 'DeleteButton':
                self._handle_delete_button(args)
            elif notify_type == 'ButtonOn':
                self._handle_button_on(args)
            elif notify_type == 'ButtonOff':
                self._handle_button_off(args)
            elif notify_type == 'AllNodesQueried':
                self._handle_all_nodes_queried(args)
            elif notify_type == 'AwakeNodesQueried':
                self._handle_awake_nodes_queried(args)
            elif notify_type == 'EssentialNodeQueriesComplete':
                self._handle_essential_node_queries_complete(args)
            elif notify_type == 'NodeQueriesComplete':
                self._handle_node_queries_complete(args)
            elif notify_type == 'MsgComplete':
                self._handle_msg_complete(args)
            elif notify_type == 'Error':
                self._handle_error(args)
            else:
                logging.warning('Skipping unhandled notification type [%s]', notify_type)
        except:
            import sys, traceback
            raise ZWaveException("Callback exception %s" % traceback.format_exception(*sys.exc_info()))

    def _handle_driver_failed(self, args):
        '''
        Driver failed to load.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.error('Z-Wave Notification DriverFailed : %s' % (args))
        self._manager = None
        self._controller = None
        self.nodes = None
        self._state = self.STATE_FAILED
        dispatcher.send(self.SIGNAL_DRIVER_FAILED, **{'network': self})
        dispatcher.send(self.SIGNAL_NETWORK_FAILED, **{'network': self})

    def _handle_driver_ready(self, args):
        '''
        A driver for a PC Z-Wave controller has been added and is ready to use.
        The notification will contain the controller's Home ID,
        which is needed to call most of the Manager methods.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification DriverReady : %s' % (args))
        self._object_id = args['homeId']
        try :
            self._controller.node = ZWaveNode(args['nodeId'], network=self)
            self._semaphore_nodes.acquire()
            self.nodes = None
            #print "nodes= ",self.nodes
            self.nodes[args['nodeId']] = self._controller.node
            self._state = self.STATE_INITIALISED
            logging.info('Driver ready using library %s' % self._controller.library_description )
            logging.info('home_id 0x%0.8x, controller node id is %d' % (self.home_id, self._controller.node_id))
            dispatcher.send(self.SIGNAL_DRIVER_READY, \
                **{'network': self, 'controller': self._controller})
        except:
            import sys, traceback
            logging.error('Z-Wave Notification DriverReady : %s' % (traceback.format_exception(*sys.exc_info())))
        finally :
            self._semaphore_nodes.release()

    def _handle_driver_reset(self, args):
        '''
        All nodes and values for this driver have been removed.
        This is sent instead of potentially hundreds of individual node
        and value notifications.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification DriverReset : %s' % (args))
        try :
            self._semaphore_nodes.acquire()
            self.nodes = None
            self._state = self.STATE_RESET
            self.nodes[args['nodeId']] = self._controller.node
            dispatcher.send(self.SIGNAL_DRIVER_RESET, \
                **{'network': self, 'controller': self._controller})
        finally :
            self._semaphore_nodes.release()

    def _handle_group(self, args):
        '''
        The associations for the node have changed.
        The application should rebuild any group information
        it holds about the node.

        To do

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification Group : %s' % (args))
        #try :
        #    node = ZWaveNode(args['nodeId'], network=self)
        #    self._semaphore_nodes.acquire()
        #    self.nodes[args['nodeId']] = node
        #finally :
        #    self._semaphore_nodes.release()
        dispatcher.send(self.SIGNAL_GROUP, \
                **{'network': self, 'node': self.nodes[args['nodeId']]})

    def _handle_node_added(self, args):
        '''
        A new node has been added to OpenZWave's set.
        This may be due to a device being added to the Z-Wave network,
        or because the application is initializing itself.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeAdded : %s' % (args))
        try :
            node = ZWaveNode(args['nodeId'], network=self)
            self._semaphore_nodes.acquire()
            self.nodes[args['nodeId']] = node
            dispatcher.send(self.SIGNAL_NODE_ADDED, \
                **{'network': self, 'node': node})
        finally :
            self._semaphore_nodes.release()

    def _handle_node_event(self, args):
        '''
        A node has triggered an event.  This is commonly caused when a
        node sends a Basic_Set command to the controller.
        The event value is stored in the notification.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeEvent : %s' % (args))
        dispatcher.send(self.SIGNAL_NODE_EVENT, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})

    def _handle_node_naming(self, args):
        '''
        One of the node names has changed (name, manufacturer, product).

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeNaming : %s' % (args))
        self.nodes[args['nodeId']].outdate("self.name")
        dispatcher.send(self.SIGNAL_NODE_NAMING, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})

    def _handle_node_new(self, args):
        '''
        A new node has been found (not already stored in zwcfg*.xml file).

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeNew : %s' % (args))
        dispatcher.send(self.SIGNAL_NODE_NEW, \
            **{'network': self, 'node_id': args['nodeId']})

    def _handle_node_protocol_info(self, args):
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
        dispatcher.send(self.SIGNAL_NODE_PROTOCOL_INFO, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})

    def _handle_node_removed(self, args):
        '''
        A node has been removed from OpenZWave's set.
        This may be due to a device being removed from the Z-Wave network,
        or because the application is closing.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeRemoved : %s' % (args))
        try :
            self._semaphore_nodes.acquire()
            self.nodes[args['nodeId']] = ZWaveNode(args['nodeId'], network=self)
            dispatcher.send(self.SIGNAL_NODE_REMOVED, \
                **{'network': self, 'node_id': args['nodeId']})
        finally :
            self._semaphore_nodes.release()

    def _handle_essential_node_queries_complete(self, args):
        '''
        The queries on a node that are essential to its operation have
        been completed. The node can now handle incoming messages.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification EssentialNodeQueriesComplete : %s' % (args))
        self.nodes[args['nodeId']].outdated = True
        dispatcher.send(self.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})

    def _handle_node_queries_complete(self, args):
        '''
        All the initialisation queries on a node have been completed.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification NodeQueriesComplete : %s' % (args))
        self.nodes[args['nodeId']].outdated = True
        dispatcher.send(self.SIGNAL_NODE_QUERIES_COMPLETE, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})

    def _handle_all_nodes_queried(self, args):
        '''
        All nodes have been queried, so client application can expected
        complete data.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification AllNodesQueried : %s' % (args))
        self._state = self.STATE_READY
        dispatcher.send(self.SIGNAL_NETWORK_READY, **{'network': self})
        dispatcher.send(self.SIGNAL_ALL_NODES_QUERIES_COMPLETE, \
            **{'network': self, 'controller': self._controller})
        #try:
        #    self._semaphore_on_ready.acquire()
        #    for callback in self._callback_on_ready:
        #        callback(*args, **kwargs)
        #finally:
        #    self._semaphore_on_ready.release()
        #dispatcher.send(self.SIGNAL_NODE_READY, **{'home_id': self.home_id, 'node_id': args['nodeId']})

    def _handle_awake_nodes_queried(self, args):
        '''
        All awake nodes have been queried, so client application can
        expected complete data for these nodes.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification AwakeNodesQueried : %s' % (args))
        self._state = self.STATE_AWAKE
        self._state = self.STATE_READY
        dispatcher.send(self.SIGNAL_NETWORK_READY, **{'network': self})
        dispatcher.send(self.SIGNAL_AWAKE_NODES_QUERIES_COMPLETE, \
            **{'network': self, 'controller': self._controller})

    def _handle_polling_disabled(self, args):
        '''
        Polling of a node has been successfully turned off by a call
        to Manager::DisablePoll.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification PollingDisabled : %s' % (args))
        self.nodes[args['nodeId']].outdate("self.is_polled")
        dispatcher.send(self.SIGNAL_POLLING_DISABLED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_polling_enabled(self, args):
        '''
        Polling of a node has been successfully turned on by a call
        to Manager::EnablePoll.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification PollingEnabled : %s' % (args))
        self.nodes[args['nodeId']].outdate("self.is_polled")
        dispatcher.send(self.SIGNAL_POLLING_ENABLED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_create_button(self, args):
        '''
        Handheld controller button event created.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification CreateButton : %s' % (args))
        dispatcher.send(self.SIGNAL_CREATE_BUTTON, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_delete_button(self, args):
        '''
        Handheld controller button event deleted.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification DeleteButton : %s' % (args))
        dispatcher.send(self.SIGNAL_DELETE_BUTTON, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_button_on(self, args):
        '''
        Handheld controller button on pressed event.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ButtonOn : %s' % (args))
        dispatcher.send(self.SIGNAL_BUTTON_ON, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_button_off(self, args):
        '''
        Handheld controller button off pressed event.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ButtonOff : %s' % (args))
        dispatcher.send(self.SIGNAL_BUTTON_OFF, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_value_added(self, args):
        '''
        A new node value has been added to OpenZWave's set.
        These notifications occur after a node has been discovered,
        and details of its command classes have been received.
        Each command class may generate one or more values depending
        on the complexity of the item being represented.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ValueAdded : %s' % (args))
        self.nodes[args['nodeId']].add_value(args['valueId']['id'], \
            args['valueId']['commandClass'])
        dispatcher.send(self.SIGNAL_VALUE_ADDED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})

    def _handle_value_changed(self, args):
        '''
        A node value has been updated from the Z-Wave network and it is
        different from the previous value.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ValueChanged : %s' % (args))
        self.nodes[args['nodeId']].change_value(args['valueId']['id'])
        dispatcher.send(self.SIGNAL_VALUE_CHANGED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})

    def _handle_value_refreshed(self, args):
        '''
        A node value has been updated from the Z-Wave network.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ValueRefreshed : %s' % (args))
        self.nodes[args['nodeId']].refresh_value(args['valueId']['id'])
        dispatcher.send(self.SIGNAL_VALUE_REFRESHED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})

    def _handle_value_removed(self, args):
        '''
        A node value has been removed from OpenZWave's set.
        This only occurs when a node is removed.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification ValueRemoved : %s' % (args))
        self.nodes[args['nodeId']].remove_value(args['valueId']['id'])
        dispatcher.send(self.SIGNAL_VALUE_REMOVED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value_id' : args['valueId']['id']})

    def _handle_error(self, args):
        '''
        Called when an error happened.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification Error : %s' % (args))
        dispatcher.send(self.SIGNAL_ERROR, \
            **{'network': self})

    def _handle_msg_complete(self, args):
        '''
        The last message that was sent is now complete.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Z-Wave Notification MsgComplete : %s' % (args))
        dispatcher.send(self.SIGNAL_MSG_COMPLETE, \
            **{'network': self})

    def write_config(self):
        '''
        The last message that was sent is now complete.

        :param args: data sent by the notification
        :type args: dict()

        '''
        logging.debug('Write ZWave configuration.')
        self._manager.writeConfig(self.home_id)
        logging.info('ZWave configuration wrote to user directory.')

#    def register_on_ready(self, callback):
#        '''
#        Register a callback function to the on_ready event.
#
#        :param callback: The callback function
#        :type callback: lambda
#
#        '''
#        logging.debug('Register on ready callback : %s' % (callback))
#        #dispatcher.send(self.SIGNAL_ERROR, **{'home_id': self.home_id, 'node_id': args['nodeId']})
#        try:
#            self._semaphore_on_ready.acquire()
#            self._callback_on_ready.append(callback)
#        finally:
#            self._semaphore_on_ready.release()
#
#    def register_on_fail(self, callback):
#        '''
#        Register a callback function to the on_fail event.
#
#        :param callback: The callback function
#        :type callback: lambda
#
#        '''
#        logging.debug('Register on fail callback : %s' % (callback))
#        #dispatcher.send(self.SIGNAL_ERROR, **{'home_id': self.home_id, 'node_id': args['nodeId']})
#        try:
#            self._semaphore_on_fail.acquire()
#            self._callback_on_fail.append(callback)
#        finally:
#            self._semaphore_on_fail.release()

#    def get_node(self, node_id):
#        """
#        Retrieve a node from its id.
#        This function does NOT lock the nodes set.
#
#        :param node_id: The node identifier
#        :type node_id: int
#        :returns: The ZWaveNode object or None
#        :rtype: ZWaveNode
#
#        """
#        node = self._getNode(home_id, node_id)
#        if node is None:
#            raise ZWaveException('Value received before node creation node_id %d' % (node_id))
#        vid = valueId['id']
#        if node._values.has_key(vid):
#            retval = node._values[vid]
#        else:
#            retval = ZWaveValueNode(home_id, node_id, valueId)
#            self._log.debug('Created new value node with home_id %0.8x, ' + \
#                'node_id %d, valueId %s' % (home_id, node_id, valueId))
#            node._values[vid] = retval
#        return retval

#    def _get_value_node(self, home_id, node_id, valueId):
#        """
#        """
#        node = self._getNode(home_id, node_id)
#        if node is None:
#            raise ZWaveException('Value received before node creation node_id %d' % (node_id))
#        vid = valueId['id']
#        if node._values.has_key(vid):
#            retval = node._values[vid]
#        else:
#            retval = ZWaveValueNode(home_id, node_id, valueId)
#            self._log.debug('Created new value node with home_id %0.8x, ' + \
#                'node_id %d, valueId %s' % (home_id, node_id, valueId))
#            node._values[vid] = retval
#        return retval

#    def _updateNodeCommandClasses(self, node):
#        '''
#        Update node's command classes.
#        '''
#        classSet = set()()
#        for cls in PyManager.COMMAND_CLASS_DESC:
#            if self._manager.getNodeClassInformation(node._home_id, node._node_id, cls):
#                classSet.add(cls)
#        node._commandClasses = classSet
#        self._log.debug('Node [%d] command classes are: %s' % \
#            (node._node_id, node._commandClasses))
#        # TODO: add command classes as string

#    def _handleInitializationComplete(self, args):
#        """
#        """
#        logging.debug('Controller capabilities are: %s' % self.manager.controller.capabilities)
#        logging.info("Initialization completed.  Found %s Z-Wave Device Nodes (%s sleeping)" % \
#            (self.nodesCount, self.sleeping_nodes_count))
#        self._initialized = True
#        #dispatcher.send(self.SIGNAL_SYSTEM_READY, **{'home_id': self.home_id})
#        self.manager.writeConfig(self.home_id)
#        # TODO: write config on shutdown as well

#    def getCommandClassName(self, commandClassCode):
#        """
#        """
#        return PyManager.COMMAND_CLASS_DESC[commandClassCode]

#    def getCommandClassCode(self, commandClassName):
#        """
#        """
#        for k, v in PyManager.COMMAND_CLASS_DESC.iteritems():
#            if v == commandClassName:
#                return k
#        return None

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

"""
   initialization callback sequence:

   [driverReady]

   [nodeAdded] <-------------------------+ This cycle is extremely quick, well under one second.
       [nodeProtocolInfo]                |
       [nodeNaming]                      |
       [valueAdded] <---------------+    |
                                    |    |
       {REPEATS FOR EACH VALUE} ----+    |
                                         |
       [group] <--------------------+    |
                                    |    |
       {REPEATS FOR EACH GROUP} ----+    |
                                         |
   {REPEATS FOR EACH NODE} --------------+

   [? (no notification)] <---------------+ (no notification announces the beginning of this cycle)
                                         |
       [valueChanged] <-------------+    | This cycle can take some time, especially if some nodes
                                    |    | are sleeping or slow to respond.
       {REPEATS FOR EACH VALUE} ----+    |
                                         |
       [group] <--------------------+    |
                                    |    |
       {REPEATS FOR EACH GROUP} ----+    |
                                         |
   [nodeQueriesComplete]                 |
                                         |
   {REPEATS FOR EACH NODE} --------------+

   [awakeNodesQueried] or [allNodesQueried] (with node_id 255)
"""
