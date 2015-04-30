# -*- coding: utf-8 -*-

"""The listener.

Note : always log after running

2015-04-28 01:38:44,677 - openzwave - ERROR - Error in manager callback : ['Traceback (most recent call last):\n', '  File "/home/sebastien/devel/python-openzwave/src-api/openzwave/network.py", line 847, in zwcallback\n    self._handle_node_naming(args)\n', '  File "/home/sebastien/devel/python-openzwave/src-api/openzwave/network.py", line 1107, in _handle_node_naming\n    self._handle_node(self.nodes[args[\'nodeId\']])\n', '  File "/home/sebastien/devel/python-openzwave/src-api/openzwave/network.py", line 1036, in _handle_node\n    **{\'network\': self, \'node\':node})\n', '  File "/usr/lib/python2.7/dist-packages/louie/dispatcher.py", line 348, in send\n    **named\n', '  File "/usr/lib/python2.7/dist-packages/louie/robustapply.py", line 56, in robust_apply\n    return receiver(*arguments, **named)\n', '  File "/home/sebastien/devel/python-openzwave/src-web/pyozwweb/app/listener.py", line 133, in _louie_node\n    logging.debug(\'OpenZWave node notification : node %s.\', data)\n', '  File "/usr/lib/python2.7/logging/__init__.py", line 1622, in debug\n    root.debug(msg, *args, **kwargs)\n', '  File "/usr/lib/python2.7/logging/__init__.py", line 1140, in debug\n    self._log(DEBUG, msg, args, **kwargs)\n', '  File "/usr/lib/python2.7/logging/__init__.py", line 1271, in _log\n    self.handle(record)\n', '  File "/usr/lib/python2.7/logging/__init__.py", line 1281, in handle\n    self.callHandlers(record)\n', '  File "/usr/lib/python2.7/logging/__init__.py", line 1321, in callHandlers\n    hdlr.handle(record)\n', '  File "/usr/lib/python2.7/logging/__init__.py", line 747, in handle\n    self.acquire()\n', '  File "/usr/lib/python2.7/logging/__init__.py", line 698, in acquire\n    self.lock.acquire()\n', '  File "/usr/lib/python2.7/threading.py", line 173, in acquire\n    rc = self.__block.acquire(blocking)\n', '  File "_semaphore.pyx", line 112, in gevent._semaphore.Semaphore.acquire (gevent/gevent._semaphore.c:3004)\n', '  File "/usr/local/lib/python2.7/dist-packages/gevent/hub.py", line 331, in switch\n    return greenlet.switch(self)\n', 'LoopExit: This operation would block forever\n']

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

from gevent import monkey
monkey.patch_all()

import os
import sys
import time

from openzwave.network import ZWaveNetwork
from openzwave.controller import ZWaveController
from openzwave.option import ZWaveOption
import threading
#from multiprocessing import Process
from threading import Thread
from louie import dispatcher, All
#from socketIO_client import SocketIO, LoggingNamespace

from flask import Flask, render_template, session, request, current_app

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass
logging.getLogger('pyozwweb').addHandler(NullHandler())

listener = None

class ListenerThread(Thread):
    def __init__(self, _socketio, _app):
        """The constructor"""
        Thread.__init__(self)
        self._stopevent = threading.Event( )
        self.socketio = _socketio
        self.app = _app
        self.connected = False

    def connect(self):
        if self.connected == False:
            self.join_room_network()
            self.join_room_controller()
            self.join_room_node()
            self.join_room_values()
            self.connected = True
            logging.info("Listener connected")

    def run(self):
        """The running method"""
        logging.info("Start listener")
        self._stopevent.wait(5.0)
        self.connect()
        while not self._stopevent.isSet():
            self._stopevent.wait(0.1)

    def join_room_network(self):
        """Join room network"""
        #join_room("network")
        dispatcher.connect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
        dispatcher.connect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)
        dispatcher.connect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.connect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.connect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_STOPPED)
        return True

    def leave_room_network(self):
        """Leave room network"""
        #join_room("network")
        dispatcher.disconnect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
        dispatcher.disconnect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_RESETTED)
        dispatcher.disconnect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)
        dispatcher.disconnect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_READY)
        dispatcher.disconnect(self._louie_network, ZWaveNetwork.SIGNAL_NETWORK_STOPPED)
        return True

    def _louie_network(self, network):
        if network is None:
            self.socketio.emit('my network response',
                {'data': data_room_network(current_app.extensions['zwnetwork'])},
                namespace='/ozwave')
        else:
            self.socketio.emit('my network response',
                {'data': data_room_network(current_app.extensions['zwnetwork'])},
                namespace='/ozwave')
            logging.debug('OpenZWave network notification : homeid %0.8x (state:%s) - %d nodes were found.' % (network.home_id, network.state, network.nodes_count))

    def join_room_node(self):
        """Join room nodes"""
        #join_room("nodes")
        dispatcher.connect(self._louie_node, ZWaveNetwork.SIGNAL_NODE)
        return True

    def leave_room_node(self):
        """Leave room nodes"""
        #join_room("nodes")
        dispatcher.disconnect(self._louie_node, ZWaveNetwork.SIGNAL_NODE)
        return True

    def _louie_node(self, network, node):
        data=node.to_dict()
        self.socketio.emit('my node response',
            {'data': data},
            namespace='/ozwave')
        logging.debug('OpenZWave node notification : node %s.', data)

    def join_room_values(self):
        """Join room values"""
        #join_room("values")
        dispatcher.connect(self._louie_values, ZWaveNetwork.SIGNAL_VALUE)
        return True

    def leave_room_values(self):
        """Leave room values"""
        #join_room("values")
        dispatcher.disconnect(self._louie_values, ZWaveNetwork.SIGNAL_VALUE)
        return True

    def _louie_values(self, network, node, value):
            with self.app.test_request_context():
                from flask import request
                if network is None:
                    self.socketio.emit('my values response',
                                       {'data': {'node_id':None, 'homeid':None, 'value_id':None},},
                                       namespace='/ozwave')
                    logging.debug('OpenZWave values notification : Network is None.')
                elif node is None:
                    logging.debug('OpenZWave values notification : Node is None.')
                    self.socketio.emit('my values response',
                                       {'data': {'node_id':None, 'homeid':network.home_id_str, 'value_id':None},},
                                       namespace='/ozwave')
                elif value is None:
                    self.socketio.emit('my values response',
                                       {'data': {'node_id':node.node_id, 'homeid':network.home_id_str, 'value_id':None},},
                                       namespace='/ozwave')
                    logging.debug('OpenZWave values notification : Value is None.')
                else:
                    self.socketio.emit('my values response',
                                       {'data': network.nodes[node.node_id].values[value.value_id].to_dict(),},
                                       namespace='/ozwave')
                    logging.debug('OpenZWave values notification : homeid %0.8x - node %d - value %d.', network.home_id, node.node_id, value.value_id)

    def join_room_controller(self):
        """Join room controller"""
        #join_room("values")
        dispatcher.connect(self._louie_controller, ZWaveController.SIGNAL_CTRL_WAITING)
        dispatcher.connect(self._louie_controller, ZWaveController.SIGNAL_CONTROLLER)
        return True

    def leave_room_controller(self):
        """Leave room controller"""
        #join_room("values")
        dispatcher.disconnect(self._louie_controller, ZWaveController.SIGNAL_CTRL_WAITING)
        dispatcher.disconnect(self._louie_controller, ZWaveController.SIGNAL_CONTROLLER)
        return True

    def _louie_controller(self, state, message, network, controller):
            with self.app.test_request_context():
                from flask import request
#               request = req
                if network is None or controller is None:
                    self.socketio.emit('my message response',
                                       {'data': {'state':None, 'message':None},},
                                       namespace='/ozwave')
                    logging.debug('OpenZWave controller message : Nework or Controller is None.')
                else:
                    self.socketio.emit('my message response',
                                       {'data': {'state':state, 'message':message},},
                                       namespace='/ozwave')
                    logging.debug('OpenZWave controller message : state %s - message %s.', state, message)

    def stop(self):
        """Stop the tread"""
        self.leave_room_node()
        self.leave_room_values()
        self.leave_room_controller()
        self.leave_room_network()
        self._stopevent.set( )
        logging.info("Stop listener")

def start_listener(app_, socketio_):
    global listener
    if listener is None:
        listener = ListenerThread(socketio_, app_)
        listener.start()
    return listener

def stop_listener():
    global listener
    listener.stop()
    listener = None
