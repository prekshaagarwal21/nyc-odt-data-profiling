#!/bin/sh
set -x

sudo pip install pandas_profiling
sudo pip install gspread

python data_profiler.py