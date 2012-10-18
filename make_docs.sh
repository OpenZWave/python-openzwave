#!/bin/bash -e

echo "------------------------------------------------------------"
echo "|   Install openzwave in tmp                               |"
echo "------------------------------------------------------------"
python setup-lib.py install --root=build/tmp
python setup-api.py install --root=build/tmp

cd docs
rm -Rf _build
echo "-----------------------------------------------------------------"
echo "|   Generate txt docs                                           |"
echo "-----------------------------------------------------------------"
make text
cp _build/text/README.txt ../README
cp _build/text/INSTALL_REPO.txt ../INSTALL_REPO
cp _build/text/INSTALL_MAN.txt ../INSTALL_MAN
cp _build/text/INSTALL_ARCH.txt ../INSTALL_ARCH
cp _build/text/COPYRIGHT.txt ../COPYRIGHT
cp _build/text/DEVEL.txt ../DEVEL
cp _build/text/EXAMPLES.txt ../EXAMPLES

echo "-----------------------------------------------------------------"
echo "|   Generate html docs                                          |"
echo "-----------------------------------------------------------------"
make html

echo "-----------------------------------------------------------------"
echo "|   Generate joomla docs                                        |"
echo "-----------------------------------------------------------------"
make joomla
cd ..
