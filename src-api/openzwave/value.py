# -*- coding: utf-8 -*-
"""
.. module:: openzwave.value

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
from six import string_types
from openzwave.object import ZWaveObject

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

# TODO: don't report controller node as sleeping
# TODO: allow value identification by device/index/instance
class ZWaveValue(ZWaveObject):
    """
    Represents a single value.
    """
    def __init__(self, value_id, network=None, parent=None):
        """
        Initialize value

        .. code-block:: python

                n['valueId'] = {'home_id' : v.GetHomeId(),
                    * 'parent_id' : v.GetNodeId(),
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
                    * 'readOnly': manager.IsValueReadOnly(v),
                    }

        :param value_id: ID of the value
        :type value_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        """
        ZWaveObject.__init__(self, value_id, network=network)
        logger.debug(u"Create object value (valueId:%s)", value_id)
        self._parent = parent

    def __str__(self):
        """
        The string representation of the value.

        :rtype: str

        """
        return u'home_id: [%s] id: [%s] parent_id: [%s] label: [%s] data: [%s]' % \
          (self._network.home_id_str, self._object_id, self.parent_id, self.label, self.data)

    @property
    def parent_id(self):
        """
        Get the parent_id of the value.
        """
        return self._parent.object_id

    @property
    def value_id(self):
        """
        Get the value_id of the value.
        """
        return self._object_id

    @property
    def id_on_network(self):
        """
        Get an unique id for this value.

        The scenes use this to retrieve values

        .. code-block:: xml

                <Scene id="1" label="scene1">
                        <Value homeId="0x014d0ef5" nodeId="2" genre="user" commandClassId="38" instance="1" index="0" type="byte">54</Value>
                </Scene>

        The format is :

            home_id.node_id.command_class.instance.index

        """
        separator = self._network.id_separator
        return "%0.8x%s%s%s%0.2x%s%s%s%s" % (self._network.home_id, \
          separator, self.parent_id, \
          separator, self.command_class, \
          separator, self.instance, \
          separator, self.index)

    @property
    def node(self):
        """
        The value_id of the value.
        """
        return self._parent

    @property
    def label(self):
        """
        Get the label of the value.

        :rtype: str
        """
        return self._network.manager.getValueLabel(self.value_id)

    @label.setter
    def label(self, value):
        """
        Set the label of the value.

        :param value: The new label value
        :type value: str
        """
        self._network.manager.setValueLabel(self.value_id, value)

    @property
    def help(self):
        """
        Gets a help string describing the value's purpose and usage.

        :rtype: str
        """
        return self._network.manager.getValueHelp(self.value_id)

    @help.setter
    def help(self, value):
        """
        Sets a help string describing the value's purpose and usage..

        :param value: The new help value
        :type value: str

        """
        self._network.manager.setValueHelp(self.value_id, value)

    @property
    def units(self):
        """
        Gets the units that the value is measured in.

        :rtype: str

        """
        return self._network.manager.getValueUnits(self.value_id)

    @units.setter
    def units(self, value):
        """
        Sets the units that the value is measured in.

        :param value: The new units value
        :type value: str

        """
        self._network.manager.setValueUnits(self.value_id, value)

    @property
    def max(self):
        """
        Gets the maximum that this value may contain.

        :rtype: int

        """
        return self._network.manager.getValueMax(self.value_id)

    @property
    def min(self):
        """
        Gets the minimum that this value may contain.

        :rtype: int

        """
        return self._network.manager.getValueMin(self.value_id)

    @property
    def type(self):
        """
        Get the type of the value.  The type describes the data held by the value
        and enables the user to select the correct value accessor method in the
        Manager class.

        :return: type of the value
        :rtype: str

        """
        return self._network.manager.getValueType(self.value_id)

    @property
    def genre(self):
        """
        Get the genre of the value.  The genre classifies a value to enable
        low-level system or configuration parameters to be filtered out
        by the application

        :return: genre of the value (Basic, User, Config, System)
        :rtype: str

        """
        return self._network.manager.getValueGenre(self.value_id)

    @property
    def index(self):
        """
        Get the value index.  The index is used to identify one of multiple
        values created and managed by a command class.  In the case of configurable
        parameters (handled by the configuration command class), the index is the
        same as the parameter ID.

        :return: index of the value
        :rtype: int

        """
        return self._network.manager.getValueIndex(self.value_id)

    @property
    def instance(self):
        """
        Get the command class instance of this value.  It is possible for there to be
        multiple instances of a command class, although currently it appears that
        only the SensorMultilevel command class ever does this.

        :return: instance of the value
        :rtype: int

        """
        return self._network.manager.getValueInstance(self.value_id)

    @property
    def data(self):
        """
        Get the current data of the value.

        :return: The data of the value
        :rtype: depending of the type of the value

        """
        return self._network.manager.getValue(self.value_id)

    @data.setter
    def data(self, value):
        """
        Set the data of the value.

        Best practice: Use check_data before setting it:

        new_val = value.check_data(some_data)
        if new_val != None:
            value.data = new_val

        :param value: The new data value
        :type value:

        """
        self._network.manager.setValue(self.value_id, value)

    @property
    def data_as_string(self):
        """
        Get the value data as String.

        :rtype: str

        """
        return self._network.manager.getValueAsString(self.value_id)

    @property
    def data_items(self):
        """
        When type of value is list, data_items contains a list of valid values

        :return: The valid values or a help string
        :rtype: string or set

        """
        if self.is_read_only:
            return "Read only"
        if self.type == "Bool":
            return "True or False"
        elif self.type == "Byte":
            return "A byte between %s and %s" % (self.min, self.max)
        elif self.type == "Decimal":
            return "A decimal"
        elif self.type == "Int":
            return "An integer between %s and %s" % (self.min, self.max)
        elif self.type == "Short":
            return "A short between %s and %s" % (self.min, self.max)
        elif self.type == "String":
            return "A string"
        elif self.type == "Button":
            return "True or False"
        elif self.type == "List":
            return self._network.manager.getValueListItems(self.value_id)
        else:
            return "Unknown"

    def check_data(self, data):
        """
        Check that data is correct for this value.
        Return the data in a correct type. None is data is incorrect.

        :param data:  The data value to check
        :type data: lambda
        :return: A variable of the good type if the data is correct. None otherwise.
        :rtype: variable

        """
        if self.is_read_only:
            return None
        new_data = None
        logger.debug(u"check_data type :%s", self.type)
        if self.type == "Bool":
            if isinstance(data, string_types):
                if data in ["False", "false", "FALSE", "0"]:
                    new_data = False
                else:
                    new_data = True
            else:
                try:
                    new_data = bool(data)
                except:
                    new_data = None
        elif self.type == "Byte":
            try:
                new_data = int(data)
            except:
                new_data = None
            if new_data is not None:
                if new_data < 0:
                    new_data = 0
                elif new_data > 255:
                    new_data = 255
        elif self.type == "Decimal":
            try:
                new_data = float(data)
            except:
                new_data = None
        elif self.type == "Int":
            try:
                new_data = int(data)
            except:
                new_data = None
            if new_data is not None:
                if new_data < -2147483648:
                    new_data = -2147483648
                elif new_data > 2147483647:
                    new_data = 2147483647
        elif self.type == "Short":
            try:
                new_data = int(data)
            except:
                new_data = None
            if new_data is not None:
                if new_data < -32768:
                    new_data = -32768
                elif new_data > 32767:
                    new_data = 32767
        elif self.type == "String":
            new_data = data
        elif self.type == "Button":
            if isinstance(data, string_types):
                if data in ["False", "false", "FALSE", "0"]:
                    new_data = False
                else:
                    new_data = True
            else:
                try:
                    new_data = bool(data)
                except:
                    new_data = None
        elif self.type == "List":
            if isinstance(data, string_types):
                if data in self.data_items:
                    new_data = data
                else:
                    new_data = None
        return new_data

    @property
    def is_set(self):
        """
        Test whether the value has been set.

        :return: True if the value has actually been set by a status message
                 from the device, rather than simply being the default.
        :rtype: bool

        """
        return self._network.manager.isValueSet(self.value_id)

    @property
    def is_read_only(self):
        """
        Test whether the value is read-only.

        :return: True if the value cannot be changed by the user.
        :rtype: bool

        """
        return self._network.manager.isValueReadOnly(self.value_id)

    @property
    def is_write_only(self):
        """
        Test whether the value is write-only.

        :return: True if the value can only be written to and not read.
        :rtype: bool

        """
        return self._network.manager.isValueWriteOnly(self.value_id)

    def enable_poll(self, intensity=1):
        """
        Enable the polling of a device's state.

        :param intensity: The intensity of the poll
        :type intensity: int
        :return: True if polling was enabled.
        :rtype: bool

        """
        return self._network.manager.enablePoll(self.value_id, intensity)

    def disable_poll(self):
        """
        Disable poll off this value.

        :return: True if polling was disabled.
        :rtype: bool

        """
        return self._network.manager.disablePoll(self.value_id)

    @property
    def poll_intensity(self):
        """
        The poll intensity of the value.

        :returns: 0=none, 1=every time through the list, 2-every other time, etc
        :rtype: int

        """
        #always ask to manager to get poll intensity
        return self._network.manager.getPollIntensity(self.value_id)

    @property
    def is_polled(self):
        """
        Verify that the value is polled.

        :rtype: bool

        """
        return self._network.manager.isPolled(self.value_id)

    @property
    def command_class(self):
        """
        The command class of the value.

        :returns: The command class of this value
        :rtype: int

        """
        return self._network.manager.getValueCommandClass(self.value_id)

    def refresh(self):
        """
        Refresh the value.

        :returns: True if the command was transmitted to controller
        :rtype: bool

        """
        return self._network.manager.refreshValue(self.value_id)

    @property
    def precision(self):
        """
        Gets a float value's precision.

        :returns: a float value's precision
        :rtype: int

        """
        return self._network.manager.getValueFloatPrecision(self.value_id)

    def is_change_verified(self):
        """
        determine if value changes upon a refresh should be verified.
        If so, the library will immediately refresh the value a second time whenever a change is observed.
        This helps to filter out spurious data reported occasionally by some devices.
        """
        return self._network.manager.getChangeVerified(self.value_id)


    def set_change_verified(self, verify):
        """
        Sets a flag indicating whether value changes noted upon a refresh should be verified.

        If so, the library will immediately refresh the value a second time whenever a change is observed.
        This helps to filter out spurious data reported occasionally by some devices.

        :param verify: if true, verify changes; if false, don't verify changes.
        :type verify: bool
        """
        logger.debug(u'Set change verified %s for valueId [%s]', verify, self.value_id)
        self._network.manager.setChangeVerified(self.value_id, verify)

    def to_dict(self, extras=['all']):
        """
        Return a dict representation of the node.

        :param extras: The extra inforamtions to add
        :type extras: []
        :returns: A dict
        :rtype: dict()

        """
        attrs = []
        if 'all' in extras:
            extras = ['kvals']
            attrs = ['data_items', 'command_class', 'is_read_only', 'is_write_only', 'type', 'index']
        ret={}
        ret['label'] = self.label
        ret['value_id'] = self.value_id
        ret['node_id'] = self.node.node_id
        ret['units'] = self.units
        ret['genre'] = self.genre
        ret['data'] = self.data

        for k in attrs:
            ret[k] = getattr(self, k)
        if 'kvals' in extras and self.network.dbcon is not None:
            vals = self.kvals
            for key in vals.keys():
                ret[key]=vals[key]
        return ret
