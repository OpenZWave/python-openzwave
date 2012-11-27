#!/bin/bash -e

echo "------------------------------------------------------------"
echo "|   Install openzwave in tmp                               |"
echo "------------------------------------------------------------"
set +e
rm zwcfg_*.xml
rm zwscene.xml
set -e
cd ..
python setup-lib.py install --root=build/tmp
python setup-api.py install --root=build/tmp
cd tests
python test_all.py $*
