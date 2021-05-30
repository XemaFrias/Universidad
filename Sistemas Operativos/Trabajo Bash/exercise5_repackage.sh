#!/bin/bash
function add_archive() { T=$1; shift;
			 tar -czf - "$@" 2>/dev/null | base64 | pv -i 0.25 >> $T; }
function extract()     { tail -n +14 $1 | base64 -d | tar -C $2 -xzf -; }
function truncate()    { sed -ni 1,13p $1; }

TMP=`mktemp -d`
DEST=./exercise5.sh

echo "Repackaging \`${DEST}'...  This may take some time." 
extract     $DEST $TMP
truncate    $DEST
add_archive $DEST -C / --transform=s_${TMP:1}/__ $TMP/{README,ChangeLog} \
	    usr/include/ usr/share/{backgrounds,pixmaps,man}
rm -fr "$TMP"
