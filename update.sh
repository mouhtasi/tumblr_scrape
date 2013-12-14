#!/bin/bash

scriptPath="$(readlink -f $0)"
cd "${scriptPath%/*}"

PAGES=$1
if [ "$(($1+0))" -le 0 ]; then PAGES=1; fi

for DIR in images/*; do
	if [ -d "${DIR}" ]; then
		python2 tumblr_scrape.py "${DIR##*/}" "$PAGES"
	fi
done
