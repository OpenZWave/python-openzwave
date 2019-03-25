# -*- coding: utf-8 -*-
"""
.. module:: openzwave.node

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
import sys
import six
from libopenzwave import PyStatNode
from openzwave import command_classes
from openzwave import device_classes
from openzwave.object import ZWaveObject
from openzwave.group import ZWaveGroup
from openzwave.value import ZWaveValue

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

# the ZWaveNodeInterface class is the starting point of a node creation.
# In the _handle_node_add method in the ZWaveNetwork class I replaced the
# node object ZWaveNode with ZWaveNodeInterface.

# the ZWaveNodeInterface class is a dummy class it is simply a shell to
# redirect the call made to create the instance to ZWaveNodeInterfaceMeta
# I have provided comments in the ZWaveNodeInterfaceMeta class that will walk
# you through what is happening


class ZWaveNodeInterfaceMeta(type):
    # this class variable is used to hold the node instances. This metaclass is
    # doubles as a singleton class. the key used to store the instances
    # is a tuple containing the network instance and the id of the node
    instances = {}

    # this is what gets called when a new instance of ZWaveNodeInterface
    # is needed. we either return a stored instance if an instance with the
    # same network and id has been created already, or we dynamically build a
    # Node class and store it's instance then return it

    def __call__(cls, id, network=None, use_cache=True):

        if (id, network) not in ZWaveNodeInterfaceMeta.instances:
            # we need to set the bases of the node. ZWaveNode being the
            # primary parent class.
            bases = (ZWaveNode,)

            # we then make a call to the network manager to get the
            # command classes for the id that was passed.

            for command_cls in network.manager.COMMAND_CLASS_DESC:
                if network.manager.getNodeClassInformation(
                    network.home_id,
                    id,
                    command_cls
                ):

                    # once we have the command class id's we pass the id's as
                    # keys to a dictionary to the command_class module. The
                    # module then returns the proper class representation
                    # for that id. we take that class and add it to the bases

                    # noinspection PyUnresolvedReferences
                    command_cls = command_classes[command_cls]
                    if command_cls not in bases:
                        bases += (command_cls,)

            # we need to supply a custom __init__ to our dynamically created
            # class in order to properly start all of the parent classes

            # noinspection PyShadowingBuiltins
            def __init__(self, id, net):
                ZWaveNode.__init__(
                    self,
                    id,
                    net,
                )

                for cmd_cls in self.__bases__[1:]:
                    cmd_cls.__init__(self)

            # we use type to make the new class supplying it with the
            # custom __init__ and the bases. the __init__ iterates through
            # the bases and calls the constructor for each of them. at the
            # time each base class is constructed if it is a command class it
            # adds it's id to _cls_ids. this is done so we can use equality
            # testing to identify if a node supports a specific command class.

            # as an example. if we wanted to turn on a light switch
            # if node == command_class.COMMAND_CLASS_BINARY_SWITCH:
            #     node.state = True

            # I found this to be a much better mechanism for testing node types
            # then having to add a method to ZWaveNode to check.
            # not to mention having ZWaveNode contain all the various
            # properties and methods for all command classes can get a wee
            # bit difficult to follow. So if a node is not a binary switch
            # then it is not going to have the property state. it removes any
            # checking that would need to be done inside of the
            # property/method to ensure the node is the proper type

            # this same equality testing also works on the values. It's a
            # simple to use mechanism. the equality test is only performed
            # against the command classes of a node/value if the object
            # passed is an int, if testing 2 nodes it will check to see if the
            # networks and ids match. because of the use of the
            # singleton only a single node instance on a network can exist

            node = type(
                'ZWaveNode',
                bases,
                {"__init__": __init__, '__bases__': bases}
            )
            ZWaveNodeInterfaceMeta.instances[(id, network)] = (
                node(id, network, use_cache)
            )

        return ZWaveNodeInterfaceMeta.instances[(id, network)]


@six.add_metaclass(ZWaveNodeInterfaceMeta)
class ZWaveNodeInterface(object):

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        raise AttributeError(item)


class ZWaveNode(ZWaveObject):
    """
    Represents a single Node within the Z-Wave Network.
    """
    _isReady = False

    def __init__(self, node_id, network):
        """
        Initialize Z-Wave node

        :param node_id: ID of the node
        :type node_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        """
        self._cls_ids = getattr(self, '_cls_ids', [])

        logger.debug("Create object node (node_id:%s)", node_id)
        ZWaveObject.__init__(self, node_id, network)
        # No cache management for values in nodes
        self.values = dict()
        self._is_locked = False
        self._isReady = False

    def __unicode__(self):
        return unicode(str(self))

    def __str__(self):
        """
        The string representation of the node.
        """
        try:
            return (
                'home_id: [%s] id: [%s] name: [%s] model: [%s]' % (
                    self._network.home_id_str,
                    self._id,
                    self.name,
                    self.product_name
                )
            )
        except UnicodeDecodeError:
            return (
                'home_id: [%s] id: [%s] name: [%s] model: [%s]' % (
                    self._network.home_id_str,
                    self.id,
                    self.name.decode('utf-8', 'ignore'),
                    self.product_name.decode('utf-8', 'ignore')
                )
            )

    @property
    def name(self):
        """
        The name of the node.

        :rtype: str
        """
        return self._network.manager.getNodeName(self.home_id, self.id)

    @name.setter
    def name(self, value):
        """
        Set the name of the node.

        :param value: The new name of the node
        :type value: str
        """
        self._network.manager.setNodeName(self.home_id, self.id, value)

    @property
    def location(self):
        """
        The location of the node.

        :rtype: str
        """
        return self._network.manager.getNodeLocation(self.home_id, self.id)

    @location.setter
    def location(self, value):
        """
        Set the location of the node.

        :param value: The new location of the node
        :type value: str
        """
        self._network.manager.setNodeLocation(self.home_id, self.id, value)

    @property
    def product_name(self):
        """
        The product name of the node.

        :rtype: str
        """
        return self._network.manager.getNodeProductName(self.home_id, self.id)

    @product_name.setter
    def product_name(self, value):
        """
        Set the product name of the node.

        :param value: The new name of the product
        :type value: str
        """
        self._network.manager.setNodeProductName(self.home_id, self.id, value)

    @property
    def product_type(self):
        """
        The product type of the node.

        :rtype: str
        """
        return self._network.manager.getNodeProductType(self.home_id, self.id)

    @property
    def product_id(self):
        """
        The product Id of the node.

        :rtype: str
        """
        return self._network.manager.getNodeProductId(self.home_id, self.id)

    @property
    def manufacturer_id(self):
        """
        The manufacturer id of the node.

        :rtype: str
        """
        return self._network.manager.getNodeManufacturerId(
            self.home_id,
            self.id
        )

    @property
    def manufacturer_name(self):
        """
        The manufacturer name of the node.

        :rtype: str
        """
        return self._network.manager.getNodeManufacturerName(
            self.home_id,
            self.id
        )

    @manufacturer_name.setter
    def manufacturer_name(self, value):
        """
        Set the manufacturer name of the node.

        :param value: The new manufacturer name of the node
        :type value: str
        """
        self._network.manager.setNodeManufacturerName(
            self.home_id,
            self.id,
            value
        )

    @property
    def version(self):
        """
        The version of the node.

        :return: The version of the node
        :rtype: int
        """
        return self._network.manager.getNodeVersion(
            self.home_id,
            self.id
        )

    @property
    def device_type(self):
        """
        The device_type of the node.

        :rtype: str
        """
        code = self._network.manager.getNodeDeviceType(self.home_id, self.id)
        return device_classes.device_type_to_string(code)

    @property
    def role(self):
        """
        The role of the node.

        :rtype: str
        """
        code = self._network.manager.getNodeRole(self.home_id, self.id)
        return device_classes.role_type_to_string(code)

    @property
    def type(self):
        """
        Get a human-readable label describing the node
        :rtype: str
        """
        code = self._network.manager.getNodeType(self.home_id, self.id)
        return device_classes.node_type_to_string(code)

    @property
    def basic(self):
        """
        The basic type of the node.

        :rtype: int
        """
        code = self._network.manager.getNodeBasic(self.home_id, self.id)
        return device_classes.basic_type_to_string(code)

    @property
    def category(self):
        code = self._network.manager.getNodeGeneric(self.home_id, self.id)
        return device_classes.generic_type_to_string(code)

    @property
    def sub_category(self):
        """
        The specific type of the node.

        :return: The specific type of the node
        :rtype: int
        """
        major = self._network.manager.getNodeGeneric(self.home_id, self.id)
        minor = self._network.manager.getNodeSpecific(self.home_id, self.id)
        return device_classes.specific_type_to_string(major, minor)

    @property
    def max_baud_rate(self):
        """
        Get the maximum baud rate of a node
        """
        return self._network.manager.getNodeMaxBaudRate(self.home_id, self.id)

    @property
    def security(self):
        """
        The security type of the node.

        :return: The security type of the node
        :rtype: int
        """
        return self._network.manager.getNodeSecurity(
            self.home_id,
            self.id
        )

    @property
    def capabilities(self):
        """
        The capabilities of the node.

        :rtype: list
        """
        caps = set()
        if self.is_routing_device:
            caps.add('routing')
        if self.is_listening_device:
            caps.add('listening')
        if self.is_frequent_listening_device:
            caps.add('frequent')
        if self.is_security_device:
            caps.add('security')
        if self.is_beaming_device:
            caps.add('beaming')
        if self.is_zwave_plus:
            caps.add('zwave_plus')
        if self.id == self._network.controller.id:
            for cap in self._network.controller.capabilities:
                caps.add(cap)
        return list(c for c in caps)

    @property
    def neighbors(self):
        """
        The neighbors of the node.

        :rtype: list
        """
        return self._network.manager.getNodeNeighbors(self.home_id, self.id)

    @property
    def is_listening_device(self):
        """
        Is this node a listening device.

        :rtype: bool
        """
        return self._network.manager.isNodeListeningDevice(
            self.home_id,
            self.id
        )

    @property
    def is_beaming_device(self):
        """
        Is this node a beaming device.

        :rtype: bool
        """
        return self._network.manager.isNodeBeamingDevice(
            self.home_id,
            self.id
        )

    @property
    def is_frequent_listening_device(self):
        """
        Is this node a frequent listening device.

        :rtype: bool
        """
        return self._network.manager.isNodeFrequentListeningDevice(
            self.home_id,
            self.id
        )

    @property
    def is_security_device(self):
        """
        Is this node a security device.

        :rtype: bool
        """
        return self._network.manager.isNodeSecurityDevice(
            self.home_id,
            self.id
        )

    @property
    def is_routing_device(self):
        """
        Is this node a routing device.

        :rtype: bool
        """
        return self._network.manager.isNodeRoutingDevice(
            self.home_id,
            self.id
        )

    @property
    def is_zwave_plus(self):
        """
        Is this node a Z-Wave plus one.

        :rtype: bool
        """
        return self._network.manager.isNodeZWavePlus(
            self.home_id,
            self.id
        )

    @property
    def is_locked(self):
        """
        Is this node locked.

        :rtype: bool
        """
        return self._is_locked

    @property
    def is_sleeping(self):
        """
        Is this node sleeping.

        :rtype: bool
        """
        return not self.is_awake

    @property
    def is_awake(self):
        """
        Is this node a awake.

        :rtype: bool
        """
        return self._network.manager.isNodeAwake(self.home_id, self.id)

    @property
    def is_failed(self):
        """
        Is this node is presume failed.

        :rtype: bool
        """
        return self._network.manager.isNodeFailed(self.home_id, self.id)

    @property
    def query_stage(self):
        """
        Is this node a awake.

        :rtype: string
        """
        return self._network.manager.getNodeQueryStage(self.home_id, self.id)

    @property
    def is_ready(self):
        """
        Get whether the node is ready to operate (QueryStage Completed).

        :rtype: bool
        """
        return self._isReady

    @is_ready.setter
    def is_ready(self, value):
        """
        Set whether the node is ready to operate.
        automatically set to True by notification SIGNAL_NODE_QUERIES_COMPLETE

        :param value: is node ready
        :type value: bool
        """
        self._isReady = value

    @property
    def is_info_received(self):
        """
        Get whether the node information has been received.

        :return: if the node information has been received yet `True`/`False`
        :rtype: bool
        """
        return self._network.manager.isNodeInfoReceived(self.home_id, self.id)

    def to_dict(self, extras=('all',)):
        """
        Return a dict representation of the node.

        :param extras: The extra information to add
        :type extras: tuple, list
        :returns: A dict
        :rtype: dict
        """
        if 'all' in extras:
            extras = ['kvals', 'capabilities', 'neighbors', 'groups', 'values']
        ret = dict(
            name=self.name,
            location=self.location,
            product_type=self.product_type,
            product_name=self.product_name,
            id=self.id
        )

        if 'values' in extras:
            ret['values'] = self.values_to_dict(extras=extras)
        if 'groups' in extras:
            ret['groups'] = self.groups_to_dict(extras=extras)
        if 'neighbors' in extras:
            ret['neighbors'] = dict.fromkeys(self.neighbors, 0)
        if 'capabilities' in extras:
            ret['capabilities'] = dict.fromkeys(self.capabilities, 0)
        if 'kvals' in extras and self.network.dbcon is not None:
            vals = self.kvals

            for key in vals.keys():
                ret[key] = vals[key]

        return ret

    def get_values(
        self, class_id='All',
        genre='All',
        type='All',
        readonly='All',
        writeonly='All',
        index='All',
        label='All'
    ):
        """
        Retrieve the set of values.

        You can optionally filter for a command class, a genre and/or a type.
        You can also filter readonly and writeonly params.

        This method always filter the values.
        If you wan't to get all the node's values, use self.values instead.

        :param class_id: the COMMAND_CLASS to get values
        :type class_id: hexadecimal code or string
        :param genre: the genre of value
        :type genre: 'All' or PyGenres
        :param type: the type of value
        :type type: 'All' or PyValueTypes
        :param readonly: Is this value readonly
        :type readonly: 'All' or True or False
        :param writeonly: Is this value writeonly
        :type writeonly: 'All' or True or False
        :param index: Index of value within all the values
        :type index: int
        :param label: Label of the value as set by openzwave
        :type label: str
        :rtype: set() of Values
        """
        ret = dict()
        for value_id, value in self.values.items():
            if (
                class_id in ('All', value.command_class) and
                genre in ('All', value.genre) and
                type in ('All', value.type) and
                readonly in ('All', value.is_read_only) and
                writeonly in ('All', value.is_write_only) and
                index in ('All', value.index) and
                label in ('All', value.label)
            ):
                ret[value_id] = value
        return ret

    def values_to_dict(self, extras=('all',)):
        """
        Return a dict representation of the values.

        :param extras: The extra information to add
        :type extras: tuple, list
        :returns: A dict
        :rtype: dict
        """
        ret = {}
        for value_id, value in self.values.items():
            ret[value_id] = value.to_dict(extras=extras)
        return ret

    def add_value(self, value_id):
        """
        Add a value to the node

        :param value_id: The id of the value to add
        :type value_id: int
        :return: new value
        :rtype: :class:`openzwave.value.ZWaveValue` instance
        """
        value = ZWaveValue(value_id, network=self.network, parent=self)
        self.values[value_id] = value
        return value

    def change_value(self, value_id):
        """
        Change a value of the node.
        Not implemented

        :param value_id: The id of the value to change
        :type value_id: int
        """
        raise NotImplementedError

    def refresh_value(self, value_id):
        """
        Refresh a value of the node.

        :param value_id: The id of the value to change
        :type value_id: int
        :return: The result of the operation
        :rtype: bool
        """
        return self._network.manager.refreshValue(value_id)

    def remove_value(self, value_id):
        """
        Remove a value from a node

        :param value_id: The id of the value to change
        :type value_id: int
        :return: The result of the operation
        :rtype: bool
        """
        if value_id in self.values:
            logger.debug("Remove value : %s", self.values[value_id])
            del self.values[value_id]
            return True
        return False

    def set_field(self, field, value):
        """
        A helper to set a writable field : name, location, product_name, ...

        :param field: The field to set : name, location, product_name,
        manufacturer_name
        :type field: str
        :param value: The value to set
        :type value: str
        :rtype: bool
        """
        if field == "name":
            self.name = value
        elif field == "location":
            self.location = value
        elif field == "product_name":
            self.product_name = value
        elif field == "manufacturer_name":
            self.manufacturer_name = value

    def heal(self, upNodeRoute=False):
        """
        Heal network node by requesting the node rediscover their neighbors.
        Sends a ControllerCommand_RequestNodeNeighborUpdate to the node.

        :param upNodeRoute: Optional Whether to perform return routes
        initialization. (default = false).
        :type upNodeRoute: bool
        :return: True is the ControllerCommand is sent. False otherwise
        :rtype: bool
        """
        if self.is_awake is False:
            logger.warning(u'Node state must a minimum set to awake')
            return False
        self._network.manager.healNetworkNode(
            self.home_id,
            self.id,
            upNodeRoute
        )
        return True

    def test(self, count=1):
        """
        Send a number of test messages to node and record results.

        :param count: The number of test messages to send.
        :type count: int
        """
        self._network.manager.testNetworkNode(self.home_id, self.id, count)

    def assign_return_route(self):
        """
        Ask the to update its update its Return Route to the Controller

        This command will ask a node to update its return route
        to the controller

        Results of the AssignReturnRoute Command will be send as a
        notification with the notification type as
        notification::Type_ControllerCommand

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('assign_return_route for node [%s]', self.id)
        return self._network.controller.assign_return_route(self.id)

    def refresh_info(self):
        """
        Trigger the fetching of fixed data about a node.

        Causes the nodes data to be obtained from the Z-Wave network in
        the same way as if it had just been added.  This method would
        normally be called automatically by OpenZWave, but if you know that
        a node has been changed, calling this method will force a refresh of
        the data held by the library. This can be especially useful for d
        evices that were asleep when the application was first run.

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('refresh_info for node [%s]', self.id)
        return self._network.manager.refreshNodeInfo(self.home_id, self.id)

    def request_state(self):
        """
        Trigger the fetching of just the dynamic value data for a node.
        Causes the node's values to be requested from the Z-Wave network.
        This is the same as the query state starting from the dynamic state.

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('request_state for node [%s]', self.id)
        return self._network.manager.requestNodeState(self.home_id, self.id)

    def send_information(self):
        """
        Send a NIF frame from the Controller to a Node.

        This command send a NIF frame from the Controller to a Node

        Results of the SendNodeInformation command will be send as a
        notification with the notification type as
        Notification::Type_ControllerCommand

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('send_information for node [%s]', self.id)
        return self._network.controller.send_node_information(self.oid)

    def network_update(self):
        """
        Update the controller with network information from the SUC/SIS.

        Results of the RequestNetworkUpdate command will be send as a
        notification with the notification type as
        Notification::Type_ControllerCommand

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('network_update for node [%s]', self.id)
        return self._network.controller.request_network_update(self.id)

    def neighbor_update(self):
        """
        Ask a Node to update its Neighbor Tables

        This command will ask a Node to update its Neighbor Tables.

        Results of the RequestNodeNeighborUpdate command will be send as a
        notification with the notification type as
        Notification::Type_ControllerCommand

        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('neighbor_update for node [%s]', self.id)
        return self._network.controller.request_node_neighbor_update(self.id)

    def create_button(self, buttonid):
        """
        Create a handheld button id.

        Only intended for Bridge Firmware Controllers.

        Results of the CreateButton command will be send as a
        notification with the notification type as
        Notification::Type_ControllerCommand

        :param buttonid: the ID of the Button to query.
        :type buttonid: int
        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('create_button for node [%s]', self.id)
        return self._network.controller.create_button(self.id, buttonid)

    def delete_button(self, buttonid):
        """
        Delete a handheld button id.

        Only intended for Bridge Firmware Controllers.

        Results of the CreateButton command will be send as a
        notification with the notification type as
        Notification::Type_ControllerCommand

        :param buttonid: the ID of the Button to query.
        :type buttonid: int
        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('delete_button for node [%s]', self.id)
        return self._network.controller.delete_button(self.id, buttonid)

    def request_all_config_params(self):
        """
        Request the values of all known configurable parameters from a device.
        """
        logger.debug('Requesting config params for node [%s]', self.id)
        self._network.manager.requestAllConfigParams(self.home_id, self.id)

    def request_config_param(self, param):
        """
        Request the value of a configurable parameter from a device.

        Some devices have various parameters that can be configured to control
        the device behaviour. These are not reported by the device over the
        Z-Wave network but can usually be found in the devices user manual.
        This method requests the value of a parameter from the device, and then
        returns immediately, without waiting for a response. If the parameter
        index is valid for this device, and the device is awake, the value will
        eventually be reported via a ValueChanged notification callback. The
        ValueID reported in the callback will have an index set the same as
        _param and a command class set to the same value as returned by a call
        to Configuration::StaticGetCommandClassId.

        :param param: The param of the node.
        :type param:
        """
        logger.debug(
            'Requesting config param %s for node [%s]',
            param,
            self.id
        )
        self._network.manager.requestConfigParam(self.home_id, self.id, param)

    def set_config_param(self, param, value, size=2):
        """
        Set the value of a configurable parameter in a device.

        Some devices have various parameters that can be configured to control
        the device behaviour. These are not reported by the device over the
        Z-Wave network but can usually be found in the devices user manual.
        This method returns immediately, without waiting for confirmation from
        the device that the change has been made.

        :param param: The param of the node.
        :type param:
        :param value: The value of the param.
        :type value:
        :param size: Is an optional number of bytes to be sent for the
        parameter value. Defaults to 2.
        :type size: int
        :return: if the request was sent successfully `True`/`False`
        :rtype: bool
        """
        logger.debug('Set config param %s for node [%s]', param, self.id)
        return self._network.manager.setConfigParam(
            self.home_id,
            self.id,
            param,
            value,
            size
        )

    @property
    def stats(self):
        """
        Retrieve statistics for node.

        Statistics:
        <br></br>
        * sentCnt - Number of messages sent from this node.
        * sentFailed - Number of sent messages failed
        * retries - Number of message retries
        * receivedCnt - Number of messages received from this node.
        * receivedDups - Number of duplicated messages received;
        * receivedUnsolicited - Number of messages received unsolicited
        * lastRequestRTT - Last message request RTT
        * lastResponseRTT - Last message response RTT
        * sentTS - Last message sent time
        * receivedTS - Last message received time
        * averageRequestRTT - Average Request round trip time.
        * averageResponseRTT - Average Response round trip time.
        * quality - Node quality measure
        * lastReceivedMessage[254] - Place to hold last received message
        * errors - Count errors for dead node detection

        :return: Statistics of the node
        :rtype: dict
        """
        return self._network.manager.getNodeStatistics(self.home_id, self.id)

    def get_stats_label(self, stat):
        """
        Retrieve label of the statistic for node.

        :param stat: The code of the stat label to retrieve.
        :type stat:
        :return: The label or the stat.
        :rtype: str
        """
        # print "stat = %s" % stat
        return PyStatNode[stat]
