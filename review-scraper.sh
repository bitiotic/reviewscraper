#!/bin/sh
#
# review-scraper.sh
#
# Wrapper for running under review-scraper's main.py
#


DIR=$(dirname $0)
PYTHON=python2.7

exec $PYTHON "${DIR}/main.py" "$@"

#eof
