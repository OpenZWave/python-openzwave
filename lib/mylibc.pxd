"""
This file is part of **python-openzwave** project http://code.google.com/p/python-openzwave.

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

ctypedef unsigned int uint32
ctypedef unsigned long uint64
ctypedef int int32
ctypedef short int16
ctypedef unsigned char uint8
ctypedef signed char int8

cdef extern from "Python.h":
    void PyEval_InitThreads()

cdef extern from "<string>" namespace "std":
    cdef cppclass string:
        string()
        string(char *)
        string (size_t n, char c)
        char * c_str()

cdef extern from "stdlib.h":
    void* malloc(size_t size)
    void free(void* ptr)

cdef extern from "<new>" namespace "std":
    void* new(size_t size)
    void delete(void* ptr)
#    void* new[](size_t size)
#    void delete[](void* ptr)
