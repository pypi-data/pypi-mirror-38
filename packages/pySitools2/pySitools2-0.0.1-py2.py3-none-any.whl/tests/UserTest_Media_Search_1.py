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

__author__="Eric Buchlin, Pablo ALINGERY"
__date__ ="$8 mars 2017 10:22:22$"

import unittest
import sitools2.clients.sdo_client_medoc as md 

class UserTest_Media_Search_1(unittest.TestCase):        
    
    def setUp(self):
        pass

    def testUserMediaSearch(self):
        print ("####User Test media_search & metadata_search #############################")
        l = md.media_search(dates=[md.datetime(2016,1,1,0,0,0), 
        	md.datetime(2016,1,1,1,0,0)], waves=['193'])
        rnlist = [str (a.recnum) for a in l]
        m=md.media_metadata_search(keywords=['date__obs', 'quality'], 
        	recnum_list=rnlist, series='aia.lev1')
        print (m[0:3])
        self.assertEqual( len(m), 60)                            

if __name__ == "__main__":
    unittest.main()
