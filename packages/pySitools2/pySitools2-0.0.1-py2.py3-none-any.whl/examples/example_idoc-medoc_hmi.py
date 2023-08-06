#! /usr/bin/env python
"""

@author: Pablo ALINGERY 
"""

from sitools2.clients.sdo_client_medoc import media_search, \
	media_metadata_search
from datetime import datetime

d1 = datetime(2016, 1, 1, 0, 0, 0)
d2 = datetime(2016, 6, 1, 0, 0, 0)

sdo_hmi_data_list = media_search(
    DATES=[d1, d2],
    SERIES='hmi.sharp_cea_720s_nrt',
    CADENCE=['1d'],
    nb_res_max=10)

print sdo_hmi_data_list
#Metadata info 
meta = media_metadata_search(
    KEYWORDS=['date__obs', 'quality', 'cdelt1', 'cdelt2', 'crval1'],
    SERIES='hmi.sharp_cea_720s_nrt',
    MEDIA_DATA_LIST=sdo_hmi_data_list)
print(meta)

#Download data 
for data in sdo_hmi_data_list:
    #data.get_file(target_dir='results', SEGMENT=['continuum'])
    data.get_file(target_dir='results')
