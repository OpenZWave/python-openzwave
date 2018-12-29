#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Unittests for the pyozwwzb Server.

See http://werkzeug.pocoo.org/docs/0.9/test/
See http://werkzeug.pocoo.org/docs/0.9/wrappers/

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

import sys
import time
import logging
import unittest

#~ from flask.ext.socketio import SocketIO, emit, join_room, leave_room, close_room, disconnect
#~ from flask.ext.socketio.test_client import SocketIOTestClient
#~ from tests.web.common import FlaskTestCase

#~ class FlaskServerTest(FlaskTestCase):

    #~ def test_000_server_start(self):
        #~ rv = self.client.get('/')
        #~ self.assertTrue('Welcome to PyOzwWeb' in rv.data)

    #~ def test_001_error_404(self):
        #~ rv = self.client.get('/bad_page')
        #~ self.assertEqual(rv.status,'404 NOT FOUND')

    #~ def test_100_home_is_up(self):
        #~ rv = self.client.get('/')
        #~ self.assertEqual(rv.status,'200 OK')

    #~ def test_200_controller_is_up(self):
        #~ rv = self.client.get('/controller')
        #~ self.assertEqual(rv.status,'200 OK')

    #~ def test_300_values_is_up(self):
        #~ rv = self.client.get('/values')
        #~ self.assertEqual(rv.status,'200 OK')

    #~ def test_400_controller_is_up(self):
        #~ rv = self.client.get('/debug')
        #~ self.assertEqual(rv.status,'200 OK')

    #~ def test_500_node_is_up(self):
        #~ rv = self.client.get('/node/1')
        #~ self.assertEqual(rv.status,'200 OK')

    #~ def test_600_map_is_up(self):
        #~ rv = self.client.get('/map')
        #~ self.assertEqual(rv.status,'200 OK')

    #~ def test_700_scenes_is_up(self):
        #~ rv = self.client.get('/scenes')
        #~ self.assertEqual(rv.status,'200 OK')

    #def test_500_socketio_home(self):
    #    rv = self.app.get('/socketio/')
    #    self.assertEqual(rv.status,'200 OK')

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
