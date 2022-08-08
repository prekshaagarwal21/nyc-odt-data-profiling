#!/bin/sh -e
set -x

sudo pip install pandas_profiling==3.1.0 ## this is the version of pandas_profiling that does not result in errors with write to_html. 
sudo pip install gspread

python /repos/nyc-odt-data-profiling/data_profiler.py