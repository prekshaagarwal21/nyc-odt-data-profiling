import pandas as pd
import pandas_profiling
from pandas_profiling import ProfileReport

import numpy as np
import string
from google.oauth2 import service_account
import gspread

from pathlib import Path
import os 

import time, datetime, os
#import re 
import shutil 
#import pdfkit as pdf
#from IPython.core.display import display, HTML

import streamlit as st

from streamlit_pandas_profiling import st_profile_report


# Check today's date and create a directory file structure for today's date.
today = datetime.date.today()  
todaystr = today.isoformat()   

def create_date_dir():
    i = 0
    d = todaystr
    if not os.path.exists(d):
        os.mkdir(d)
    else:
        '''#if os.path.exists(d):
        #    i += 1
        #    d = d[:10] + '_' + str(i).zfill(2)
        #os.mkdir(d)
        #else:
        #    m = re.findall(r'\w\w$', d)
        #    i = float(m[0:]) + 1
        #    d = d[:10] + '_' + str(i).zfill(2)
        #os.mkdir(d)'''
        shutil.rmtree(d)
        #os.rmdir(d)
        os.mkdir(d)
        
create_date_dir()

# This will point to where the job is being run from NOT the directory where this file lives (mnt/notebooks/scratch), when run as a Domino Job 
current_dir = os.getcwd()
    
## Read in service account credentials - link to whichever json file holds your credentials
gc = gspread.service_account(filename='/mnt/data/odt-data-profiler-069defc7abf3.json')

## Spreadsheet key of your destination 
sh2 = gc.open_by_key('1gtMHAQkfufSOPb3hpThM_aZ0rwV8NG-CeVh3BY2dorQ')

# Read data from worksheet
worksheet2 = sh2.get_worksheet(0)
list_of_lists = worksheet2.get_all_records()


# Profile each dataset
def profile_data(list_of_lists, todaystr):
    for i in range (0,len(list_of_lists)):
        #today = datetime.date.today()  
        #todaystr = today.isoformat()
        agency_name = list_of_lists[i]['agency']
        dataset_name = list_of_lists[i]['dataset']
        dataset_url = list_of_lists[i]['url']
        df = pd.read_json(dataset_url)
        prl = ProfileReport(df, title=f"{dataset_name}_Data_Profiler", html={"style": {"full_width": True}}, sort=None)
        #st.title(f"{dataset_name} in Streamlit!")
        #st.write(df)
        #st_profile_report(prl)
        #out = "Hello"
        #with open(Path(current_dir, todaystr, f'{dataset_name}.html'), 'w+') as outpath:
        #    outpath.write(out)
        out = prl.to_file(f"{todaystr}_{agency_name}_{dataset_name}.html")
        #out = prl.to_file("/mnt/nyc-odt-data-profiling/f"{todaystr}_{agency_name}_{dataset_name}.html"")
        #with open(Path(current_dir, todaystr, f'{agency_name}_{dataset_name}.html'), 'w') as outpath:
        #    outpath.write(prl)
        #prl.to_html(current_dir + "/" + "test.html")
        #prl.to_html("test.html")
        #pdf.from_file('test.html', 'test.pdf')
        #report_html = prl._render_html()
        #display(HTML(report_html))
# Run function
#out = profile_data(list_of_lists)

profile_data(list_of_lists, todaystr)