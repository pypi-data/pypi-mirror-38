#! /usr/bin/env python
"""

@author: Pablo ALINGERY for IAS 28-08-2012
"""
from sitools2.clients.gaia_client_medoc import gaia_search, gaia_get
from datetime import datetime, timedelta

d1 = datetime(2012, 8, 10, 0, 0, 0)
d2 = d1 + timedelta(days=1)

gaia_data_list = gaia_search(DATES=[d1, d2], nb_res_max=10)
for item in gaia_data_list:
    print(item)

#the fastest way to retrieve data
gaia_get(gaia_list=gaia_data_list, target_dir="results")

#Need to get a tar ball do sthg like :
#gaia_get(GAIA_LIST=gaia_data_list,DOWNLOAD_TYPE="tar", target_dir="results" ,FILENAME="my_dowload_file.tar")

#Need to do it quietly 
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results",QUIET=True)

#specify TYPE you want to  retrieve , it should be in list 'temp','em','width','chi2' (TYPE=['all'] will do as well ), FILENAME would be the default one 
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", TYPE=['temp','em'])
#Warning TYPE will be ignored if you specify DOWNLOAD_TYPE

#To specify FILENAME you want to retrieve, Use get_file() method 
#FILENAME should be a dictionary with key within 'temp','em','width','chi2' and value can be whatever you want
#for item in gaia_data_list :
#	file_date_obs = (item.date_obs).strftime("%Y-%m-%dT%H:%M:%S")
#	item.get_file(TARGET_DIR="results", FILENAME = {'temp' :"temp_%s.fits" % file_date_obs, 'em':"em_%s.fits" % file_date_obs})

#########################Warning###########################
#specify both FILENAME and TYPE is not allowed 
#gaia_get(GAIA_LIST=gaia_data_list, TARGET_DIR="results", FILENAME={'temp' :'temp.fits','em':'em.fits'}, TYPE=['temp','em'])
###########################################################
