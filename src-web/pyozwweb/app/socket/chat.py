# -*- coding: utf-8 -*-

"""The socketio views

Thinking about rooms.
- A room for the network : state,
- A room for nodes : list, add, remove, ...
- A room for each nodes (nodeid_1): values, parameters, ...
- A room for the controller
- A room for values

When joining a room, you will receive message from it.
"""

__license__ = """

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.

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

try:
    from gevent import monkey
    monkey.patch_all()
except ImportError:
    pass
import os, sys
import time
from threading import Thread

from flask import Flask, render_template, session, request, current_app
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect

from pyozwweb.app import socketio, app

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """NullHandler logger for python 2.6"""
        def emit(self, record):
            pass
logging.getLogger('pyozwweb').addHandler(NullHandler())

@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    logging.debug("Client %s echo message : %s", request.remote_addr, message)
    print "Client %s echo message : %s" % (request.remote_addr, message)
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my broadcast event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('close room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


#~ @socketio.on('my echo event', namespace='/socket')
#~ def socket_echo(message):
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ logging.debug("Client %s send echo" % (request.remote_addr))
    #~ logging.debug('Echo event %s', message)
    #~ socketio.emit('my echo response',
         #~ {'data': message, 'count': session['receive_count']})
#~
#~ @socketio.on('test event', namespace='/socket')
#~ def test_message(message):
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ socketio.emit('test response',
         #~ {'data': message['data'], 'count': session['receive_count']})
#~
#~ @socketio.on('my broadcast event', namespace='/socket')
#~ def test_broadcast_message(message):
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ logging.debug("Client %s has broadcast message" % (request.remote_addr))
    #~ socketio.emit('my response',
         #~ {'data': message['data'], 'count': session['receive_count']},
          #~ broadcast=True)
#~
#~ @socketio.on('join', namespace='/socket')
#~ def join(message):
    #~ data = 'No data for room %s' % message['room']
    #~ if message['room'] == 'network':
        #~ data = data_room_network(current_app.extensions['zwnetwork'])
    #~ logging.debug("Client %s has joined room %s" % (request.remote_addr, message['room']))
    #~ join_room(message['room'])
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ socketio.emit('my %s response' % message['room'],
         #~ {'data' : data,
          #~ 'count': session['receive_count']},
          #~ room=message['room'],
          #~ )
#~
#~ @socketio.on('refresh', namespace='/socket')
#~ def refresh(message):
    #~ data = 'No data for room %s' % message['room']
    #~ if message['room'] == 'network':
        #~ data = data_room_network(current_app.extensions['zwnetwork'])
    #~ logging.debug("Client %s refresh room %s" % (request.remote_addr, message['room']))
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ socketio.emit('my %s response' % message['room'],
         #~ {'data' : data,
          #~ 'count': session['receive_count']},
          #~ room=message['room'],
          #~ )
#~
#~ @socketio.on('leave', namespace='/socket')
#~ def leave(message):
    #~ leave_room(message['room'])
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ logging.debug("Client %s has leaved room %s" % (request.remote_addr, message['room']))
    #~ socketio.emit('my %s response' % message['room'],
         #~ {'data': None,
          #~ 'count': session['receive_count']},
          #~ room=message['room'],
          #~ )
#~
#~ @socketio.on('close room', namespace='/socket')
#~ def close(message):
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ logging.debug("Client %s has closed the room %s" % (request.remote_addr, message['room']))
    #~ socketio.emit('my echo response', {'data': 'Room ' + message['room'] + ' is closing.',
                         #~ 'count': session['receive_count']},
         #~ room=message['room'])
    #~ close_room(message['room'])
#~
#~ @socketio.on('my room event', namespace='/socket')
#~ def send_room_message(message):
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ logging.debug("Client %s has sent message to room %s" % (request.remote_addr, message['room']))
    #~ socketio.emit('my echo response',
         #~ {'data': message['data'], 'count': session['receive_count']},
         #~ room=message['room'])
#~
#~
#~ @socketio.on('disconnect request', namespace='/socket')
#~ def disconnect_request():
    #~ session['receive_count'] = session.get('receive_count', 0) + 1
    #~ logging.debug("Client %s disconnects." % (request.remote_addr))
    #~ socketio.emit('my echo response',
         #~ {'data': 'Disconnected!', 'count': session['receive_count']})
    #~ disconnect()
