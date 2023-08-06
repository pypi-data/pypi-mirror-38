#! /usr/bin/env python
"""

@author: Pablo ALINGERY 
"""

from sitools2.clients.sdo_client_medoc import media_search, media_metadata_search, media_get
from datetime import datetime, timedelta

d1 = datetime(2016, 1, 1, 0, 0, 0)
d2 = datetime(2016, 1, 1, 5, 12, 0)
#d2 = d1 + timedelta(minutes=5)

sdo_hmi_data_list = media_search(
    DATES=[d1, d2],
    series='hmi.sharp_cea_720s_nrt',
    cadence=['1h'],
    nb_res_max=10)
for data in sdo_hmi_data_list:
    print(data)

    ##sdo_data_list = media_search( DATES=[d1,d2], WAVES=['335','193'], CADENCE=['12 s'], nb_res_max=2 ) 
    #recnum_list=[]
    #for result in sdo_data_list :
    #	print result.sunum ,result.recnum, result.date_obs  
    #	recnum_list.append(result.recnum)

    #Test media_metada_search
    #print "Exemple media_metadata_search()"
    #my_meta_search=media_metadata_search(KEYWORDS=['date__obs','quality','cdelt1','cdelt2','crval1', 'sunum', 'recnum'], recnum_list=recnum_list)
    #i=0
    #for result in my_meta_search :
    #	print i+1,")",result,"\n"
    #	i+= 1

    #print my_meta_search
    #To limit the results sent by the server set nb_res_max
    #sdo_data_list = search( DATES=[d1,d2], WAVES=['335','304'], nb_res_max= 5 ,CADENCE=['1 min'] ) 

    #The fastest way to retrieve data
    #PS : The directory 'results' will be created if it does not exist
    for data in sdo_hmi_data_list:
        data.get_file(target_dir='results', SEGMENT=['Br'])

#Need to get a tar ball or zip file :
#A bit slower than the previous one
#media_get (MEDIA_DATA_LIST=sdo_data_list,DOWNLOAD_TYPE="tar", target_dir="results" ,FILENAME="my_download_file.tar")

#And if you want to specifies files name do sthg like 
#for item in sdo_data_list :
#	print item.date_obs, item.wave , item.recnum, item.sunum, item.ias_location
#	file_date_obs = item.date_obs.strftime('%Y-%m-%dT%H-%M-%S')
#	file_wave = item.wave
#	item.get_file( DECOMPRESS=False, FILENAME="toto_%s_%s.fits" %(file_date_obs,file_wave) , TARGET_DIR='results', QUIET=False )

#Search meta data info
#for item in sdo_data_list:
#	print item.date_obs
#	my_meta_search = item.metadata_search(KEYWORDS=['date__obs','quality','cdelt1','cdelt2','crval1'])
#	print my_meta_search
#	if (my_meta_search['quality'] == 0) :
#		#item.display()
#	         item.get_file(TARGET_DIR='results')	
