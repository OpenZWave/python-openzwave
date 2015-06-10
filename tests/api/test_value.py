#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
.. module:: tests

This file is part of **python-openzwave** project https://github.com/OpenZWave/python-openzwave.
    :platform: Unix, Windows, MacOS X
    :sinopsis: openzwave Library

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

import sys, os, shutil
import time
import unittest
from pprint import pprint
import datetime
import random
import socket
import libopenzwave
import re
import time
import sys
if sys.hexversion >= 0x3000000:
    from pydispatch import dispatcher
else:
    from louie import dispatcher
import libopenzwave
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from tests.common import pyozw_version
from tests.common import SLEEP
from tests.api.common import TestApi
from tests.common import TestPyZWave
import json

class TestValue(TestApi):

    def test_200_values_to_dict(self):
        for node in self.network.nodes:
            for value in self.network.nodes[node].values:
                val = self.network.nodes[node].values[value].to_dict()
                self.assertEqual(type(val), type({}))
                try :
                    res = json.dumps(val)
                except TypeError:
                    res = None
                self.assertNotEqual(res, None)

    def test_210_values_check_data(self):
        for node in self.network.nodes:
            for value in self.network.nodes[node].values:
                val = self.network.nodes[node].values[value]
                if val.is_read_only == False:
                    if val.type == "Bool":
                        for data in ['False', 'false', '0']:
                            self.assertFalse(val.check_data(data))
                        for data in ['True', 'true', '1', "what else"]:
                            self.assertTrue(val.check_data(data))
                    elif val.type == "Byte":
                        pass
                    elif val.type == "Decimal":
                        pass
                    elif val.type == "Int":
                        pass
                    elif val.type == "Short":
                        pass
                    elif val.type == "String":
                        pass
                    elif val.type == "Button":
                        pass
                    elif val.type == "List":
                        pass

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
