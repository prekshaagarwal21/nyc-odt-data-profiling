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
import shutil
import requests

# Check today's date and create a directory file structure for today's date.
today = datetime.date.today()  
todaystr = today.isoformat()   

def create_date_dir():
    i = 0
    d = todaystr
    if not os.path.exists(d):
        os.mkdir(d)
    else:
        shutil.rmtree(d)
        os.mkdir(d)
        
create_date_dir()

# This will point to where the job is being run from NOT the directory where this file lives (mnt/notebooks/scratch), when run as a Domino Job 
current_dir = os.getcwd()
    
## Read in service account credentials - link to whichever json file holds your credentials
gc = gspread.service_account(filename='/mnt/data/odt-data-profiler-069defc7abf3.json')

## Spreadsheet key of your destination 
sh = gc.open_by_key('1gtMHAQkfufSOPb3hpThM_aZ0rwV8NG-CeVh3BY2dorQ')

# Read data from worksheet
worksheet = sh.get_worksheet(0)
list_of_lists = worksheet.get_all_records()


# Function to profile each dataset
def profile_data(list_of_lists):
    for i in range (0,len(list_of_lists)):
        agency_name = list_of_lists[i]['agency']
        dataset_name = list_of_lists[i]['dataset']
        url = list_of_lists[i]['4x4']
        dataset_url = f'https://data.cityofnewyork.us/resource/{url}.json'
        chunk_size = 100000
        offset = 0
        reached_end_of_dataset = False
        tmp_dfs = []
        while not reached_end_of_dataset:
            chunk_url = f'{dataset_url}?$limit={chunk_size}&$offset={offset}'
            tmp_r = requests.get(chunk_url, auth=("8febnpgtxedbep4no9oqegrce","36g68l45jhsdzeu08j3i44j4nxn2t65ua1gw4o0xwa9o17ownv"), timeout=None) #pd.read_json(chunk_url)
            tmp = pd.DataFrame(tmp_r.json())
            tmp_dfs.append(tmp)
    
            if tmp.shape[0] == chunk_size:
                offset += chunk_size
        
            else: # if got the last chunk, should be smaller than the chunk size 
                reached_end_of_dataset = True

        out_df = pd.concat(tmp_dfs, axis=0)
        #r = requests.get(dataset_url+f"?$limit=500000", auth=("8febnpgtxedbep4no9oqegrce","36g68l45jhsdzeu08j3i44j4nxn2t65ua1gw4o0xwa9o17ownv"), timeout=None)
        prl = ProfileReport(out_df, title=f"{dataset_name}_Data_Profiler", html={"style": {"full_width": True}}, sort=None,
            correlations=None,
            interactions=None,
            missing_diagrams={
                "bar": False,
                "matrix": True,
                "heatmap": False,
                "dendrogram": False,
            })
        out = prl.to_file(current_dir + "/" + todaystr + "/" + f"{todaystr}_{agency_name}_{dataset_name}.html")
        #with open(Path(current_dir, todaystr, f'{agency_name}_{dataset_name}.html'), 'w') as outpath:
        #    outpath.write(prl)
        #prl.to_html(current_dir + "/" + "test.html")

# Run function
profile_data(list_of_lists)