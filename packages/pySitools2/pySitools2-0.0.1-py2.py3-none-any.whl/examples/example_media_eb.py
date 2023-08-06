#! /usr/bin/env python
"""

@author: Pablo ALINGERY
"""


import sitools2.clients.sdo_client_medoc as md

d1 = md.datetime(2010,5,1,0,0,0)

d2 = d1 + md.timedelta(days=7*365)

l = md.media_search(dates=[d1,d2], series='hmi.m_720s', cadence=['1d'],nb_res_max=2 )

l[0].get_file()
