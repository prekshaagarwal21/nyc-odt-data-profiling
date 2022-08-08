# # About this project: nyc-odt-data-profiling
Data Profiling Tool for NYC's Open Data Team at the Office of Data Analytics

## Who owns the project? 
This project is owned by the Open Data Team at ODA. The early development work for this project was done by Preksha Agarwal during her summer internship in summer 2022. For questions on this project, please reach out to Zachary Feder or Ryan Zirngibl.

## When was the project created and when has major work on it occurred?
This project was created in July 2022. 

## What is this project?
This project exists to help the Open Data Team with the data quality review process for new and existing datasets on the Open Data portal. This data profiler uses the Google API to read from an internal google sheet updated regularly by the Open Data team, to profile the datasets listed on the google sheet and generate interactive html reports summarizing the key data elements, missing values, data duplication, top values, etc. This job is run daily to support the open data team's data quality review needs. 

## Why was this project created? 
Currently the Open Data team relies on a lot of manual review work by the team members. Each team member checks against a list of standards for the data quality, but the process by which they flag something might be completely different for each team member. Additionally, initial review for new datasets can take a lot of time even though we apply the same standards and checks for each dataset. This project was started to simplify, speed up, and further standardize the data quality review process.

## Who is this project for? 
The end consumer of this project is the ODA open data team, who should use it as a basis for their data quality review (QAQC) moving forward.


# Running the project
This project is scheduled to run once daily inside the Domino environment at ODA. If you need an additional manual run, please contact Ryan Zirngibl.  

## Environmental variables 
N/A

## Inputs and Data 
The input to this project is the Data Profiling Worksheet, updated and maintained regularly by the Open Data team. 

## Outputs 
Outputs from this project are sent to everyone on the email list for the scheduled job as a Domino notification email daily after the scheduled job completes.

## Scheduling 
This job is scheduled to run in the Domino environment. The scheduled job title is "data profiler" and it runs the /repos/nyc-odt-data-profiling/profiler.sh' script everyday at 12:30PM EST. It is set up to run sequentially on the largest hardware tier (6 cores, 16 GiB RAM). The following emails are notified when this scheduled job completes:

AWebber@oti.nyc.gov,kotorres@oti.nyc.gov,huizhang@oti.nyc.gov,aeng@oti.nyc.gov,ZFeder@oti.nyc.gov,henwu@oti.nyc.gov,afinkel@oti.nyc.gov,OHyacinthe@oti.nyc.gov,arholder@oti.nyc.gov,pragarwal@oti.nyc.gov

## External requirements 
To be notified by Domino with the output files, you do not need any access to Domino, Socrata or GCP APIs. However, to be able to edit the Google spreadhseet that is the input data to this project, users need to have edit access to the Data Profiling Worksheet and access to any datasets (private) that they want to profile. 

