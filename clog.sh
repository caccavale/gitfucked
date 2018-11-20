#!/bin/bash
# Please think of a cleverer solution.
TMPDIR=`mktemp -d`
pushd $TMPDIR
git clone "$1" &>/dev/null
cloc *
popd
rm -rf $TMPDIR
