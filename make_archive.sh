#!/bin/bash -e

PYLIBRARY=$(grep "PYLIBRARY = " lib/libopenzwave.pyx  | sed -e "s|PYLIBRARY = ||"  | sed -e "s|\"||g")
echo "-----------------------------------------------------------------"
echo "|   Make archive                                                |"
echo "-----------------------------------------------------------------"

echo $PYLIBRARY
R023="cc56d65fbff4"
ARCHIVE=python-openzwave-$PYLIBRARY.tgz

hg archive \
    -p python-openzwave-$PYLIBRARY \
    -r $R023 \
    -I . \
    -X make_archive.*.sh \
    -X make_docs.*.sh \
    -X .hg_archival.txt  \
    -X .coverage  \
    -X .hgignore  \
    -X docs/_build/ \
    -X old/ \
    -t tgz $ARCHIVE
if [ $? -ne 0 ] ; then
	echo "Error... exiting"
	exit 1
fi
echo "Package successfully created : $ARCHIVE"

