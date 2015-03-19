#!/bin/bash -e
#Deprecated : will be removed in the next releases. Look at Makefile

echo "-----------------------------------------------------------------"
echo "|   Update sources of python-openzwave                          |"
echo "-----------------------------------------------------------------"
git pull

echo "-----------------------------------------------------------------"
echo "|   Update sources of openzwave                                 |"
echo "-----------------------------------------------------------------"
if [ -d openzwave ]; then
    cd openzwave
    git pull
    cd ..
else
    git clone git://github.com/OpenZWave/open-zwave.git openzwave
fi

echo "-----------------------------------------------------------------"
echo "|   Sources updated                                             |"
echo "-----------------------------------------------------------------"
