# -*- coding: utf-8 -*-
"""
.. module:: openzwave.object

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
import datetime
import logging

logging.getLogger('openzwave').addHandler(logging.NullHandler())

class NullLoggingHandler(logging.Handler):
    '''
    A Null Logging Handler
    '''
    def emit(self, record):
        pass

class ZWaveException(Exception):
    '''
    Exception class for OpenZWave
    '''
    def __init__(self, value):
        Exception.__init__(self)
        self.msg = "Zwave Generic Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' '+self.value)

class ZWaveCacheException(ZWaveException):
    '''
    Exception class for OpenZWave
    '''
    def __init__(self, value):
        Exception.__init__(self)
        self.msg = "Zwave Cache Exception"
        self.value = value

    def __str__(self):
        return repr(self.msg+' '+self.value)


class ZwaveObject(object):
    '''
    Represents a Zwave object. Values, nodes, ... can be changer by
    other managers on the network.
    '''

    def __init__(self, objectId, network = None, useCache = True):
        '''
        Initialize a Zwave object

        :param objectId: ID of the object
        :type objectId: int
        :param network: The network object to access the manager
        :type network: ZWaveNetwork
        '''
        self._network = network
        self._lastUpdate = None
        self._outdated = True
        self._useCache = useCache
        self._objectId = objectId
        if self._useCache:
            self._cachedProperties = dict()
        else :
            self._cachedProperties = None

    @property
    def homeId(self):
        """
        The homeId of the node.
        :rtype: int
        """
        return self._network.objectId if self._network!=None else None

    @property
    def useCache(self):
        """
        Should this object use cache from property
        """
        return self._useCache

    @property
    def lastUpdate(self):
        """
        The last update date of the device.
        """
        return self._lastUpate

    @lastUpdate.setter
    def lastUpdate(self, value):
        """
        Set the last update date of the device.
        """
        self._lastUpate = value

    @property
    def outdated(self):
        """
        Are the informations of this object outdated.

        How to manage the cache ?

        2 ways of doing it :
        - refresh informations when setting the property
        - refresh informations when getting gtting property.
        Maybe whe could implement the 2 methods.

        """
        return self._outdated

    @outdated.setter
    def outdated(self, value):
        """
        Set that informations are outdated.
        """
        if self._useCache :
            if value :
                for prop in self._cachedProperties:
                    self._cachedProperties[prop] = True
                self._outdated = value
            else:
                raise ZWaveCacheException("Can't set outdated to False manualy. It is done automatically.")
        else:
            raise ZWaveCacheException("Cache not enabled")

    def isOutdated(self, prop):
        """
        Check if property information is outdated.
        """
        if self._useCache :
            return self._cachedProperties[str(prop)]
        else:
            raise ZWaveCacheException("Cache not enabled")

    def outdate(self, prop):
        """
        Says that the property information is outdated.
        """
        if self._useCache :
            self._cachedProperties[str(prop)] = True
            self._outdated = True
        else:
            raise ZWaveCacheException("Cache not enabled")

    def update(self, prop):
        """
        Says that the property are updated.
        """
        if self._useCache :
            self._cachedProperties[str(prop)] = False
            #logging.debug("Data %s is updated." % str(prop))
            outd = False
            for p in self._cachedProperties:
                if self._cachedProperties[p]:
                    outd = True
                    break
            self._outdated = outd
        else:
            raise ZWaveCacheException("Cache not enabled")

    def cacheProperty(self, prop):
        """
        Add this property to the cache manager.
        """
        if self._useCache :
            self._cachedProperties[str(prop)] = True
        else:
            raise ZWaveCacheException("Cache not enabled")

    @property
    def objectId(self):
        """
        The id of the object.
        objectId could be None, when creating a scene for example.
        """

