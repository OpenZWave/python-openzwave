#!/bin/bash -e

echo "-----------------------------------------------------------------"
echo "|   Retrieve sources of openzwave                               |"
echo "-----------------------------------------------------------------"
[ ! -d openzwave ] && svn checkout http://open-zwave.googlecode.com/svn/trunk/ openzwave

echo "-----------------------------------------------------------------"
echo "|   Build openzwave                                             |"
echo "-----------------------------------------------------------------"
cd openzwave/cpp/build/linux
make
cd ../../../..

echo "-----------------------------------------------------------------"
echo "|   Build python-openzwave                                      |"
echo "-----------------------------------------------------------------"
python setup.py build

if [ u != $(which sphinx-build)u ] ; then
	echo "-----------------------------------------------------------------"
	echo "|   Make documentation                                          |"
	echo "-----------------------------------------------------------------"
	python setup.py install --root=build/tmp
	cd docs
	make html
	cd ..
else
	echo "-----------------------------------------------------------------"
	echo "|   sphinx not found                                            |"
	echo "|   No documentation general                                    |"
	echo "-----------------------------------------------------------------"

fi

echo "-----------------------------------------------------------------"
echo "|   You can now install python-openzwave                        |"
echo "|   Run the following command                                   |"
echo "|   sudo ./install.sh                                           |"
echo "|   Installation directories :                                  |"
echo "|   config directory : /usr/local/share/python-openzwave        |"
if [ u != $(which sphinx-build)u ] ; then
	echo "|   Documentation : /usr/local/share/doc/python-openzwave       |"
fi
echo "-----------------------------------------------------------------"
