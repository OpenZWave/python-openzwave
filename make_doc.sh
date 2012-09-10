#!/bin/bash -e

echo "------------------------------------------------------------"
echo "|   Install openzwave in tmp                               |"
echo "------------------------------------------------------------"
python setup.py install --root=build/tmp

echo "------------------------------------------------------------"
echo "|   Generate documentation                                 |"
echo "------------------------------------------------------------"
cd docs
make html
cp -Rf _build/html ../build/
