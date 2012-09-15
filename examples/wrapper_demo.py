#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys, os

#Insert your build directory here (it depends of your python distribution)
#To get one, run the make_doc.sh command
sys.path.insert(0, os.path.abspath('../build/tmp/usr/local/lib/python2.7/dist-packages'))
from openzwave.wrapper import ZWaveWrapper

FORMAT='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
log = logging.getLogger('ZWaveWrapper')

wrapper = ZWaveWrapper(device='/dev/keyspan-2', config='../openzwave/config/', log=log)

from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()
ipshell()
