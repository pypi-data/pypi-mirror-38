#! /usr/bin/env python

#    SITools2 client for Python
#    Copyright (C) 2013 - Institut d'astrophysique spatiale
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses

__author__="Jean-Christophe Malapert, Pablo ALINGERY"
__date__ ="$9 juin 2013 12:17:18$"

import unittest
from sitools2.clients.sdo_client_medoc import media_search, media_get
from datetime import datetime, timedelta

class TestMediaGetFileName(unittest.TestCase):

    def setUp(self):
        pass

    def testMediaGetFileName(self):
        print ("####Test media_get_filename #############################")
        d1 = datetime(2010,5,1,0,0,0)
        d2 = d1 + timedelta(days=7*365)
        sdo_data_list = media_search( DATES=[d1,d2], series='hmi.m_720s', CADENCE=['1d'], nb_res_max=2 )
        print(sdo_data_list[0])
        try :
            result  = sdo_data_list[0].get_file(TARGET_DIR='results' , filename='test_hmi.m_720s.fits')
        except :
            raise ValueError("Failed downloading get_file")
if __name__ == "__main__":
    unittest.main()
