# -*- coding: utf-8 -*-
"""
.. module:: openzwave.singleton

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave wrapper

.. moduleauthor:: Kevin Schlosser (@kdschlosser)

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


class InstanceSingleton(type):
    """
    InstanceSingleton metaclass

    child = class that contains this class as a metaclass
    parent = this class

    This class gets used on 2 different occasions.

    The first occasion is when the child class gets compiled. we are able to
    get in front of that compilation because this classes `__init__` gets
    called first. We use that to set a class level variable, `_instances`.
    This variable gets created for every child of this class. The variables
    are not connected to any other child classes. so they are unique. The
    variable is a dict that holds all of the unique instances of that
    child class.

    The second time in which this class gets used is when one of the child
    classes gets constructed. the `__call__` method of this class gets called
    before the `__init__`. the `__call__` method is supposed to return a new
    instance. We do not want to do this is one already exists. So when a new
    instance is supposed to be created we use the `__call__` method to check
    for the existence of an instance. If it does not exist we create a new
    instance, if it does exist we return the already created one.

    How we are able to check if an instance already exists is actually pretty
    crafty. I use the args and kwargs that are passed when the construction of
    a new instance is supposed to take place. I iterate over a sorted list of
    the keys in kwargs and add the values to the args creating a tuple of all
    of the arguments that have been passed. A python dict is able to use a
    tuple as a key. For our use this key will be unique because each class
    that uses this metaclass makes use of an object_id.

    This is a pretty neat spin on making singletons. Singletons are typically
    used so that only a single instance of a class can exist. Our need is to
    make sure that only a single instance of a ZWave object exists, whether it
    be a node, value, controller, network, or options.

    If this library is used on multiple ZSticks at the same time the
    ZWaveOptions class is going to have to have 2 different locations supplied
    for it's user config data. For the ZWaveNetwork class an instance of
    ZWaveOptions has to be passed. and since that has to be unique it now makes
    the ZWaveNetwork instance unique. and the ZWaveNetwork instance has to be
    used on all other classes. it's a domino effect.
    """

    def __init__(cls, *args, **kwargs):
        """
        InstanceSingleton metaclass constructor.
        """
        super(InstanceSingleton, cls).__init__(*args, **kwargs)

        cls._instances = {}

    def __call__(cls, *args, **kwargs):
        """
        This gets called before the __init__ method of the class the has
        InstanceSingleton as a metaclass.
        """

        key = list(args)
        for k in sorted(kwargs.keys()):
            key += [kwargs[k]]

        key = tuple(key)

        if key not in cls._instances:
            cls._instances[key] = (
                super(InstanceSingleton, cls).__call__(*args, **kwargs)
            )

        return cls._instances[key]
