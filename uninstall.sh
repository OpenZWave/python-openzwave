#!/bin/bash -e
#Deprecated : will be removed in the next releases. Look at Makefile

echo "-----------------------------------------------------------------"
echo "|   Uninstall python-openzwave                                  |"
echo "-----------------------------------------------------------------"
[ ! -f install.files ] && echo "Can't find install.files. Abort !!" && exit 1
rm -Rf $(cat install.files)

#Some file are not deleted
rm -Rf /usr/local/lib/python2.7/dist-packages/openzwave \
    /usr/local/lib/python2.7/dist-packages/python_openzwave_api* \
    /usr/local/lib/python2.6/dist-packages/openzwave \
    /usr/local/lib/python2.6/dist-packages/python_openzwave_api* \
    /usr/local/share/python-openzwave

echo "-----------------------------------------------------------------"
echo "|   Uninstallation done                                         |"
echo "-----------------------------------------------------------------"
