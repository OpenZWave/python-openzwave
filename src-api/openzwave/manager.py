# -*- coding: utf-8 -*-
"""
.. module:: openzwave.manager

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

import libopenzwave
import os
import inspect
import traceback
import logging

logger = logging.getLogger(__name__)

if 'MAKE_IDE_HAPPY' in os.environ:
    # This is here to make an IDE happy. It never actually gets run.
    ZWaveManager = libopenzwave.PyManager

else:

    class MethodWrapper(object):
        """
        Wrapper for libopenzwave.PyManager methods.
        """

        def __init__(self, method):
            self.__dict__.update(method.__dict__)
            self.__method = method
            self.__call__ = self.__call

        def __call(self, *args, **kwargs):
            try:
                return self.__method(*args, **kwargs)
            except:
                logger.error(traceback.format_exc())


    class ZWaveManager(object):
        """
        Wrapper around libopenzwave.PyManager.

        Exceptions that bubble up in OpenZWave was added in version 1.6. So
        to keep the program from stalling this wrapper makes it easier to
        handle the exception catching and logging.
        """
        def __init__(self):
            self.__manager = libopenzwave.PyManager()

        def __getattr__(self, item):
            if item in self.__dict__:
                return self.__dict__[item]

            if hasattr(self.__dict__['__manager'], item):
                attr = getattr(self.__dict__['__manager'], item)

                if inspect.ismethod(attr) or inspect.isfunction(attr):
                    self.__dict__[item] = attr = MethodWrapper(attr)

                return attr

            raise AttributeError(item)

        def __setattr__(self, key, value):
            if key == '__manager':
                self.__dict__[key] = value
            else:
                setattr(self.__dict__['__manager'], key, value)
