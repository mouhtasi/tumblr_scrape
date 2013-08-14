#!/bin/bash

DIRS=`ls -l images | egrep '^d' | awk '{print $9}'`

for DIR in $DIRS
	do
		python tumblr_scrape.py ${DIR} $1
	done
