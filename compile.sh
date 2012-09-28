#!/bin/bash -e

CLEAN=0
[ 'u'$1 == 'uclean' ] && CLEAN=1

echo "-----------------------------------------------------------------"
echo "|   Retrieve sources of openzwave                               |"
echo "-----------------------------------------------------------------"
[ ! -d openzwave ] && svn checkout http://open-zwave.googlecode.com/svn/trunk/ openzwave

echo "-----------------------------------------------------------------"
echo "|   Build openzwave                                             |"
echo "-----------------------------------------------------------------"
cd openzwave/cpp/build/linux
[ $CLEAN -eq 1 ] && make clean
make
cd ../../../..

echo "-----------------------------------------------------------------"
echo "|   Build python-openzwave                                      |"
echo "-----------------------------------------------------------------"
[ $CLEAN -eq 1 ] && python setup.py clean
[ $CLEAN -eq 1 ] && rm -Rf build/
[ $CLEAN -eq 1 ] && rm -Rf docs/_build
[ $CLEAN -eq 1 ] && rm lib/libopenzwave.cpp
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
