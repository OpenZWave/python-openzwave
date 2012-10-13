#!/bin/bash -e

echo $PYLIBRARY
#Archive history
RY023="cc56d65fbff4"
RZ023="539"

#Last archive
#The release number of python-openzwave
RY024="50a9d95db236"
#The release number of openzwave
RZ024="540"

#Current archive
RY=$(echo $RY024)
RZ=$(echo $RZ024)

#Define variables
PYLIBRARY=$(grep "PYLIBRARY = " lib/libopenzwave.pyx | sed -e "s|PYLIBRARY = ||" | sed "s/\x0D$//" | sed -e "s|^M$||" | sed -e "s|\"||g")
ARCHIVEDIR=python-openzwave-${PYLIBRARY}
ARCHIVE=python-openzwave-${PYLIBRARY}.tgz

echo "-----------------------------------------------------------------"
echo "|   Clean build directory                                       |"
echo "-----------------------------------------------------------------"
[ -d build/$ARCHIVEDIR ] && rm -Rf build/$ARCHIVEDIR

echo "-----------------------------------------------------------------"
echo "|   Make root documentation                                     |"
echo "-----------------------------------------------------------------"
./make_docs.sh

echo "-----------------------------------------------------------------"
echo "|   Make python-openzwave archive                               |"
echo "-----------------------------------------------------------------"
hg archive \
    -p ${ARCHIVEDIR} \
    -r ${RY} \
    -I . \
    -X make_archive.sh \
    -X make_distdir.sh \
    -X make_docs.sh \
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
echo "OPZW=r${RZ}" >${ARCHIVEDIR}/VERSIONS
echo "PYOZW=${PYLIBRARY}" >>${ARCHIVEDIR}/VERSIONS
cd ..

echo "-----------------------------------------------------------------"
echo "|   Checkout openwave repository                                |"
echo "-----------------------------------------------------------------"
if [ -d openzwave ] ; then
    echo "Update openzwave directory"
    svn update http://open-zwave.googlecode.com/svn/trunk/ openzwave
else
    echo "Checkout openzwave directory"
    svn checkout http://open-zwave.googlecode.com/svn/trunk/ openzwave
fi
svn export -r ${RZ} openzwave build/${ARCHIVEDIR}/openzwave

echo "-----------------------------------------------------------------"
echo "|   Compress to $ARCHIVE                                        |"
echo "-----------------------------------------------------------------"
cd build
tar cvzf ../${ARCHIVE} ${ARCHIVEDIR}

echo "Package successfully created : ${ARCHIVE}"

