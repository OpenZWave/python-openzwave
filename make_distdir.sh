#!/bin/bash -e

echo "------------------------------------------------------------"
echo "|   Build openzwave in build/tmp                       |"
echo "------------------------------------------------------------"
python setup-lib.py install --root=build/tmp
python setup-api.py install --root=build/tmp

echo "------------------------------------------------------------"
echo "|   Generate documentation                                 |"
echo "------------------------------------------------------------"
cd docs
make html
cd ..

echo "------------------------------------------------------------"
echo "|   Install openzwave in build/distdir                     |"
echo "------------------------------------------------------------"
python setup-lib.py install --root=build/distdir
python setup-api.py install --root=build/distdir

echo "------------------------------------------------------------"
echo "|   Files are in build/distdir                             |"
echo "------------------------------------------------------------"
