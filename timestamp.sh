#!/bin/bash

CHANGED_MDS=$(git diff HEAD^ HEAD --name-only *.md)
sed -i "s/Modified:.*/Modified: $(TZ="EST" date +'%F %H:%I EST')/" $CHANGED_MDS
