# -*- coding: utf-8 -*-
"""
.. module:: openzwave.object

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
# Set default logging handler to avoid "No handler found" warnings.
import logging
import warnings
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass
logger = logging.getLogger('openzwave')
logger.addHandler(NullHandler())

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)#turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning, stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning) #reset filter
        return func(*args, **kwargs)
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func

class ZWaveException(Exception):
    """
    Exception class for OpenZWave
    """
    def __init__(self, value):
        Exception.__init__(self)
        self.msg = u"Zwave Generic Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)

class ZWaveCacheException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    def __init__(self, value):
        ZWaveException.__init__(self)
        self.msg = u"Zwave Cache Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)

class ZWaveTypeException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    def __init__(self, value):
        ZWaveException.__init__(self)
        self.msg = u"Zwave Type Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' : '+self.value)

class ZWaveCommandClassException(ZWaveException):
    """
    Exception class for OpenZWave
    """
    def __init__(self, value):
        ZWaveException.__init__(self)
        self.msg = u"Zwave Command Class Exception"
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
                raise ZWaveCacheException(u"Can't set outdated to False manually. It is done automatically.")
        else:
            raise ZWaveCacheException(u"Cache not enabled")

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
            raise ZWaveCacheException(u"Cache not enabled")

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
            raise ZWaveCacheException(u"Cache not enabled")

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
            raise ZWaveCacheException(u"Cache not enabled")

    def cache_property(self, prop):
        """
        Add this property to the cache manager.

        :param prop: The property to cache
        :type prop: lambda

        """
        if self._use_cache:
            self._cached_properties[str(prop)] = True
        else:
            raise ZWaveCacheException(u"Cache not enabled")

    @property
    def object_id(self):
        """
        The id of the object.
        object_id could be None, when creating a scene for example.

        :rtype: int

        """
        return self._object_id

    @property
    def kvals(self):
        """
        The keyvals store in db for this object.

        :rtype: {}

        """
        if self.network.dbcon is None:
            return None
        res = {}
        cur = self.network.dbcon.cursor()
        cur.execute("SELECT key,value FROM %s WHERE object_id=?"%(self.__class__.__name__), (self.object_id,))
        while True:
            row = cur.fetchone()
            if row == None:
                break
            res[row[0]] = row[1]
        return res

    @kvals.setter
    def kvals(self, kvs):
        """
        The keyvals store in db for this object.

        :param kvs: The key/valuse to store in db. Setting a value to None will remove it.
        :type kvs: {}
        :rtype: boolean

        """
        if self.network.dbcon is None:
            return False
        if len(kvs) == 0:
            return True
        cur = self.network.dbcon.cursor()
        for key in kvs.keys():
            logger.debug(u"DELETE FROM %s WHERE object_id=%s and key='%s'", self.__class__.__name__, self.object_id, key)
            cur.execute("DELETE FROM %s WHERE object_id=? and key=?"%(self.__class__.__name__), (self.object_id, key))
            if kvs[key] is not None:
                logger.debug(u"INSERT INTO %s(object_id, 'key', 'value') VALUES (%s,'%s','%s');", self.__class__.__name__, self.object_id, key, kvs[key])
                cur.execute("INSERT INTO %s(object_id, 'key', 'value') VALUES (?,?,?)"%(self.__class__.__name__), (self.object_id, key, kvs[key]))
        self.network.dbcon.commit()
        return True

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
