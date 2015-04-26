# -*- coding: utf-8 -*-
"""
.. module:: openzwave.object

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

class ZWaveException(Exception):
    """
    Exception class for OpenZWave
    """
    def __init__(self, value):
        Exception.__init__(self)
        self.msg = "Zwave Generic Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)

class ZWaveCacheException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    def __init__(self, value):
        ZWaveException.__init__(self)
        self.msg = "Zwave Cache Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)

class ZWaveTypeException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    def __init__(self, value):
        ZWaveException.__init__(self)
        self.msg = "Zwave Type Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)

class ZWaveCommandClassException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    def __init__(self, value):
        ZWaveException.__init__(self)
        self.msg = "Zwave Command Class Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)

class ZWaveObject(object):
    """
    Represents a Zwave object. Values, nodes, ... can be changer by
    other managers on the network.
    """

    def __init__(self, object_id, network=None, use_cache=True):
        """
        Initialize a Zwave object

        :param object_id: ID of the object
        :type object_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        """
        self._network = network
        self._last_update = None
        self._outdated = True
        self._use_cache = use_cache
        self._object_id = object_id
        if self._use_cache:
            self._cached_properties = dict()
        else:
            self._cached_properties = None

    @property
    def home_id(self):
        """
        The home_id of the node.

        :rtype: int

        """
        return self._network.object_id if self._network != None else None

    @property
    def network(self):
        """
        The network of the node.

        :rtype: ZWaveNetwork

        """
        return self._network

    @property
    def use_cache(self):
        """
        Should this object use cache from property

        :rtype: bool

        """
        return self._use_cache

    @property
    def last_update(self):
        """
        The last update date of the device.

        :rtype: time

        """
        return self._last_update

    @last_update.setter
    def last_update(self, value):
        """
        Set the last update date of the device.

        :param value: The time of last update
        :type value: time

        """
        self._last_update = value

    @property
    def outdated(self):
        """
        Are the information of this object outdated.

        How to manage the cache ?

        2 ways of doing it :
        - refresh information when setting the property
        - refresh information when getting getting property.
        Maybe whe could implement the 2 methods.

        :rtype: int

        """
        return self._outdated

    @outdated.setter
    def outdated(self, value):
        """
        Set that this object ist outdated.

        :param value: True
        :type value: bool - True

        """
        if self._use_cache:
            if value:
                for prop in self._cached_properties:
                    self._cached_properties[prop] = True
                self._outdated = value
            else:
                raise ZWaveCacheException("Can't set outdated to False manually. It is done automatically.")
        else:
            raise ZWaveCacheException("Cache not enabled")

    def is_outdated(self, prop):
        """
        Check if property information is outdated.

        :param prop: The property to check
        :type prop: lambda
        :rtype: bool

        """
        if self._use_cache:
            if str(prop) in self._cached_properties:
                #print "property in cache %s" % self._cached_properties[str(prop)]
                return self._cached_properties[str(prop)]
            else:
                #This property is not cached so return true
                return True
        else:
            raise ZWaveCacheException("Cache not enabled")

    def outdate(self, prop):
        """
        Says that the property information is outdated.

        :param prop: The property to outdate
        :type prop: lambda

        """
        if self._use_cache:
            if str(prop) in self._cached_properties:
                self._cached_properties[str(prop)] = True
                self._outdated = True
        else:
            raise ZWaveCacheException("Cache not enabled")

    def update(self, prop):
        """
        Says that the property are updated.

        :param prop: The property to update
        :type prop: lambda

        """
        if self._use_cache:
            if str(prop) in self._cached_properties:
                self._cached_properties[str(prop)] = False
                out_dated = False
                for prop in self._cached_properties:
                    if self._cached_properties[prop]:
                        out_dated = True
                        break
                self._outdated = out_dated
        else:
            raise ZWaveCacheException("Cache not enabled")

    def cache_property(self, prop):
        """
        Add this property to the cache manager.

        :param prop: The property to cache
        :type prop: lambda

        """
        if self._use_cache:
            self._cached_properties[str(prop)] = True
        else:
            raise ZWaveCacheException("Cache not enabled")

    @property
    def object_id(self):
        """
        The id of the object.
        object_id could be None, when creating a scene for example.

        :rtype: int

        """
        return self._object_id

class ZWaveNodeInterface(object):
    """
    Represents an interface of a node. An interface can manage
    specific commandClasses (ie a switch, a dimmer, a thermostat, ...).
    Don't know what to do with it now but sure it must exist
    """

    def __init__(self):
        """
        Initialize a Zwave Node Interface

        :param object_id: ID of the object
        :type object_id: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork

        """
        self._class = "unknown"
