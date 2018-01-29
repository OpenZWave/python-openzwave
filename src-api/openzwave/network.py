# -*- coding: utf-8 -*-
"""
.. module:: openzwave.network

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
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
import os
#from collections import namedtuple
import time
import sys
import six
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher
import threading

import libopenzwave
import openzwave
from openzwave.object import ZWaveException, ZWaveTypeException, ZWaveObject
from openzwave.controller import ZWaveController
from openzwave.node import ZWaveNode
from openzwave.option import ZWaveOption
from openzwave.scene import ZWaveScene
from openzwave.singleton import Singleton

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

try:
    import sqlite3 as lite
except ImportError:
    logger.warning('pysqlite is not installed')

class ZWaveNetwork(ZWaveObject):
    """
    The network object = homeid.
    It contains a reference to the manager and the controller.

    It dispatches the following louie signals :

        * SIGNAL_NETWORK_FAILED = 'NetworkFailed'
        * SIGNAL_NETWORK_STARTED = 'NetworkStarted'
        * SIGNAL_NETWORK_READY = 'NetworkReady'
        * SIGNAL_NETWORK_STOPPED = 'NetworkStopped'
        * SIGNAL_NETWORK_RESETTED = 'DriverResetted'
        * SIGNAL_NETWORK_AWAKED = 'DriverAwaked'
        * SIGNAL_DRIVER_FAILED = 'DriverFailed'
        * SIGNAL_DRIVER_READY = 'DriverReady'
        * SIGNAL_DRIVER_RESET = 'DriverReset'
        * SIGNAL_DRIVER_REMOVED = 'DriverRemoved'
        * SIGNAL_NODE_ADDED = 'NodeAdded'
        * SIGNAL_NODE_EVENT = 'NodeEvent'
        * SIGNAL_NODE_NAMING = 'NodeNaming'
        * SIGNAL_NODE_NEW = 'NodeNew'
        * SIGNAL_NODE_PROTOCOL_INFO = 'NodeProtocolInfo'
        * SIGNAL_NODE_READY = 'NodeReady'
        * SIGNAL_NODE_REMOVED = 'NodeRemoved'
        * SIGNAL_SCENE_EVENT = 'SceneEvent'
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
        * SIGNAL_AWAKE_NODES_QUERIED = 'AwakeNodesQueried'
        * SIGNAL_ALL_NODES_QUERIED = 'AllNodesQueried'
        * SIGNAL_ALL_NODES_QUERIED_SOME_DEAD = 'AllNodesQueriedSomeDead'
        * SIGNAL_MSG_COMPLETE = 'MsgComplete'
        * SIGNAL_ERROR = 'Error'
        * SIGNAL_NOTIFICATION = 'Notification'
        * SIGNAL_CONTROLLER_COMMAND = 'ControllerCommand'
        * SIGNAL_CONTROLLER_WAITING = 'ControllerWaiting'

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

    * DriverRemoved

    [always sent (either due to Error or by request)] The Driver is being removed.
    Do Not Call Any Driver Related Methods after receiving this

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

    * ValueChanged : Sent when a value associated with a node has changed. Receipt of this notification indicates that it may be a good time to read the new value and display or otherwise process it accordingly.
    * ValueRemoved : Sent when a value associated with a node has been removed.
    * Group : Sent when a node’s group association has changed.
    * NodeRemoved : Sent when a node has been removed from the ZWave network.
    * NodeEvent : Sent when a node sends a Basic_Set command to the controller. This notification can be generated by certain sensors, for example, motion detectors, to indicate that an event has been sensed.
    * PollingEnabled : Sent when node/value polling has been enabled.
    * PollingDisabled : Sent when node/value polling has been disabled.
    * DriverReset : Sent to indicate when a controller has been reset. This notification is intended to replace the potentially hundreds of notifications representing each value and node removed from the network.

    About the use of louie signals :
    For network, python-openzwave send the following louie signal :

        SIGNAL_NETWORK_FAILED : the driver has failed to start.
        SIGNAL_NETWORK_STARTED : the driver is ready, but network is not available.
        SIGNAL_NETWORK_AWAKED : all awake nodes are queried. Some sleeping nodes may be missing.
        SIGNAL_NETWORK_READY : all nodes are queried. Network is fully functionnal.
        SIGNAL_NETWORK_RESETTED : the network has been resetted. It will start again.
        SIGNAL_NETWORK_STOPPED : the network has been stopped.

    Deprecated : SIGNAL_DRIVER_* shouldn't be used anymore.

    """

    SIGNAL_NETWORK_FAILED = 'NetworkFailed'
    SIGNAL_NETWORK_STARTED = 'NetworkStarted'
    SIGNAL_NETWORK_READY = 'NetworkReady'
    SIGNAL_NETWORK_STOPPED = 'NetworkStopped'
    SIGNAL_NETWORK_RESETTED = 'DriverResetted'
    SIGNAL_NETWORK_AWAKED = 'DriverAwaked'
    SIGNAL_DRIVER_FAILED = 'DriverFailed'
    SIGNAL_DRIVER_READY = 'DriverReady'
    SIGNAL_DRIVER_RESET = 'DriverReset'
    SIGNAL_DRIVER_REMOVED = 'DriverRemoved'
    SIGNAL_GROUP = 'Group'
    SIGNAL_NODE = 'Node'
    SIGNAL_NODE_ADDED = 'NodeAdded'
    SIGNAL_NODE_EVENT = 'NodeEvent'
    SIGNAL_NODE_NAMING = 'NodeNaming'
    SIGNAL_NODE_NEW = 'NodeNew'
    SIGNAL_NODE_PROTOCOL_INFO = 'NodeProtocolInfo'
    SIGNAL_NODE_READY = 'NodeReady'
    SIGNAL_NODE_REMOVED = 'NodeRemoved'
    SIGNAL_SCENE_EVENT = 'SceneEvent'
    SIGNAL_VALUE = 'Value'
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
    SIGNAL_AWAKE_NODES_QUERIED = 'AwakeNodesQueried'
    SIGNAL_ALL_NODES_QUERIED = 'AllNodesQueried'
    SIGNAL_ALL_NODES_QUERIED_SOME_DEAD = 'AllNodesQueriedSomeDead'
    SIGNAL_MSG_COMPLETE = 'MsgComplete'
    SIGNAL_NOTIFICATION = 'Notification'
    SIGNAL_CONTROLLER_COMMAND = 'ControllerCommand'
    SIGNAL_CONTROLLER_WAITING = 'ControllerWaiting'

    STATE_STOPPED = 0
    STATE_FAILED = 1
    STATE_RESETTED = 3
    STATE_STARTED = 5
    STATE_AWAKED = 7
    STATE_READY = 10

    ignoreSubsequent = True

    def __init__(self, options, log=None, autostart=True, kvals=True):
        """
        Initialize zwave network

        :param options: Options to use with manager
        :type options: ZWaveOption
        :param log: A log file (not used. Deprecated
        :type log:
        :param autostart: should we start the network.
        :type autostart: bool
        :param kvals: Enable kvals (use pysqlite)
        :type kvals: bool

        """
        logger.debug("Create network object.")
        self.log = log
        self._options = options
        ZWaveObject.__init__(self, None, self)
        self._controller = ZWaveController(1, self, options)
        self._manager = libopenzwave.PyManager()
        self._manager.create()
        self._state = self.STATE_STOPPED
        self.nodes = None
        self._semaphore_nodes = threading.Semaphore()
        self._id_separator = '.'
        self.network_event = threading.Event()
        self.dbcon = None
        if kvals == True:
            try:
                self.dbcon = lite.connect(os.path.join(self._options.user_path, 'pyozw.sqlite'), check_same_thread=False)
                cur = self.dbcon.cursor()
                version = cur.execute('SELECT SQLITE_VERSION()').fetchone()
                logger.debug("Use sqlite version : %s", version)
                self._check_db_tables()
            except lite.Error as e:
                logger.warning("Can't connect to sqlite database : kvals are disabled - %s", e.args[0])
        self._started = False
        if autostart:
            self.start()

    def __str__(self):
        """
        The string representation of the node.

        :rtype: str

        """
        return u'home_id: [%s] controller: [%s]' % \
          (self.home_id_str, self.controller)

    def _check_db_tables(self):
        """
        Check that the tables for "classes" are in database.

        :returns: True if operation succeed. False oterwise
        :rtype: boolean

        """
        if self.dbcon is None:
            return False
        cur = self.dbcon.cursor()
        for mycls in ['ZWaveOption', 'ZWaveOptionSingleton', 'ZWaveNetwork', 'ZWaveNetworkSingleton', 'ZWaveNode', 'ZWaveController', 'ZWaveValue']:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (mycls,))
            data = cur.fetchone()
            if data is None:
                cur.execute("CREATE TABLE %s(object_id INT, key TEXT, value TEXT)" % mycls)
        return True

    def start(self):
        """
        Start the network object :
            - add a watcher
            - add a driver

        """
        if self._started == True:
            return
        logger.info(u"Start Openzwave network.")
        self._manager.addWatcher(self.zwcallback)
        self._manager.addDriver(self._options.device)
        self._started = True

    def stop(self, fire=True):
        """
        Stop the network object.

            - remove the watcher
            - remove the driver
            - clear the nodes

        .. code-block:: python

            dispatcher.send(self.SIGNAL_NETWORK_STOPPED, **{'network': self})

        """
        if self._started == False:
            return
        logger.info(u"Stop Openzwave network.")
        if self.controller is not None:
            self.controller.stop()
        self.write_config()
        try:
            self._semaphore_nodes.acquire()
            self._manager.removeWatcher(self.zwcallback)
            try:
                self.network_event.wait(1.0)
            except AssertionError:
                #For gevent AssertionError: Impossible to call blocking function in the event loop callback
                pass
            self._manager.removeDriver(self._options.device)
            try:
                self.network_event.wait(1.0)
            except AssertionError:
                #For gevent AssertionError: Impossible to call blocking function in the event loop callback
                pass
            for i in range(0, 60):
                if self.controller.send_queue_count <= 0:
                    break
                else:
                    try:
                        self.network_event.wait(1.0)
                    except AssertionError:
                        #For gevent AssertionError: Impossible to call blocking function in the event loop callback
                        pass
            self.nodes = None
        except:
            import sys, traceback
            logger.exception(u'Stop network : %s')
        finally:
            self._semaphore_nodes.release()
        self._started = False
        self._state = self.STATE_STOPPED
        try:
            self.network_event.wait(1.0)
        except AssertionError:
            #For gevent AssertionError: Impossible to call blocking function in the event loop callback
            pass
        if fire:
            dispatcher.send(self.SIGNAL_NETWORK_STOPPED, **{'network': self})

    def destroy(self):
        """
        Destroy the netwok and all related stuff.
        """
        if self.dbcon is not None:
            self.dbcon.commit()
            self.dbcon.close()
        self._manager.destroy()
        self._options.destroy()
        self._manager = None
        self._options = None

    @property
    def home_id(self):
        """
        The home_id of the network.

        :rtype: int

        """
        if self._object_id is None:
            return 0
        return self._object_id

    @home_id.setter
    def home_id(self, value):
        """
        The home_id of the network.

        :param value: new home_id
        :type value: int

        """
        self._object_id = value

    @property
    def home_id_str(self):
        """
        The home_id of the network as string.

        :rtype: str

        """
        return "0x%0.8x" % self.home_id

    @property
    def is_ready(self):
        """
        Says if the network is ready for operations.

        :rtype: bool

        """
        return self._state >= self.STATE_READY

    @property
    def state(self):
        """
        The state of the network. Values may be changed in the future,
        only order is important.
        You can safely ask node information when state >= STATE_READY

        * STATE_STOPPED = 0
        * STATE_FAILED = 1
        * STATE_RESETTED = 3
        * STATE_STARTED = 5
        * STATE_AWAKED = 7
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
        * STATE_RESETTED = 3
        * STATE_STARTED = 5
        * STATE_AWAKED = 7
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
        You can safely ask node informations when state >= STATE_AWAKED

        :rtype: int

        """
        if self._state == self.STATE_STOPPED:
            return "Network is stopped"
        elif self._state == self.STATE_FAILED:
            return "Driver failed"
        elif self._state == self.STATE_STARTED:
            return "Driver initialised"
        elif self._state == self.STATE_RESETTED:
            return "Driver is reset"
        elif self._state == self.STATE_AWAKED:
            return "Topology loaded"
        elif self._state == self.STATE_READY:
            return "Network ready"
        else:
            return "Unknown state"

    @property
    def manager(self):
        """
        The manager to use to communicate with the lib c++.

        :rtype: ZWaveManager

        """
        if self._manager is not None:
            return self._manager
        else:
            raise ZWaveException(u"Manager not initialised")

    @property
    def controller(self):
        """
        The controller of the network.

        :return: The controller of the network
        :rtype: ZWaveController

        """
        if self._controller is not None:
            return self._controller
        else:
            raise ZWaveException(u"Controller not initialised")

    @property
    def nodes(self):
        """
        The nodes of the network.

        :rtype: dict()

        """
        return self._nodes

    def nodes_to_dict(self, extras=['all']):
        """
        Return a dict representation of the network.

        :param extras: The extra inforamtions to add
        :type extras: []
        :returns: A dict
        :rtype: dict()

        """
        ret = {}
        for ndid in self._nodes.keys():
            ret[ndid]=self._nodes[ndid].to_dict(extras=extras)
        return ret

    def to_dict(self, extras=['kvals']):
        """
        Return a dict representation of the network.

        :param extras: The extra inforamtions to add
        :type extras: []
        :returns: A dict
        :rtype: dict()

        """
        ret = {}
        ret['state'] = self.state,
        ret['state_str'] = self.state_str,
        ret['home_id'] = self.home_id_str,
        ret['nodes_count'] = self.nodes_count,
        if 'kvals' in extras and self.network.dbcon is not None:
            vals = self.kvals
            for key in vals.keys():
                ret[key]=vals[key]
        return ret

    @nodes.setter
    def nodes(self, value):
        """
        The nodes of the network.

        :param value: The new value
        :type value: dict() or None

        """
        if type(value) == type(dict()):
            self._nodes = value
        else:
            self._nodes = dict()

    def switch_all(self, state):
        """
        Method for switching all devices on or off together.  The devices must support
        the SwitchAll command class.  The command is first broadcast to all nodes, and
        then followed up with individual commands to each node (because broadcasts are
        not routed, the message might not otherwise reach all the nodes).

        :param state: True to turn on the switches, False to turn them off
        :type state: bool

        """
        if state:
            self.manager.switchAllOn(self.home_id)
        else:
            self.manager.switchAllOff(self.home_id)

    def test(self, count=1):
        """
        Send a number of test messages to every node and record results.

        :param count: The number of test messages to send.
        :type count: int

        """
        self.manager.testNetwork(self.home_id, count)

    def heal(self, upNodeRoute=False):
        """
        Heal network by requesting nodes rediscover their neighbors.
        Sends a ControllerCommand_RequestNodeNeighborUpdate to every node.
        Can take a while on larger networks.

        :param upNodeRoute: Optional Whether to perform return routes initialization. (default = false).
        :type upNodeRoute: bool
        :return: True is the ControllerCommand ins sent. False otherwise
        :rtype: bool

        """
        if self.network.state < self.network.STATE_AWAKED:
            logger.warning(u'Network must be awake')
            return False
        self.manager.healNetwork(self.home_id, upNodeRoute)
        return True

    def get_value(self, value_id):
        """
        Retrieve a value on the network.

        Check every nodes to see if it holds the value

        :param value_id: The id of the value to find
        :type value_id: int
        :return: The value or None
        :rtype: ZWaveValue

        """
        for node in self.nodes:
            if value_id in self.nodes[node].values:
                return self.nodes[node].values[value_id]
        return None

    @property
    def id_separator(self):
        """
        The separator in id representation.

        :rtype: char

        """
        return self._id_separator

    @id_separator.setter
    def id_separator(self, value):
        """
        The nodes of the network.

        :param value: The new separator
        :type value: char

        """
        self._id_separator = value

    def get_value_from_id_on_network(self, id_on_network):
        """
        Retrieve a value on the network from it's id_on_network.

        Check every nodes to see if it holds the value

        :param id_on_network: The id_on_network of the value to find
        :type id_on_network: str
        :return: The value or None
        :rtype: ZWaveValue

        """
        for node in self.nodes.itervalues():
            for val in node.values.itervalues():
                if val.id_on_network == id_on_network:
                    return val
        return None

    def get_scenes(self):
        """
        The scenes of the network.

        Scenes are generated directly from the lib. There is no notification
        support to keep them up to date. So for a batch job, consider
        storing them in a local variable.

        :return: return a dict() (that can be empty) of scene object. Return None if betwork is not ready
        :rtype: dict() or None

        """
        if self.state < self.STATE_AWAKED:
            return None
        else:
            return self._load_scenes()

    def scenes_to_dict(self, extras=['all']):
        """
        Return a JSONifiable dict representation of the scenes.

        :param extras: The extra inforamtions to add
        :type extras: []
        :returns: A dict
        :rtype: dict()

        """
        ret={}
        scenes = self.get_scenes()
        for scnid in scenes.keys():
            ret[scnid] = scenes[scnid].to_dict(extras=extras)
        return ret

    def _load_scenes(self):
        """
        Load the scenes of the network.

        :return: return a dict() (that can be empty) of scene object.
        :rtype: dict()

        """
        ret = {}
        set_scenes = self._manager.getAllScenes()
        logger.debug(u'Load Scenes: %s', set_scenes)
        for scene_id in set_scenes:
            scene = ZWaveScene(scene_id, network=self)
            ret[scene_id] = scene
        return ret

    def create_scene(self, label=None):
        """
        Create a new scene on the network.
        If label is set, also change the label of the scene

        If you store your scenes on a local variable, get a new one
        to get the scene id

        :param label: The new label
        :type label: str or None
        :return: return the id of scene on the network. Return 0 if fails
        :rtype: int

        """
        scene = ZWaveScene(None, network=self)
        return scene.create(label)

    def scene_exists(self, scene_id):
        """
        Check that the scene exists

        :param scene_id: The id of the scene to check
        :type scene_id: int
        :return: True if the scene exist. False in other cases
        :rtype: bool

        """
        return self._network.manager.sceneExists(scene_id)

    @property
    def scenes_count(self):
        """
        Return the number of scenes

        :return: The number of scenes
        :rtype: int

        """
        return self._network.manager.getNumScenes()

    def remove_scene(self, scene_id):
        """
        Delete the scene on the network.

        :param scene_id: The id of the scene to check
        :type scene_id: int
        :return: True if the scene was removed. False in other cases
        :rtype: bool

        """
        return self._network.manager.removeScene(scene_id)

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
        result = 0
        for node in self.nodes:
            if node.is_sleeping:
                result += 1
        return result

    def get_poll_interval(self):
        """
        Get the time period between polls of a nodes state

        :return: The number of milliseconds between polls
        :rtype: int

        """
        return self.manager.getPollInterval()

    def set_poll_interval(self, milliseconds=500, bIntervalBetweenPolls=True):
        """
        Set the time period between polls of a nodes state.

        Due to patent concerns, some devices do not report state changes automatically
        to the controller.  These devices need to have their state polled at regular
        intervals.  The length of the interval is the same for all devices.  To even
        out the Z-Wave network traffic generated by polling, OpenZWave divides the
        polling interval by the number of devices that have polling enabled, and polls
        each in turn.  It is recommended that if possible, the interval should not be
        set shorter than the number of polled devices in seconds (so that the network
        does not have to cope with more than one poll per second).

        :param milliseconds: The length of the polling interval in milliseconds.
        :type milliseconds: int
        :param bIntervalBetweenPolls: If set to true (via SetPollInterval), the pollInterval will be interspersed between each poll (so a much smaller m_pollInterval like 100, 500, or 1,000 may be appropriate). If false, the library attempts to complete all polls within m_pollInterval.
        :type bIntervalBetweenPolls: bool

        """
        self.manager.setPollInterval(milliseconds, bIntervalBetweenPolls)

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

        :param args: A dict containing informations about the state of the controller
        :type args: dict()

        """
        logger.debug('zwcallback args=[%s]', args)
        try:
            notify_type = args['notificationType']
            if notify_type == self.SIGNAL_DRIVER_FAILED:
                self._handle_driver_failed(args)
            elif notify_type == self.SIGNAL_DRIVER_READY:
                self._handle_driver_ready(args)
            elif notify_type == self.SIGNAL_DRIVER_RESET:
                self._handle_driver_reset(args)
            elif notify_type == self.SIGNAL_NODE_ADDED:
                self._handle_node_added(args)
            elif notify_type == self.SIGNAL_NODE_EVENT:
                self._handle_node_event(args)
            elif notify_type == self.SIGNAL_NODE_NAMING:
                self._handle_node_naming(args)
            elif notify_type == self.SIGNAL_NODE_NEW:
                self._handle_node_new(args)
            elif notify_type == self.SIGNAL_NODE_PROTOCOL_INFO:
                self._handle_node_protocol_info(args)
            elif notify_type == self.SIGNAL_NODE_READY:
                self._handleNodeReady(args)
            elif notify_type == self.SIGNAL_NODE_REMOVED:
                self._handle_node_removed(args)
            elif notify_type == self.SIGNAL_GROUP:
                self._handle_group(args)
            elif notify_type == self.SIGNAL_SCENE_EVENT:
                self._handle_scene_event(args)
            elif notify_type == self.SIGNAL_VALUE_ADDED:
                self._handle_value_added(args)
            elif notify_type == self.SIGNAL_VALUE_CHANGED:
                self._handle_value_changed(args)
            elif notify_type == self.SIGNAL_VALUE_REFRESHED:
                self._handle_value_refreshed(args)
            elif notify_type == self.SIGNAL_VALUE_REMOVED:
                self._handle_value_removed(args)
            elif notify_type == self.SIGNAL_POLLING_DISABLED:
                self._handle_polling_disabled(args)
            elif notify_type == self.SIGNAL_POLLING_ENABLED:
                self._handle_polling_enabled(args)
            elif notify_type == self.SIGNAL_CREATE_BUTTON:
                self._handle_create_button(args)
            elif notify_type == self.SIGNAL_DELETE_BUTTON:
                self._handle_delete_button(args)
            elif notify_type == self.SIGNAL_BUTTON_ON:
                self._handle_button_on(args)
            elif notify_type == self.SIGNAL_BUTTON_OFF:
                self._handle_button_off(args)
            elif notify_type == self.SIGNAL_ALL_NODES_QUERIED:
                self._handle_all_nodes_queried(args)
            elif notify_type == self.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD:
                self._handle_all_nodes_queried_some_dead(args)
            elif notify_type == self.SIGNAL_AWAKE_NODES_QUERIED:
                self._handle_awake_nodes_queried(args)
            elif notify_type == self.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE:
                self._handle_essential_node_queries_complete(args)
            elif notify_type == self.SIGNAL_NODE_QUERIES_COMPLETE:
                self._handle_node_queries_complete(args)
            elif notify_type == self.SIGNAL_MSG_COMPLETE:
                self._handle_msg_complete(args)
            elif notify_type == self.SIGNAL_NOTIFICATION:
                self._handle_notification(args)
            elif notify_type == self.SIGNAL_DRIVER_REMOVED:
                self._handle_driver_removed(args)
            elif notify_type == self.SIGNAL_CONTROLLER_COMMAND:
                self._handle_controller_command(args)
            else:
                logger.warning(u'Skipping unhandled notification [%s]', args)
        except:
            import sys, traceback
            logger.exception(u'Error in manager callback')

    def _handle_driver_failed(self, args):
        """
        Driver failed to load.

        :param args: data sent by the notification
        :type args: dict()

        dispatcher.send(self.SIGNAL_NETWORK_FAILED, **{'network': self})

        """
        logger.warning(u'Z-Wave Notification DriverFailed : %s', args)
        self._manager = None
        self._controller = None
        self.nodes = None
        self._state = self.STATE_FAILED
        dispatcher.send(self.SIGNAL_DRIVER_FAILED, **{'network': self})
        dispatcher.send(self.SIGNAL_NETWORK_FAILED, **{'network': self})

    def _handle_driver_ready(self, args):
        """
        A driver for a PC Z-Wave controller has been added and is ready to use.
        The notification will contain the controller's Home ID,
        which is needed to call most of the Manager methods.

        dispatcher.send(self.SIGNAL_NETWORK_STARTED, **{'network': self, 'controller': self._controller})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification DriverReady : %s', args)
        self._object_id = args['homeId']
        try:
            controller_node = ZWaveNode(args['nodeId'], network=self)
            self._semaphore_nodes.acquire()
            self.nodes = None
            self.nodes[args['nodeId']] = controller_node
            self._controller.node = self.nodes[args['nodeId']]
            logger.info(u'Driver ready using library %s', self._controller.library_description)
            logger.info(u'home_id 0x%0.8x, controller node id is %d', self.home_id, self._controller.node_id)
            logger.debug(u'Network %s', self)
            #Not needed. Already sent by the lib
            #~ dispatcher.send(self.SIGNAL_DRIVER_READY, \
                #~ **{'network': self, 'controller': self._controller})
            self._state = self.STATE_STARTED
            dispatcher.send(self.SIGNAL_NETWORK_STARTED, \
                **{'network': self})
            ctrl_state = libopenzwave.PyControllerState[0]
            ctrl_message = libopenzwave.PyControllerState[0].doc
            dispatcher.send(self.controller.SIGNAL_CONTROLLER, \
                **{'state': ctrl_state, 'message': ctrl_message, 'network': self, 'controller': self.controller})
        except:
            import sys, traceback
            logger.exception('Z-Wave Notification DriverReady',)
        finally:
            self._semaphore_nodes.release()

    def _handle_driver_reset(self, args):
        """
        This notification is never fired.

        Look at
            and

        All nodes and values for this driver have been removed.
        This is sent instead of potentially hundreds of individual node
        and value notifications.

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification DriverReset : %s', args)
        try:
            self._semaphore_nodes.acquire()
            logger.debug(u'DriverReset received. Remove all nodes')
            self.nodes = None
            self._state = self.STATE_RESETTED
            dispatcher.send(self.SIGNAL_DRIVER_RESET, \
                **{'network': self})
            dispatcher.send(self.SIGNAL_NETWORK_RESETTED, \
                **{'network': self})
        finally:
            self._semaphore_nodes.release()

    def _handle_driver_removed(self, args):
        """
        The Driver is being removed. (either due to Error or by request)
        Do Not Call Any Driver Related Methods after receiving this

        dispatcher.send(self.SIGNAL_DRIVER_REMOVED, **{'network': self})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification DriverRemoved : %s', args)
        try:
            self._semaphore_nodes.acquire()
            self._state = self.STATE_STOPPED
            dispatcher.send(self.SIGNAL_DRIVER_REMOVED, \
                **{'network': self})
        finally:
            self._semaphore_nodes.release()

    def _handle_group(self, args):
        """
        The associations for the node have changed.
        The application should rebuild any group information
        it holds about the node.

        dispatcher.send(self.SIGNAL_GROUP, **{'network': self, 'node': self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification Group : %s', args)
        dispatcher.send(self.SIGNAL_GROUP, \
                **{'network': self, 'node': self.nodes[args['nodeId']], 'groupidx': args['groupIdx']})

    def _handle_node(self, node):
        """
        Sent when a node is changed, added, removed, ...
        If you don't interest in nodes event details you can listen to this
        signal only.

        dispatcher.send(self.SIGNAL_NODE, **{'network': self, 'node':self.nodes[args['nodeId']]})

        :param node: the node
        :type node: ZWaveNode

        """
        logger.debug(u'Z-Wave Notification Node : %s', node)
        dispatcher.send(self.SIGNAL_NODE, \
                **{'network': self, 'node':node})

    def _handle_node_added(self, args):
        """
        A new node has been added to OpenZWave's set.
        This may be due to a device being added to the Z-Wave network,
        or because the application is initializing itself.

        dispatcher.send(self.SIGNAL_NODE_ADDED, **{'network': self, 'node': node})
        dispatcher.send(self.SIGNAL_NODE, **{'network': self, 'node':self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification NodeAdded : %s', args)
        try:
            node = ZWaveNode(args['nodeId'], network=self)
            self._semaphore_nodes.acquire()
            self.nodes[args['nodeId']] = node
            dispatcher.send(self.SIGNAL_NODE_ADDED, \
                **{'network': self, 'node': self.nodes[args['nodeId']]})
            self._handle_node(self.nodes[args['nodeId']])
        finally:
            self._semaphore_nodes.release()

    def _handle_scene_event(self, args):
        """
        Scene Activation Set received

        Not implemented

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification SceneEvent : %s', args)
        dispatcher.send(self.SIGNAL_SCENE_EVENT, \
            **{'network': self, 'node': self.nodes[args['nodeId']],
               'scene_id': args['sceneId']})

    def _handle_node_event(self, args):
        """
        A node has triggered an event.  This is commonly caused when a
        node sends a Basic_Set command to the controller.
        The event value is stored in the notification.

        dispatcher.send(self.SIGNAL_NODE_EVENT, **{'network': self, 'node': self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification NodeEvent : %s', args)
        dispatcher.send(self.SIGNAL_NODE_EVENT,
                        **{'network': self, 'node': self.nodes[args['nodeId']], 'value': args['event']})

    def _handle_node_naming(self, args):
        """
        One of the node names has changed (name, manufacturer, product).

        dispatcher.send(self.SIGNAL_NODE_NAMING, **{'network': self, 'node': self.nodes[args['nodeId']]})
        dispatcher.send(self.SIGNAL_NODE, **{'network': self, 'node':self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification NodeNaming : %s', args)
        dispatcher.send(self.SIGNAL_NODE_NAMING, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})
        self._handle_node(self.nodes[args['nodeId']])

    def _handle_node_new(self, args):
        """
        A new node has been found (not already stored in zwcfg*.xml file).

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug('Z-Wave Notification NodeNew : %s', args)
        dispatcher.send(self.SIGNAL_NODE_NEW, \
            **{'network': self, 'node_id': args['nodeId']})

    def _handle_node_protocol_info(self, args):
        """
        Basic node information has been received, such as whether
        the node is a listening device, a routing device and its baud rate
        and basic, generic and specific types.
        It is after this notification that you can call Manager::GetNodeType
        to obtain a label containing the device description.

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification NodeProtocolInfo : %s', args)
        dispatcher.send(self.SIGNAL_NODE_PROTOCOL_INFO, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})
        self._handle_node(self.nodes[args['nodeId']])

    def _handle_node_removed(self, args):
        """
        A node has been removed from OpenZWave's set.
        This may be due to a device being removed from the Z-Wave network,
        or because the application is closing.

        dispatcher.send(self.SIGNAL_NODE_REMOVED, **{'network': self, 'node_id': args['nodeId']})
        dispatcher.send(self.SIGNAL_NODE, **{'network': self, 'node':self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification NodeRemoved : %s', args)
        try:
            self._semaphore_nodes.acquire()
            if args['nodeId'] in self.nodes:
                node = self.nodes[args['nodeId']]
                del self.nodes[args['nodeId']]
                dispatcher.send(self.SIGNAL_NODE_REMOVED, \
                    **{'network': self, 'node': node})
                self._handle_node(node)
        finally:
            self._semaphore_nodes.release()

    def _handle_essential_node_queries_complete(self, args):
        """
        The queries on a node that are essential to its operation have
        been completed. The node can now handle incoming messages.

        dispatcher.send(self.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE, **{'network': self, 'node': self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification EssentialNodeQueriesComplete : %s', args)
        dispatcher.send(self.SIGNAL_ESSENTIAL_NODE_QUERIES_COMPLETE, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})

    def _handle_node_queries_complete(self, args):
        """
        All the initialisation queries on a node have been completed.

        dispatcher.send(self.SIGNAL_NODE_QUERIES_COMPLETE, **{'network': self, 'node': self.nodes[args['nodeId']]})
        dispatcher.send(self.SIGNAL_NODE, **{'network': self, 'node':self.nodes[args['nodeId']]})

        When receiving this value, we consider that the node is ready.

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification NodeQueriesComplete : %s', args)
        #the query stage are now completed, set the flag is ready to operate
        self.nodes[args['nodeId']].is_ready = True
        dispatcher.send(self.SIGNAL_NODE_QUERIES_COMPLETE, \
            **{'network': self, 'node': self.nodes[args['nodeId']]})
        self._handle_node(self.nodes[args['nodeId']])

    def _handle_all_nodes_queried(self, args):
        """
        All nodes have been queried, so client application can expected
        complete data.

        :param args: data sent by the notification
        :type args: dict()

        dispatcher.send(self.SIGNAL_NETWORK_READY, **{'network': self})
        dispatcher.send(self.SIGNAL_ALL_NODES_QUERIED, **{'network': self, 'controller': self._controller})

        """
        logger.debug(u'Z-Wave Notification AllNodesQueried : %s', args)
        self._state = self.STATE_READY
        dispatcher.send(self.SIGNAL_NETWORK_READY, **{'network': self})
        dispatcher.send(self.SIGNAL_ALL_NODES_QUERIED, \
            **{'network': self, 'controller': self._controller})

    def _handle_all_nodes_queried_some_dead(self, args):
        """
        All nodes have been queried, but some node ar mark dead, so client application can expected
        complete data.

        :param args: data sent by the notification
        :type args: dict()

        dispatcher.send(self.SIGNAL_NETWORK_READY, **{'network': self})
        dispatcher.send(self.SIGNAL_ALL_NODES_QUERIED, **{'network': self, 'controller': self._controller})

        """
        logger.debug(u'Z-Wave Notification AllNodesQueriedSomeDead : %s', args)
        self._state = self.STATE_READY
        dispatcher.send(self.SIGNAL_NETWORK_READY, **{'network': self})
        dispatcher.send(self.SIGNAL_ALL_NODES_QUERIED_SOME_DEAD, \
            **{'network': self, 'controller': self._controller})

    def _handle_awake_nodes_queried(self, args):
        """
        All awake nodes have been queried, so client application can
        expected complete data for these nodes.

        dispatcher.send(self.SIGNAL_NETWORK_AWAKED, **{'network': self})
        dispatcher.send(self.SIGNAL_AWAKE_NODES_QUERIED, **{'network': self, 'controller': self._controller})

        dispatcher.send(self.SIGNAL_NETWORK_AWAKED, **{'network': self})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification AwakeNodesQueried : %s', args)
        self._object_id = args['homeId']
        try:
            if self._state < self.STATE_AWAKED:
                self._state = self.STATE_AWAKED
            dispatcher.send(self.SIGNAL_NETWORK_AWAKED, **{'network': self})
            dispatcher.send(self.SIGNAL_AWAKE_NODES_QUERIED, \
                **{'network': self, 'controller': self._controller})
        except:
            import sys, traceback
            logger.error('Z-Wave Notification AwakeNodesQueried : %s', traceback.format_exception(*sys.exc_info()))
        finally:
            pass

    def _handle_polling_disabled(self, args):
        """
        Polling of a node has been successfully turned off by a call
        to Manager::DisablePoll.

        dispatcher.send(self.SIGNAL_POLLING_DISABLED, **{'network': self, 'node' : self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification PollingDisabled : %s', args)
        dispatcher.send(self.SIGNAL_POLLING_DISABLED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_polling_enabled(self, args):
        """
        Polling of a node has been successfully turned on by a call
        to Manager::EnablePoll.

        dispatcher.send(self.SIGNAL_POLLING_ENABLED, **{'network': self, 'node' : self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification PollingEnabled : %s', args)
        dispatcher.send(self.SIGNAL_POLLING_ENABLED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_create_button(self, args):
        """
        Handheld controller button event created.

        dispatcher.send(self.SIGNAL_CREATE_BUTTON, **{'network': self, 'node' : self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification CreateButton : %s', args)
        dispatcher.send(self.SIGNAL_CREATE_BUTTON, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_delete_button(self, args):
        """
        Handheld controller button event deleted.

        dispatcher.send(self.SIGNAL_DELETE_BUTTON, **{'network': self, 'node' : self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification DeleteButton : %s', args)
        dispatcher.send(self.SIGNAL_DELETE_BUTTON, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_button_on(self, args):
        """
        Handheld controller button on pressed event.

        dispatcher.send(self.SIGNAL_BUTTON_ON, **{'network': self, 'node' : self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification ButtonOn : %s', args)
        dispatcher.send(self.SIGNAL_BUTTON_ON, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_button_off(self, args):
        """
        Handheld controller button off pressed event.

        dispatcher.send(self.SIGNAL_BUTTON_OFF, **{'network': self, 'node' : self.nodes[args['nodeId']]})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification ButtonOff : %s', args)
        dispatcher.send(self.SIGNAL_BUTTON_OFF, \
            **{'network': self, 'node' : self.nodes[args['nodeId']]})

    def _handle_value(self, node=None, value=None):
        """
        Sent when a value is changed, addes, removed, ...
        If you don't interrest in values event details you can listen to this
        signal only.

        dispatcher.send(self.SIGNAL_VALUE, **{'network': self, 'node' : node, 'value' : value})

        :param nodeid: the id of the node who hold the value
        :type nodeid: int
        :param valueid: the id of the value
        :type valueid: int

        """
        dispatcher.send(self.SIGNAL_VALUE, \
            **{'network': self, 'node' : node, \
                'value' : value})

    def _handle_value_added(self, args):
        """
        A new node value has been added to OpenZWave's set.
        These notifications occur after a node has been discovered,
        and details of its command classes have been received.
        Each command class may generate one or more values depending
        on the complexity of the item being represented.

        dispatcher.send(self.SIGNAL_VALUE_ADDED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})
        dispatcher.send(self.SIGNAL_VALUE, **{'network': self, 'node' : node, 'value' : value})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification ValueAdded : %s', args)
        self.nodes[args['nodeId']].add_value(args['valueId']['id'])
        dispatcher.send(self.SIGNAL_VALUE_ADDED, \
            **{'network': self, \
               'node' : self.nodes[args['nodeId']], \
               'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})
        self._handle_value(node=self.nodes[args['nodeId']], value=self.nodes[args['nodeId']].values[args['valueId']['id']])

    def _handle_value_changed(self, args):
        """
        A node value has been updated from the Z-Wave network and it is
        different from the previous value.

        dispatcher.send(self.SIGNAL_VALUE_CHANGED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})
        dispatcher.send(self.SIGNAL_VALUE, **{'network': self, 'node' : node, 'value' : value})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification ValueChanged : %s', args)
        if args['nodeId'] not in self.nodes:
            logger.warning('Z-Wave Notification ValueChanged (%s) for an unknown node %s', args['valueId'], args['nodeId'])
            return False
        self.nodes[args['nodeId']].change_value(args['valueId']['id'])
        dispatcher.send(self.SIGNAL_VALUE_CHANGED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})
        self._handle_value(node=self.nodes[args['nodeId']], value=self.nodes[args['nodeId']].values[args['valueId']['id']])

    def _handle_value_refreshed(self, args):
        """
        A node value has been updated from the Z-Wave network.

        dispatcher.send(self.SIGNAL_VALUE_REFRESHED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})
        dispatcher.send(self.SIGNAL_VALUE, **{'network': self, 'node' : node, 'value' : value})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification ValueRefreshed : %s', args)
        if args['nodeId'] not in self.nodes:
            logger.warning('Z-Wave Notification ValueRefreshed (%s) for an unknown node %s', args['valueId'], args['nodeId'])
            return False
        self.nodes[args['nodeId']].refresh_value(args['valueId']['id'])
        dispatcher.send(self.SIGNAL_VALUE_REFRESHED, \
            **{'network': self, 'node' : self.nodes[args['nodeId']], \
                'value' : self.nodes[args['nodeId']].values[args['valueId']['id']]})
        self._handle_value(node=self.nodes[args['nodeId']], value=self.nodes[args['nodeId']].values[args['valueId']['id']])

    def _handle_value_removed(self, args):
        """
        A node value has been removed from OpenZWave's set.
        This only occurs when a node is removed.

        dispatcher.send(self.SIGNAL_VALUE_REMOVED, \
                **{'network': self, 'node' : self.nodes[args['nodeId']], \
                    'value' : val})
        dispatcher.send(self.SIGNAL_VALUE, **{'network': self, 'node' : node, 'value' : value})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification ValueRemoved : %s', args)
        if args['nodeId'] not in self.nodes:
            logger.warning(u'Z-Wave Notification ValueRemoved (%s) for an unknown node %s', args['valueId'], args['nodeId'])
            return False
        if args['valueId']['id'] in self.nodes[args['nodeId']].values:
            logger.warning(u'Z-Wave Notification ValueRemoved for an unknown value (%s) on node %s', args['valueId'], args['nodeId'])
            dispatcher.send(self.SIGNAL_VALUE_REMOVED, \
                **{'network': self, 'node' : self.nodes[args['nodeId']], \
                    'value' : None, 'valueId' : args['valueId']['id']})
            return False
        val = self.nodes[args['nodeId']].values[args['valueId']['id']]
        if self.nodes[args['nodeId']].remove_value(args['valueId']['id']):
            dispatcher.send(self.SIGNAL_VALUE_REMOVED, \
                **{'network': self, 'node' : self.nodes[args['nodeId']], \
                    'value' : val, 'valueId' : args['valueId']['id']})
            #self._handle_value(node=self.nodes[args['nodeId']], value=val)
        if args['nodeId'] in self.nodes and args['valueId']['id'] in self.nodes[args['nodeId']].values:
            del self.nodes[args['nodeId']].values[args['valueId']['id']]
        return True

    def _handle_notification(self, args):
        """
        Called when an error happened, or node changed (awake, sleep, death, no operation, timeout).

        dispatcher.send(self.SIGNAL_NOTIFICATION, **{'network': self})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification : %s', args)
        dispatcher.send(self.SIGNAL_NOTIFICATION, \
            **{'network': self, 'args': args})

    def _handle_controller_command(self, args):
        """
        Called when a message from controller is sent.

        The state could be obtained here :
        dispatcher.send(self.SIGNAL_CONTROLLER_WAITING, \
            **{'network': self, 'controller': self.controller,
               'state_int': args['controllerStateInt'], 'state': args['controllerState'], 'state_full': args['controllerStateDoc'],
               })

        And the full command here :

        dispatcher.send(self.SIGNAL_CONTROLLER_COMMAND, \
            **{'network': self, 'controller': self.controller,
               'node':self.nodes[args['nodeId']] if args['nodeId'] in self.nodes else None, 'node_id' : args['nodeId'],
               'state_int': args['controllerStateInt'], 'state': args['controllerState'], 'state_full': args['controllerStateDoc'],
               'error_int': args['controllerErrorInt'], 'error': args['controllerError'], 'error_full': args['controllerErrorDoc'],
               })

        :param args: data sent by the notification
        :type args: dict()

        """
        self._controller._handle_controller_command(args)

    def _handle_msg_complete(self, args):
        """
        The last message that was sent is now complete.

        dispatcher.send(self.SIGNAL_MSG_COMPLETE, **{'network': self})

        :param args: data sent by the notification
        :type args: dict()

        """
        logger.debug(u'Z-Wave Notification MsgComplete : %s', args)
        dispatcher.send(self.SIGNAL_MSG_COMPLETE, \
            **{'network': self})

    def write_config(self):
        """
        The last message that was sent is now complete.

        """
        self._manager.writeConfig(self.home_id)
        logger.info(u'ZWave configuration written to user directory.')

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

    [driverRemoved]
"""

class ZWaveNetworkSingleton(ZWaveNetwork):
    """
    Represents a singleton Zwave network.

    """
    __metaclass__ = Singleton

