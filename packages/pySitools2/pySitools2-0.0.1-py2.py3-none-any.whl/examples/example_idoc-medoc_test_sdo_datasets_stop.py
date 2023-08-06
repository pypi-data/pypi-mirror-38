#! /usr/bin/python
"""

@author: Pablo ALINGERY for IAS 06-02-2017
"""

from sitools2.core.pySitools2 import *


def main():

    sitools_url = 'http://localhost:8182'

    print("Loading SitoolsClient for", sitools_url)
    SItools1 = Sitools2Instance(sitools_url)
    # prj_list = SItools1.list_project()
    # p1=prj_list[0]
    # ds_list = p1.dataset_list()
    # url_list=[]
    # # for ds in ds_list :
    # #     print ds.url

    # ds_url=ds_list[73].url
    # print ds_url
    request = Request("http://localhost:8182/sitools/datasets/829940c9-95a6-4538-b623-c7705989df25/start")
    print request
    request.get_method = lambda : 'POST'
    urlopen(request)
if __name__ == "__main__":
    main()
