# -*- coding: utf-8 -*-

"""The Rooms

"""

__license__ = """

This file is part of **python-openzwave** project https://github.com/bibi21000/python-openzwave.

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
__author__ = 'Sébastien GALLET aka bibi21000'
__email__ = 'bibi21000@gmail.com'

import os, sys
import time
from threading import Thread

from flask import Blueprint, Flask, render_template, session, request, current_app
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect

import libopenzwave
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption

from louie import dispatcher, All

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass
logging.getLogger('pyozwweb').addHandler(NullHandler())

def data_room_network(network):
    """The network room"""
    if network is None:
        data={
            'state' : None,
            'state_str' : None,
            'home_id' : None,
            'nodes_count' : 0,
        }
    else:
        data={
            'state' : network.state,
            'state_str' : network.state_str,
            'home_id' : network.home_id_str,
            'nodes_count' : network.nodes_count,
        }
    return data

def data_room_values(network, node_id):
    """The values room"""
    data=network.nodes_to_dict()
    logging.debug('data_room_nodes : %s', data)
    return data
