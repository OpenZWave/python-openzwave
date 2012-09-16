#!/bin/bash -e

echo $PYLIBRARY
#The release number of python-openzwave
RY023="cc56d65fbff4"
#The release number of openzwave
RZ023="539"

PYLIBRARY=$(grep "PYLIBRARY = " lib/libopenzwave.pyx  | sed -e "s|PYLIBRARY = ||"  | sed -e "s|\"||g")
ARCHIVEDIR=python-openzwave-${PYLIBRARY}
ARCHIVE=python-openzwave-${PYLIBRARY}.tgz

echo "-----------------------------------------------------------------"
echo "|   Clean build directory                                       |"
echo "-----------------------------------------------------------------"
[ -d build/$ARCHIVEDIR ] && rm -Rf build/$ARCHIVEDIR

echo "-----------------------------------------------------------------"
echo "|   Make python-openzwave archive                               |"
echo "-----------------------------------------------------------------"
hg archive \
    -p ${ARCHIVEDIR} \
    -r ${RY023} \
    -I . \
    -X make_archive.sh \
    -X make_distdir.sh \
    -X .hg_archival.txt  \
    -X .coverage  \
    -X .hgignore  \
    -X docs/_build/ \
    -X old/ \
    -t tgz ${ARCHIVE}
if [ $? -ne 0 ] ; then
	echo "Error : can't create archive python-openzwave ... exiting"
	exit 1
fi

echo "-----------------------------------------------------------------"
echo "|   Extract it to ${ARCHIVEDIR}                                   |"
echo "-----------------------------------------------------------------"
[ ! -d build ] && mkdir build
cd build
tar xvzf ../${ARCHIVE}
echo "OPZW=r${RZ023}" >${ARCHIVEDIR}/VERSIONS
echo "PYOZW=${PYLIBRARY}" >>${ARCHIVEDIR}/VERSIONS
cd ..

echo "-----------------------------------------------------------------"
echo "|   Checkout openwave repository                                |"
echo "-----------------------------------------------------------------"
svn checkout http://open-zwave.googlecode.com/svn/trunk/ openzwave
svn export -r ${RZ023} openzwave build/${ARCHIVEDIR}/openzwave

echo "-----------------------------------------------------------------"
echo "|   Compress to $ARCHIVE                                        |"
echo "-----------------------------------------------------------------"
cd build
tar cvzf ../${ARCHIVE} ${ARCHIVEDIR}

echo "Package successfully created : ${ARCHIVE}"

