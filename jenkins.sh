#!/bin/bash
python2.6 bootstrap.py
./bin/buildout
./bin/test -s collective.archiveviewer
