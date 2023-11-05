#!/usr/bin/env bash

set -ev

cp jugfile1.py jugfile.py
jug execute

cp jugfile2.py jugfile.py
jug execute

cp jugfile3.py jugfile.py
jug execute

cp jugfile4.py jugfile.py
jug execute

python plot-results.py
