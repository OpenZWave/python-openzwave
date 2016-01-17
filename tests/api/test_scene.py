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
import six
if six.PY3:
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

class TestScene(TestApi):
    count = 0
    level = 70

    def test_005_scene_add_remove(self):
        self.count = self.network.scenes_count
        self.assertTrue(self.count >= 0)
        self.sceneid = self.network.create_scene("TestUnit Scene")
        self.assertTrue(self.sceneid > 0)
        scene = self.network.get_scenes()[self.sceneid]
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_switches() :
                ret = scene.add_value(val, True)
                self.assertTrue(ret)
        scene = self.network.get_scenes()[self.sceneid]
        for node in self.network.nodes:
            for val in self.network.nodes[node].get_dimmers() :
                ret = scene.add_value(val, self.level)
                self.assertTrue(ret)
        self.assertTrue(self.network.scene_exists(self.sceneid))
        scene = self.network.get_scenes()[self.sceneid]
        self.assertTrue(scene.activate())
        self.assertEqual(self.network.scenes_count, self.count + 1)
        ret = self.network.remove_scene(self.sceneid)
        self.assertTrue(ret)
        self.assertEqual(self.network.scenes_count, self.count)

    def test_010_scenes_to_dict(self):
        dscenes = self.network.scenes_to_dict()
        self.assertEqual(type(dscenes), type({}))
        res = json.dumps(dscenes)
        self.assertNotEqual(res, None)
        self.assertTrue(len(res)>0)

    def test_020_scene_to_dict(self):
        scenes = self.network.get_scenes()
        for scene in scenes:
            try :
                scene = scenes[scene].to_dict()
                self.assertEqual(type(scene), type({}))
                res = json.dumps(scene)
            except TypeError:
                res = None
            self.assertNotEqual(res, None)

if __name__ == '__main__':
    sys.argv.append('-v')
    unittest.main()
