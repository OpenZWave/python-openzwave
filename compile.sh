#!/bin/bash -e

CLEAN=0
[ 'u'$1 == 'uclean' ] && CLEAN=1

echo "-----------------------------------------------------------------"
echo "|   Build openzwave                                             |"
echo "-----------------------------------------------------------------"
rm -Rf openzwave/cpp/src/vers.cpp
cd openzwave/
[ $CLEAN -eq 1 ] && make clean
make
cd ..

echo "-----------------------------------------------------------------"
echo "|   Build python-openzwave                                      |"
echo "-----------------------------------------------------------------"
[ $CLEAN -eq 1 ] && python setup-lib.py clean
[ $CLEAN -eq 1 ] && python setup-api.py clean
[ $CLEAN -eq 1 ] && rm -Rf build/
[ $CLEAN -eq 1 ] && rm -Rf docs/_build
[ $CLEAN -eq 1 ] && rm lib/libopenzwave.cpp
python setup-lib.py build
python setup-api.py build

#Remove the doc generattion as it fails on Ubuntu 10.04
#if [ u != $(which sphinx-build)u ] ; then
#    echo "-----------------------------------------------------------------"
#    echo "|   Make documentation                                          |"
#    echo "-----------------------------------------------------------------"
#    python setup-lib.py install --root=build/tmp
#    python setup-api.py install --root=build/tmp
#    cd docs
#    make html
#    cd ..
#else
#    echo "-----------------------------------------------------------------"
#    echo "|   sphinx not found                                            |"
#    echo "|   No documentation general                                    |"
#    echo "-----------------------------------------------------------------"#
#
#fi

echo "-----------------------------------------------------------------"
echo "|   You can now install python-openzwave                        |"
echo "|   Run the following command                                   |"
echo "|   sudo ./install.sh                                           |"
#echo "|   Installation directories :                                  |"
#echo "|   config directory : /usr/local/share/python-openzwave        |"
#if [ u != $(which sphinx-build)u ] ; then
#    echo "|   Documentation : /usr/local/share/doc/python-openzwave       |"
#fi
echo "-----------------------------------------------------------------"
