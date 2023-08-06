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
from sitools2.clients.sdo_client_medoc import media_search, \
	media_metadata_search, media_get
from datetime import datetime, timedelta

class TestMedia(unittest.TestCase):        
    
    def setUp(self):
        pass

    def testSearchMedia(self):
        print ("####Test media_search #############################")
        d1 = datetime(2012,8,10,0,0,0)
        d2 = d1 + timedelta(days=1)
        sdo_data_list = media_search( DATES=[d1,d2], WAVES=['335','304'], 
        	CADENCE=['10 min'] )
        self.assertEqual( len(sdo_data_list), 288)                            

if __name__ == "__main__":
    unittest.main()
