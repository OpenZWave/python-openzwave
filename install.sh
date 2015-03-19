#!/bin/bash -e
#Deprecated : will be removed in the next releases. Look at Makefile

echo "-----------------------------------------------------------------"
echo "|   Uninstall python-openzwave                                  |"
echo "-----------------------------------------------------------------"
set +e
./uninstall.sh
set -e

echo "-----------------------------------------------------------------"
echo "|   Install python-openzwave  lib                               |"
echo "-----------------------------------------------------------------"
python setup-lib.py install --record install.files

echo "-----------------------------------------------------------------"
echo "|   Install python-openzwave  api                               |"
echo "-----------------------------------------------------------------"
python setup-api.py install --record install.tmp
cat install.tmp >>install.files
rm install.tmp
rm -Rf python_openzwave_lib.egg-info >/dev/null 2>&1
rm -Rf python_openzwave_api.egg-info >/dev/null 2>&1

echo "-----------------------------------------------------------------"
echo "|   Installation done                                           |"
echo "|   You can unistall python-openzwave using :                   |"
echo "|   sudo ./uninstall.sh                                         |"
echo "-----------------------------------------------------------------"
