#!/bin/bash

CHANGED_MDS=$(git diff HEAD^ HEAD --name-only *.md)
sed -i "s/Modified:.*/Modified: $(date +'%F %H:%I')/" $CHANGED_MDS
