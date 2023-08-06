#! /usr/bin/python
"""

@author: Pablo ALINGERY for IAS 06-05-2016
"""

from sitools2.core.pySitools2 import *


import unittest
from sitools2.clients.sdo_client_medoc import *

class TestIdocMedocDsNbr(unittest.TestCase):        
    
    def setUp(self):
        pass

    def testNbrDsIdocMedoc(self):
        print ("####Test idoc-medoc NbrDatasets #############################")
        sitools_url = 'http://idoc-medoc-test.ias.u-psud.fr'

        SItools1 = Sitools2Instance(sitools_url)
        prj_list = SItools1.list_project()
        print("Nombre de projets : ", len(prj_list))

        p1 = prj_list[0]
        print(p1)
        ds_list = p1.dataset_list()
        print ("Nbr datasets : %s" % len(ds_list))
        self.assertEqual( len(ds_list), 75)
if __name__ == "__main__":
    unittest.main()
