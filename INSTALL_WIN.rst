:orphan:

======================================
Installing python-openzwave on Windows
======================================


How To Build python-openzwave on Windows with VS2015
====================================================

Assuming Python 3.5 is set in PATH
Assuming your python environment has pip, cython, setuptools


Get sources
-----------

.. code-block:: bash

    git clone https://github.com/openzwave/python-openzwave.git

    cd python-openzwave
    git clone git://github.com/OpenZWave/open-zwave.git openzwave

    cd openzwave
    git checkout Dev
    cd ..
    git checkout python3


Build open-zwave
----------------

Open openzwave/cpp/build/windows/vs2010/OpenZWave.sln in Visual Studio

When asked, accept the project upgrade to VS2015

Build Win32|Release


Build python-openzwave lib
--------------------------

Patch libopenzwave.pyx

Cause: ValueID has no default constructor and cython needs one for allocating objects on the stack

Fix: Allocate object on the the heap as a workaround

Open test/python-openzwave/src-lib/libopenzwave/libopenzwave.pyx

Go to line 437 and change:

.. code-block:: bash

    values_map.insert(pair[uint64_t, ValueID](v.GetId(), v))

To:

.. code-block:: bash

    newPair = new pair[uint64_t, ValueID](v.GetId(), v)
    values_map.insert(deref(newPair))
    del newPair

From a Command Prompt, build it :

.. code-block:: bash

    python setup-lib build
    python setup-api build

And install it (in a virtualenv if needed) :

.. code-block:: bash

    python setup-lib install
    python setup-api install

Reference : https://github.com/OpenZWave/python-openzwave/issues/53
