# -*- coding: utf-8 -*-

"""
.. module:: tests

This file is part of **python-openzwave** project https://github.com/bibi21000/python-openzwave.
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

#The common sleep dealy to wait for network
#We wait 1*SLEEP for network.STATE_AWAKED
#After that we wait 1*SLEEP for network.STATE_READY
SLEEP = 30

import sys, os
import time
import unittest
import threading
import logging
import json as mjson

from nose.plugins.skip import SkipTest

sys.path.insert(1, os.path.abspath('..'))
import pyozw_version

pyozw_version=pyozw_version.pyozw_version

class TestPyZWave(unittest.TestCase):
    """Grand mother
    """
    device = "/dev/ttyUSB0"
    ozwlog = "Debug"
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
        try:
            os.makedirs(self.userpath)
        except:
            pass

    def skipTest(self, message):
        """Skip a test
        """
        if self.skip == True:
            raise SkipTest("%s" % (message))

    def skipTravisTest(self, message):
        """Skip a test on travis
        """
        if 'TRAVIS_OS_NAME' in os.environ:
            raise SkipTest("%s" % ("Skip on travis : %s" % message))

    def skipNotReady(self, message):
        """Skip a test because zwave network is not ready
        """
        raise SkipTest("%s" % ("Skip NotReady : %s" % message))

    def wipTest(self):
        """Work In Progress test
        """
        raise SkipTest("Work in progress")

    def touchFile(self, path):
        with open(path, 'a'):
            os.utime(path, None)
