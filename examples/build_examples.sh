#!/bin/bash -e

echo "------------------------------------------------------------"
echo "|   Install openzwave in tmp                               |"
echo "------------------------------------------------------------"
cd ..
python setup-lib.py install --root=build/tmp
python setup-api.py install --root=build/tmp
cd examples
