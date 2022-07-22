#!/bin/sh -e
set -x

#sudo pip install pandas_profiling==3.1.0
#sudo pip install gspread
#sudo pip install pdfkit
#sudo pip install streamlit
#sudo pip install streamlit_pandas_profiling
#sudo pip install cairosvg

python data_profiler.py

#mv /repos/nyc-odt-data-profiling/*.html /mnt/.

#echo "      date     time $(free -m | grep total | sed -E 's/^    (.*)/\1/g')"
#while true; do
#    echo "$(date '+%Y-%m-%d %H:%M:%S') $(free -m | grep Mem: | sed 's/Mem://g')"
#    sleep 1
#done