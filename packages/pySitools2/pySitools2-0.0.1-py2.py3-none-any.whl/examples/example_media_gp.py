#! /usr/bin/env python
"""

@author: Pablo ALINGERY
"""

from sitools2.clients.sdo_client_medoc import media_search, \
    media_metadata_search, media_get
from datetime import datetime, timedelta


d1 = datetime(2016, 6, 1, 5, 0, 0)
d2 = datetime(2016, 6, 1, 10, 12, 0)
#d2 = d1 + timedelta(minutes=5)

#sdo_data_list = media_search(
#   DATES=[d1,d2],
#   WAVES=['335'],
#   CADENCE=['12s'],
#   nb_res_max=10,
#   server='http://medoc-sdo.ias.u-psud.fr')

sdo_data_list = media_search(
    DATES=[d1, d2],
    WAVES=['335', '304'],
    CADENCE=['1m'],
    nb_res_max=10,
    server='http://idoc-medoc-test.ias.u-psud.fr')


#And if you want to specifies files name do sthg like
for item in sdo_data_list :
	print item.date_obs, item.wave , item.recnum, item.sunum, item.ias_location
	file_date_obs=item.date_obs.strftime('%Y-%m-%dT%H-%M-%S')
	file_wave=item.wave
	item.get_file(
       DECOMPRESS=False,
       FILENAME="toto_%s_%s.fits" %(file_date_obs,file_wave),
       TARGET_DIR='results'
   )

