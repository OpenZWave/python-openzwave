# -*- coding: utf-8 -*-

"""Unittests for the pyozwwzb Server.

Credits : https://flask-testing.readthedocs.org/en/latest/
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

import sys, os
import time
import logging
import json as mjson

from flask import Flask

from pyozwweb.app import create_app, run_app, stop_all

from tests.common import SLEEP
from tests.common import TestPyZWave
#import threading

from multiprocessing import Process
#from threading import Thread

class TestServer(Process):
    def __init__(self):
        """The constructor"""
        Process.__init__(self)
        self.socketio = None
        self.app = None
        self.client = None
        self.app, self.socketio = create_app(config_object='pyozwweb.config.TestingConfig')
        #self._stopevent = threading.Event( )

    def run(self):
        """The running method"""
        run_app(self.app, self.socketio)
        #while not self._stopevent.isSet():
        #    self._stopevent.wait(1.0)

    def stop(self):
        """Stop the tread"""
        print 'got stop'
        Process.terminate(self)
        time.sleep(2.0)
        #self._stopevent.wait(2.0)
        self.socketio = None
        self.app = None
        self.client = None

class FlaskTestCase(TestPyZWave):

    @classmethod
    def setUpClass(self):
        super(FlaskTestCase, self).setUpClass()
        self.testserver = TestServer()
        #global socket_server
        #socket_server = self.testserver
        self.testserver.start()
        #app, socketio = create_app(config_object='pyozwweb.config.TestingConfig')
        #app.testing = True
        #run_app(app, socketio)
        self.app = self.testserver.app
        self.socketio = self.testserver.socketio
        self.client = self.testserver.app.test_client()
        time.sleep(7.0)

    @classmethod
    def tearDownClass(self):
        self.testserver.stop()
        self.testserver.join()
        self.socketio = None
        time.sleep(2.0)
        self.app = None
        self.client = None
        self.testserver = None
        super(FlaskTestCase, self).tearDownClass()

