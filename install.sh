#!/bin/bash -e

echo "-----------------------------------------------------------------"
echo "|   Install python-openzwave                                    |"
echo "-----------------------------------------------------------------"
python setup.py install --record install.files

echo "-----------------------------------------------------------------"
echo "|   Installation done                                           |"
echo "|   Run the following command to unistall python-openzwave :    |"
echo "|   sudo ./uninstall.sh                                         |"
echo "-----------------------------------------------------------------"
