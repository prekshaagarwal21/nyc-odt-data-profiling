#!/bin/sh
set -x

sudo pip install pandas_profiling
sudo pip install gspread
sudo pip install pdfkit
sudo pip install streamlit
sudo pip install streamlit_pandas_profiling

python data_profiler.py