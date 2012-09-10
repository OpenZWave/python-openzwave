""" This file is part of py-openzwave project (https://github.com/maartendamen/py-openzwave).

License
=======

py-openzwave is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-openzwave is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with py-openzwave. If not, see U{http://www.gnu.org/licenses}.

@author: maartendamen
@author: bibi21000 <bibi21000@gmail.com>
@license: GPL(v3)
"""
from mylibc cimport uint32, uint64, int32, int16, uint8, int8
from mylibc cimport string
from libcpp cimport bool

cdef extern from "Options.h" namespace "OpenZWave":
    cdef cppclass Options:
        bool Lock()

cdef extern from "Options.h" namespace "OpenZWave::Options":
    Options* Create(string a, string b, string c)

