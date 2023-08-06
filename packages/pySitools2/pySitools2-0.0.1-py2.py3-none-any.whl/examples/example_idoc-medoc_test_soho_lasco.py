#! /usr/bin/python
"""

@author: Pablo ALINGERY for IAS 06-02-2017
"""

from sitools2.core.pySitools2 import *


def main():

    sitools_url = 'http://idoc-medoc-test.ias.u-psud.fr'

    print("Loading SitoolsClient for", sitools_url)
    SItools1 = Sitools2Instance(sitools_url)
    ds1 = Dataset(sitools_url + "/webs_SOHO_dataset")
    ds1.display()

    #date__ob
    #Format must be somthing like 2015-11-01T00:00:00.000 in version Sitools2 3.0 that will change 
    param_query1 = [
                     [ds1.fields_dict['date_obs']], 
                     ['2015-01-01T00:00:00.000', '2015-01-01T01:00:00.000'],
                     'DATE_BETWEEN'
    ]

    Q1 = Query(param_query1)
    #Q2 = Query(param_query2)
    #Q3 = Query(param_query3)

    #Ask recnum, sunum,series_name,date__obs, ias_location,ias_path

    O1 = [
        ds1.fields_dict['filename'], ds1.fields_dict['filesize'], 
        ds1.fields_dict['instrument'], ds1.fields_dict['date_obs'], 
        ds1.fields_dict['secchisata'], ds1.fields_dict['secchisatb'],
        ds1.fields_dict['wavemin'], ds1.fields_dict['wavemax'],
        ds1.fields_dict['datatype'],  ds1.fields_dict['download_path'],
         ds1.fields_dict['path'],  ds1.fields_dict['id_sitools_view']
    ]

    #Sort date__obs ASC
    S1 = [[ds1.fields_dict['date_obs'], 'ASC']]

    #       for field in ds1.fields_dict :
    #               field.display()

    #        print "\nPrint Query  ..."
    Q1.display()
    # Q2.display()
    # Q3.display()

    result = ds1.search([Q1], O1, S1)
    print(len(result), " item(s) found\n")
    # #        result=ds1.search([Q1,Q2],O1,S1,limit_to_nb_res_max=10)
    if len(result) != 0:
         print("Results :\n")
         for i, data in enumerate(result):
             print("%d) %s" % (i + 1, data))



    print ("Download just one SOHO data\nIn progress please wait ...") 
    print("item : \n%s" % result[1])
    print("id : %s" % result[1]['id_sitools_view'])
    # try :
    ds1.execute_plugin(plugin_name='pluginSOHOtar', pkey_list=[result[1]['id_sitools_view']], FILENAME='first_download_SOHO.tar')
    # except :
    #     print ("Issue downloading id_sitools_view : %s " % result[1]['id_sitools_view'])
    # else :
    #     print ("Download id_sitools_view : %s completed" % result[1]['id_sitools_view'] )

if __name__ == "__main__":
    main()
