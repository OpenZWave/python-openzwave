#!/bin/bash -e

echo "-----------------------------------------------------------------"
echo "|   Install python-openzwave  lib                               |"
echo "-----------------------------------------------------------------"
python setup-lib.py install --record install.files

echo "-----------------------------------------------------------------"
echo "|   Install python-openzwave  api                               |"
echo "-----------------------------------------------------------------"
python setup-api.py install --record install.files

echo "-----------------------------------------------------------------"
echo "|   Installation done                                           |"
echo "|   Run the following command to unistall python-openzwave :    |"
echo "|   sudo ./uninstall.sh                                         |"
echo "-----------------------------------------------------------------"
