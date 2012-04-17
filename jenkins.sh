#!/bin/bash
python2.6 bootstrap.py -d
./bin/buildout
./bin/test -s collective.archiveviewer
