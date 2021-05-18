#! /bin/bash
source /root/resultsNotifier/env/bin/activate
echo env activated!

# virtualenv is now active.
#
python3 /root/resultsNotifier/resultChecker.py
