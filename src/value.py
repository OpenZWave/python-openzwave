# -*- coding: utf-8 -*-
"""
.. module:: openzwave.value

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
import libopenzwave
import openzwave
import logging
from openzwave.object import ZwaveObject

logging.getLogger('openzwave').addHandler(logging.NullHandler())

# TODO: don't report controller node as sleeping
# TODO: allow value identification by device/index/instance
class ZWaveValue(ZwaveObject):
    '''
    Represents a single value.
    Must be updated to use the cachedObject facilities.
    '''
    def __init__(self, valueId, network=None, nodeId=None):
        '''
        Initialize value

        n['valueId'] = {'homeId' : v.GetHomeId(),
                'nodeId' : v.GetNodeId(),
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

        :param valueId: ID of the value
        :type valueId: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        :param homeid: ID of home/driver
        :type homeid: int
        :param nodeid: ID of node
        :type nodeid: int
        :param valueData: valueId dict
        :type valueData: dict
        '''
        super(ZWaveValue, self).__init__(valueId, network)
        self.logDebug("Create object value (valueId:%s)" % (valueId))
        self._nodeId = nodeId
        self._valueData = valueData
        #self.n = valueId
        #self._values = dict()
        self._label = None
        self.cacheProperty(lambda: self.label)
        self._help = None
        self.cacheProperty(lambda: self.help)
        self._min = None
        self.cacheProperty(lambda: self.min)
        self._max = None
        self.cacheProperty(lambda: self.max)
        self._units = None
        self.cacheProperty(lambda: self.units)
        self._asString = None
        self.cacheProperty(lambda: self.asString)
        self._data = None
        self.cacheProperty(lambda: self.data)

    @property
    def nodeId(self):
        """
        The nodeId of the value.
        """
        return self._nodeId

    @property
    def label(self):
        """
        The label of the value.
        :rtype: str
        """
        if self.isOutdated(lambda: self.label):
            self._label = self._network.manager.getValueLabel(self.objectId)
            self.update(lambda: self.label)
        return self._label

    @label.setter
    def label(self, value):
        """
        Set the label of the value.
        :param value: The new label value
        :type value: str
        """
        self._network.manager.setValueLabel(self.objectId, value)
        self.outdate(lambda: self.label)

    @property
    def help(self):
        """
        The help of the value.
        :rtype: str
        """
        if self.isOutdated(lambda: self.help):
            self._help = self._network.manager.getValueHelp(self.objectId)
            self.update(lambda: self.help)
        return self._help

    @help.setter
    def help(self, value):
        """
        Set the help of the value.
        :param value: The new help value
        :type value: str
        """
        self._network.manager.setValueHelp(self.objectId, value)
        self.outdate(lambda: self.help)

    @property
    def units(self):
        """
        The units of the value.
        :rtype: str
        """
        if self.isOutdated(lambda: self.units):
            self._units = self._network.manager.getValueUnits(self.objectId)
            self.update(lambda: self.units)
        return self._units

    @units.setter
    def units(self, value):
        """
        Set the units of the value.
        :param value: The new units value
        :type value: str
        """
        self._network.manager.setValueUnits(self.objectId, value)
        self.outdate(lambda: self.units)

    @property
    def max(self):
        """
        The max of the value.
        :rtype: int
        """
        if self.isOutdated(lambda: self.max):
            self._max = self._network.manager.getValueMax(self.objectId)
            self.update(lambda: self.max)
        return self._min

    @property
    def min(self):
        """
        The min of the value.
        :rtype: int
        """
        if self.isOutdated(lambda: self.min):
            self._min = self._network.manager.getValueMin(self.objectId)
            self.update(lambda: self.min)
        return self._min

    @property
    def asString(self):
        """
        The value as String.
        :rtype: str
        """
        if self.isOutdated(lambda: self.asString):
            self._asString = self._network.manager.getValueAsString(self.objectId)
            self.update(lambda: self.asString)
        return self._asString

    @property
    def data(self):
        """
        The data of the value.
        :rtype: depending of the type of the value
        """
        if self.isOutdated(lambda: self.data):
            self._data = self._network.manager.getValue(self.objectId)
            self.update(lambda: self.data)
        return self._data

    @data.setter
    def data(self, value):
        """
        Set the data of the value.
        :param value: The new data value
        :type value: str
        """
        self._network.manager.setValue(self.objectId, value)
        self.outdate(lambda: self.data)

    def getValue(self, key):
        """
        The valueData of the value.
        """
        return self.valueData[key] if self._valueData.has_key(key) else None

    def update(self, args):
        """
        Update node value from callback arguments.
        """
        self._valueData = args['valueId']
        self._lastUpdate = time.time()

    def __str__(self):
        return 'homeId: [{0}]  nodeId: [{1}]  valueData: {2}'.format(self._homeId, self._nodeId, self._valueData)
