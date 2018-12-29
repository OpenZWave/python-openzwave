# -*- coding: utf-8 -*-

"""
.. module:: tests

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

import os
import shutil
import sys
import time
import unittest
import threading
import logging
import json
#~ import bson
import six

#The common sleep dealy to wait for network
#We wait 1*SLEEP for network.STATE_AWAKED
#After that we wait 1*SLEEP for network.STATE_READY
SLEEP = 45

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def json_dumps(data_as_object):
    #~ return json.dumps(data_as_object, default=json_util.default)
    return json.dumps(data_as_object, cls=SetEncoder)

def json_loads(data_as_string):
    #~ return json.loads(data_as_string, object_hook=json_util.object_hook)
    return json.loads(data_as_string)

from nose.plugins.skip import SkipTest

sys.path.insert(1, os.path.abspath('..'))
import pyozw_version

pyozw_version=pyozw_version.pyozw_version

class TestPyZWave(unittest.TestCase):
    """Grand mother
    """
    device = "/dev/ttyUSB0"
    ozwlog = "Debug"
    ozwout = True
    pylog = logging.DEBUG
    userpath = ".tests_user_path"

    @classmethod
    def tearDownClass(self):
        try:
            shutil.rmtree(self.userpath)
        except:
            pass

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=self.pylog)
        self.skip = True
        if 'NOSESKIP' in os.environ:
            self.skip = eval(os.environ['NOSESKIP'])
        self.skipManual = True
        if 'MANUALSKIP' in os.environ:
            self.skipManual = eval(os.environ['MANUALSKIP'])
        try:
            os.makedirs(self.userpath)
        except:
            pass

    @classmethod
    def skipTest(self, message):
        """Skip a test
        """
        if self.skip == True:
            raise SkipTest("%s" % (message))

    def skipPython3(self):
        """Skip a test on python 3
        """
        if six.PY3:
            raise SkipTest("Skip on Python 3")

    def skipTravisTest(self, message):
        """Skip a test on travis
        """
        if 'TRAVIS_OS_NAME' in os.environ:
            raise SkipTest("%s" % ("travis : %s" % message))

    def skipManualTest(self, message=''):
        """Skip a manual test (need human intervention)
        """
        if self.skipManual == True:
            raise SkipTest("%s" % ("manual test (%s)" % message))

    def skipNotReady(self, message):
        """Skip a test because zwave network is not ready
        """
        raise SkipTest("%s" % ("network NotReady : %s" % message))

    def wipTest(self):
        """Work In Progress test
        """
        raise SkipTest("Work in progress")

    def touchFile(self, path):
        with open(path, 'a'):
            os.utime(path, None)

    def rmFile(self, path):
        if os.path.isfile(path):
            os.remove(path)
