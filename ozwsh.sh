#!/bin/bash -e

echo "------------------------------------------------------------"
echo "|   Install openzwave in tmp                               |"
echo "------------------------------------------------------------"
python setup-lib.py install --root=build/tmp
python setup-api.py install --root=build/tmp

echo "------------------------------------------------------------"
echo "|   Run ozwsh                                           |"
echo "------------------------------------------------------------"
./manager/ozwsh.py $*
