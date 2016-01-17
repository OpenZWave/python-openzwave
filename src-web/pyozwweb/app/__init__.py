# -*- coding: utf-8 -*-

"""pyozwweb app module.

Use factories : http://flask.pocoo.org/docs/0.10/patterns/appfactories/
Use templates : https://pythonhosted.org/Flask-Themes/
Use Flask-SocketIO : https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/app.py
Use socket-IO : https://github.com/abourget/gevent-socketio/blob/master/examples/flask_chat/chat.py

Help : http://www.scratchinginfo.net/useful-jquery-datatables-examples-tutorials-and-plugins/

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

from gevent import monkey
monkey.patch_all()

import os
import sys
import time

from flask import Flask, current_app, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect

#from flask_fanstatic import Fanstatic
#from flask.ext.sqlalchemy import SQLAlchemy

from openzwave.network import ZWaveNetwork
#from openzwave.network import ZWaveNetworkSingleton as ZWaveNetwork
from openzwave.option import ZWaveOption
#from openzwave.option import ZWaveOptionSingleton as ZWaveOption
import threading
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

import signal

from listener import start_listener, stop_listener

fanstatic = None
app = None
socketio = None

def run_app(app_, socketio_, debug=False):

    def signal_term_handler(signal, frame):
        print('got SIGTERM')
        stop_all()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_term_handler)
    signal.signal(signal.SIGINT, signal_term_handler)

    global socketio
    socketio = socketio_
    global app
    app = app_
    logging.debug("Current config %s"%app.config)
    if 'listener' not in app.extensions or app.extensions['listener'] is None:
        app.extensions['listener'] = start_listener(app_, socketio_)
    app_.debug = app.config['DEBUG']
    app_.testing = app.config['TESTING']
    logging.debug("Flask url maps %s" % app.url_map)
    socketio.run(app, use_reloader=app.config['RELOADER'],host=app.config['HOST'], port=app.config['PORT'])
    #print("App has ran")
    #stop_all()

def stop_all():
    stop_listener()
    global app
    stop_zwnetwork(app.extensions['zwnetwork'])

def create_app(config_object='pyozwweb.config.DevelopmentConfig'):
    from gevent import monkey
    monkey.patch_all()

    _app = Flask(__name__)
    _app.config.from_object(config_object)
    global app
    app = _app
    #Logging configuration
    import logging.config, yaml
    logs = yaml.load(open(app.config['LOGGING_CONF']))
    logging.config.dictConfig(logs)
    logging.debug("Load config from %s"%config_object)
    if logs['loggers']['libopenzwave']['level'] == 'DEBUG':
        ZWAVE_DEBUG = "Debug"
    elif logs['loggers']['libopenzwave']['level'] == 'ERROR':
        ZWAVE_DEBUG = "Error"
    elif logs['loggers']['libopenzwave']['level'] == 'WARNING':
        ZWAVE_DEBUG = "Warning"
    else:
        ZWAVE_DEBUG = "Info"
    #Application configuration
    from ConfigParser import SafeConfigParser
    settings = SafeConfigParser()
    settings.read(app.config['APP_CONF'])
    section = "zwave"
    if settings.has_option(section, 'device'):
        app.config['ZWAVE_DEVICE'] = settings.get(section, 'device')
    section = "server"
    if settings.has_option(section, 'host'):
        app.config['HOST'] = settings.get(section, 'host')
    if settings.has_option(section, 'port'):
        app.config['PORT'] = settings.getint(section, 'port')
    #Flask stuff
    #global fanstatic
    #fanstatic = Fanstatic(app)
    global socketio
    socketio = SocketIO(app)
    if not app.config['DEBUG']:
        install_secret_key(app)
    import views
    from socket import ozwave, chat
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    if 'zwnetwork' not in app.extensions or app.extensions['zwnetwork'] is None:
        app.extensions['zwnetwork'] = start_zwnetwork(app)
    return app, socketio

def start_zwnetwork(app):
    options = ZWaveOption(device=app.config['ZWAVE_DEVICE'], config_path=app.config['ZWAVE_DIR'], user_path=app.config['USER_DIR'])
    options.set_log_file("OZW_Log.log")
    options.set_append_log_file(False)
    options.set_console_output(False)
    options.set_save_log_level(app.config['ZWAVE_DEBUG'])
    options.set_logging(app.config['ZWAVE_LOGGING'])
    options.lock()
    zwnetwork = ZWaveNetwork(options)
    return zwnetwork

def stop_zwnetwork(zwnetwork):
    if zwnetwork is not None:
        zwnetwork.stop()
        zwnetwork.destroy()
        #time.sleep(1.5)
        zwnetwork = None

########################
# Configure Secret Key #
########################
def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)

#from app.users.views import mod as usersModule
#app.register_blueprint(usersModule)

# Later on you'll import the other blueprints the same way:
#from app.comments.views import mod as commentsModule
#from app.posts.views import mod as postsModule
#app.register_blueprint(commentsModule)
#app.register_blueprint(postsModule)

#try:
#    __import__('pkg_resources').declare_namespace(__name__)
#except:
#    # bootstrapping
#    pass
#
#from flask import Flask
#import zmq
#
#app = Flask(__name__)
#context = zmq.Context()
#endpoint_cmd = "tcp://*:14015"
#socket = context.socket(zmq.REQ)
#socket.setsockopt(zmq.LINGER, 0)
#socket.connect(endpoint_cmd)
#
#import views
