#!/bin/sh
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
find . -name '.DS_Store' -type f -ls -delete
mkdir -p bp bp/jetson_utils bp/qtWidgets bp/csicam_utils
cp *.py *.sh bp/
cp qtWidgets/*.py bp/qtWidgets/
cp jetson_utils/*.py bp/jetson_utils/
cp csicam_utils/* bp/csicam_utils/
