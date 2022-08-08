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

## Check today's date and create a directory file structure for today's date.
today = datetime.date.today()  
todaystr = today.isoformat()   

def create_date_dir():
    i = 0
    d = todaystr
    if not os.path.exists(d): # if directory for today's date does not exist, create one.
        os.mkdir(d)
    else:
        shutil.rmtree(d)
        os.mkdir(d)
        
## call create_date_dir function to create the directory structure for today's date.        
create_date_dir()

## This will point to where the job is being run from NOT the directory where this file lives, when run as a Domino Job. 
## In this case the job is being run from the same directory (/repos/nyc-odt-data-profiling) where the file lives.
current_dir = os.getcwd()
    
## Read in service account credentials - link to json file that holds GCP credentials.
gc = gspread.service_account(filename='/mnt/data/odt-data-profiler-069defc7abf3.json')

## Spreadsheet key of your destination. This is the working input document used by the Open Data team. 
## (link here: https://docs.google.com/spreadsheets/d/1gtMHAQkfufSOPb3hpThM_aZ0rwV8NG-CeVh3BY2dorQ/edit#gid=0) 
sh = gc.open_by_key('1gtMHAQkfufSOPb3hpThM_aZ0rwV8NG-CeVh3BY2dorQ')

# Read data from "data to profile" tab of the worksheet. 
worksheet = sh.worksheet("data to profile")
list_of_lists = worksheet.get_all_records() ## this returns a list of lists containing key/value pairs for each field.


# Function to profile each dataset
def profile_data(list_of_lists):
    for i in range (0,len(list_of_lists)):
        agency_name = list_of_lists[i]['agency'] # agency field for each row - will be used in the report name
        dataset_name = list_of_lists[i]['dataset'] # dataset name for each row - will be used in the report name
        url = list_of_lists[i]['4x4'] # 4x4 for each row - will be used to identify the dataset and read in the data from the API endpoint
        dataset_url = f'https://data.cityofnewyork.us/resource/{url}.json' # defining the url using the 4x4 for each row
        chunk_size = 100000 # the chunk size is the limit that will be set for the get requests. Only 100000 rows are read at a given time. 
        offset = 0
        reached_end_of_dataset = False
        tmp_dfs = []
        while not reached_end_of_dataset:
            chunk_url = f'{dataset_url}?$limit={chunk_size}&$offset={offset}'
            tmp_r = requests.get(chunk_url, auth=("8febnpgtxedbep4no9oqegrce","36g68l45jhsdzeu08j3i44j4nxn2t65ua1gw4o0xwa9o17ownv"), timeout=None)
            tmp = pd.DataFrame(tmp_r.json())
            tmp_dfs.append(tmp)
    
            if tmp.shape[0] == chunk_size: # Offset and limit are used together to incrementally read 100000 rows at a time if we have not reached the end of the dataset. 
                offset += chunk_size
        
            else: # if got the last chunk, should be smaller than the chunk size 
                reached_end_of_dataset = True

        out_df = pd.concat(tmp_dfs, axis=0) # chunks of dataset are concatenated to get the full dataset. NOTE THAT THIS STEP FAILS FOR VERY LARGE DATASETS LARGER THAN ~ 10 MILLION ROWS.
        prl = ProfileReport(out_df, title=f"{dataset_name}_Data_Profiler", html={"style": {"full_width": True}}, sort=None,
            correlations=None,
            interactions=None,
            missing_diagrams={
                "bar": False,
                "matrix": True,
                "heatmap": False,
                "dendrogram": False,
            }) # using pandas_profiling to generate the report. Many features are configurable within this function. For now, we only turn off some of the extraneous information that we don't want to see.
        out = prl.to_file(current_dir + "/" + todaystr + "/" + f"{todaystr}_{agency_name}_{dataset_name}.html") # output the report to the appropriate directory.

# Run function
profile_data(list_of_lists) 