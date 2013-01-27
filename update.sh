#!/bin/bash -e

echo "-----------------------------------------------------------------"
echo "|   Update sources of python-openzwave                          |"
echo "-----------------------------------------------------------------"
hg pull https://code.google.com/p/python-openzwave/
hg update

echo "-----------------------------------------------------------------"
echo "|   Update sources of openzwave                                 |"
echo "-----------------------------------------------------------------"
if [ -d openzwave ] ; then
    echo "Update openzwave directory"
    svn update openzwave
else
    echo "Checkout openzwave directory"
    svn checkout http://open-zwave.googlecode.com/svn/trunk/ openzwave
fi

echo "-----------------------------------------------------------------"
echo "|   Sources updated                                             |"
echo "-----------------------------------------------------------------"
