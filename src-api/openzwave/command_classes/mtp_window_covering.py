# -*- coding: utf-8 -*-
"""
This file is part of **python-openzwave**
project https://github.com/OpenZWave/python-openzwave.
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

from .command_class_base import CommandClassBase

# Move To Position Window Covering Command Class - Obsolete
# Application
COMMAND_CLASS_MTP_WINDOW_COVERING = 0x51


# noinspection PyAbstractClass
class MtpWindowCovering(CommandClassBase):
    """
    Mtp Window Covering Command Class

    symbol: `COMMAND_CLASS_MTP_WINDOW_COVERING`
    """

    def __init__(self):
        CommandClassBase.__init__(self)
        self._cls_ids += []
