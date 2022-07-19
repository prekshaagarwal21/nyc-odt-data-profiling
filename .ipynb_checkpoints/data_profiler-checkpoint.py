import pandas as pd
import pandas_profiling
from pandas_profiling import ProfileReport

import numpy as np
import string
from google.oauth2 import service_account
import gspread

from pathlib import Path
import os 

# This will point to mnt/ NOT the directory where this file lives (mnt/notebooks/scratch), when run as a Domino Job 
current_dir = os.getcwd()

## Read in service account credentials - link to whichever json file holds your credentials
gc = gspread.service_account(filename='/mnt/data/odt-data-profiler-069defc7abf3.json')

## Spreadsheet key of your destination 
sh2 = gc.open_by_key('1gtMHAQkfufSOPb3hpThM_aZ0rwV8NG-CeVh3BY2dorQ')

# Read data from worksheet
worksheet2 = sh2.get_worksheet(0)
list_of_lists = worksheet2.get_all_records()

# Profile each dataset
def profile_data(list_of_lists):
    for i in range (0,len(list_of_lists)):
        dataset_name = list_of_lists[i]['dataset']
        dataset_url = list_of_lists[i]['url']
        df = pd.read_json(dataset_url)
        prl = ProfileReport(df, title=f"{dataset_name}_Data_Profiler", html={"style": {"full_width": True}}, sort=None)
        prl.to_file(f"testing_{dataset_name}.html")
        #prl.to_file(f"testing_{dataset_name}.html")
    
# Run function
out = profile_data(list_of_lists)

with open(Path(current_dir, 'notebooks', 'scratch', 'outputs', f'{out}.html'), 'w') as outpath:
    outpath.write(out)
    
