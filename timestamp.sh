#!/bin/bash

CHANGED_MDS=$(git diff --name-only | grep *.md)
echo $CHANGED_MDS
sed -i "s/Modified:.*/Modified: $(date +'%F %H:%I')/" $CHANGED_MDS
