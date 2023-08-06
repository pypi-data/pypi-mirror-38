#! /usr/bin/python
"""

@author: Pablo ALINGERY for IAS 06-05-2016
"""

from sitools2.core.pySitools2 import *


def main():
    sitools_url = 'http://idoc-medoc-test.ias.u-psud.fr'
    #       sitools_url = 'http://localhost:8184'

    SItools1 = Sitools2Instance(sitools_url)
    prj_list = SItools1.list_project()
    print("Nombre de projets : ", len(prj_list))
    #       ds_list=[]

    #       for p in prj_list :
    #               p.display()
    #               for ds in p.dataset_list() :
    #                       print p.name
    #                       ds_list.append(ds)

    #       if len(ds_list)!=0 :
    #               print "%d dataset(s) found :" % len(ds_list)
    #               for i,dataset in enumerate(ds_list) :
    #                       print "%d) %s" % (i, dataset.name)

    p1 = prj_list[0]
    print(p1)
    print("\nTarget project :\n\t", p1.name)
    ds_list = p1.dataset_list()
    if len(ds_list) != 0:
        print("%d dataset(s) found :" % len(ds_list))
        for i, dataset in enumerate(ds_list):
            print("%d) %s %s" % (i, dataset.name, dataset.url))

    ds1_url = sitools_url + "/webs_aia_dataset?media=json"

    print(ds1_url)

    try:
        result = simplejson.load(urllib.urlopen(ds1_url))
        name = result['dataset']['name']
        description = result['dataset']['description']
        status = result['dataset']['status']

    except:
        print("Load json info failed")
    else:
        print("Load json info ok")
        print(name, status)

    print("Loading SitoolsClient for", sitools_url)
    SItools1 = Sitools2Instance(sitools_url)
    ds1 = Dataset(sitools_url + "/webs_IAS_SDO_HMI_dataset")
    #        ds1 = Dataset(sitools_url+"/webs_IAS_SDO_AIA_dataset")

    ds1.display()
    #display() or print works as well
    #        print ds1

    #date__ob
    #Format must be somthing like 2015-11-01T00:00:00.000 in version Sitools2 3.0 that will change 
    param_query1 = [[ds1.fields_dict['date__obs']],
                    ['2015-11-01T00:00:00.000', '2015-11-02T00:00:00.000'],
                    'DATE_BETWEEN']
    #series_name 
    param_query2 = [[ds1.fields_dict['series_name']],
                    ['hmi.sharp_cea_720s_nrt'], 'IN']
    #       param_query2=[[ds1.fields_dict['series_name']],['aia.lev1'],'IN']
    #cadence
    param_query3 = [[ds1.fields_dict['mask_cadence']], ['2 h'], 'CADENCE']

    Q1 = Query(param_query1)
    Q2 = Query(param_query2)
    Q3 = Query(param_query3)

    #Ask recnum, sunum,series_name,date__obs, ias_location, harpnum,ias_path

    O1 = [
        ds1.fields_dict['recnum'], ds1.fields_dict['sunum'],
        ds1.fields_dict['series_name'], ds1.fields_dict['date__obs'],
        ds1.fields_dict['ias_location'], ds1.fields_dict['harpnum'],
        ds1.fields_dict['ias_path']
    ]
    #       O1 = [ds1.fields_dict['recnum'],ds1.fields_dict['sunum'],ds1.fields_dict['series_name'],ds1.fields_dict['date__obs'],ds1.fields_dict['ias_location'],ds1.fields_dict['ias_path']]

    #Sort date__obs ASC
    S1 = [[ds1.fields_dict['date__obs'], 'ASC']]

    #       for field in ds1.fields_list :
    #               field.display()

    #        print "\nPrint Query  ..."
    #        Q1.display()
    #        Q2.display()
    #       Q3.display()

    result = ds1.search([Q1, Q2, Q3], O1, S1)
    #        result=ds1.search([Q1,Q2],O1,S1,limit_to_nb_res_max=10)
    if len(result) != 0:
        print("Results :")
        for i, data in enumerate(result):
            print("%d) %s" % (i + 1, data))

    recnum_list = []
    for record in result:
        recnum_list.append(str(record['recnum']))

    ds_hmi = Dataset(sitools_url + "/webs_hmi.sharp_cea_720s_nrt_dataset")
    ds_hmi.display()
    #        print recnum_list
    #recnum
    param_query_hmi = [[ds_hmi.fields_list[0]], recnum_list, 'IN']
    Q_hmi = Query(param_query_hmi)
    #        Q_hmi.display()
    #output 
    O1_hmi = [
        ds_hmi.fields_dict['recnum'], ds_hmi.fields_dict['sunum'],
        ds_hmi.fields_dict['lat_max']
    ]
    S1_hmi = [[ds_hmi.fields_dict['recnum'], 'ASC']]
    #       for field in ds_aia.fields_list :
    #               field.display()
    result_hmi = ds_hmi.search([Q_hmi], O1_hmi, S1_hmi)
    for data in result_hmi:
        print(data)


#       print "Download just one recnum\nIn progress please wait ..." 
#       ds1.execute_plugin(plugin_name='pluginDownloadTar', pkey_list=["1878160,hmi.sharp_cea_720s_nrt"], FILENAME='first_download_hmi.tar')
#       print "Download completed"

#Unit test get_file
#       for data in result_hmi :
#       for data in sdo_hmi_data_list :
#data.get_file(target_dir='results')

if __name__ == "__main__":
    main()
