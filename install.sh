#!/bin/bash -e

echo "------------------------------------------------------------"
echo "|   Retrieve sources of openzwave                          |"
echo "------------------------------------------------------------"
svn checkout http://open-zwave.googlecode.com/svn/trunk/ openzwave

echo "------------------------------------------------------------"
echo "|   Build openzwave                                        |"
echo "------------------------------------------------------------"
cd openzwave/cpp/build/linux
make
cd ../../../..

echo "------------------------------------------------------------"
echo "|   Build py-openzwave                                     |"
echo "------------------------------------------------------------"
python setup build

echo "------------------------------------------------------------"
echo "|   You can now install py-openzwave                       |"
echo "|   Run the following command                              |"
echo "|   sudo python setup.py install                           |"
echo "------------------------------------------------------------"
