#!/bin/bash

CHANGED_MDS=$(git diff --name-only *.md)
sed -i "s/Modified:.*/Modified: $(date +'%F %H:%I')/" $CHANGED_MDS
