#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
This script has been designed to give python programmers an easy way to
interrogate media sitools2 interface. You can make a search with the following
entries : a date range , a wavelenghth or multiple wavelengths , a cadence.
You will have as a result a list of Sdo_data objets on which you can apply the
method display() that will give you for each the recnum, the sunum, the
date_obs, the wavelength, the ias_location, the exptime and t_rec_index
For each result you will be able to call metadata_search() method in order to
have the metadata information.
@author: Pablo ALINGERY for IAS 28-08-2012
"""
__license__ = "GPLV3"
__author__ = "Pablo ALINGERY"
__credit__ = ["Pablo ALINGERY", "Elie SOUBRIE"]
__maintainer__ = "Pablo ALINGERY"
__email__ = "medoc-contact@ias.u-psud.fr"

from sitools2.core.pySitools2 import *
from sys import stdout, stderr
from os import path, mkdir
from collections import Counter
from future.utils import iteritems
from builtins import map
from future.moves.urllib.request import urlretrieve
from simplejson import load

#sitools2_url='http://medoc-sdo.ias.u-psud.fr'
#sitools2_url='http://medoc-sdo-test.ias.u-psud.fr'
sitools2_url = 'http://idoc-medoc-test.ias.u-psud.fr'

#sitools2_url='http://localhost:8182'


def media_get(media_data_list=[], target_dir=None, download_type=None, **kwds):
    """Donwload hmi and aia data from MEDOC server

    Parameters
    ----------
    media_data_list : list of Sdo_data objects
        The result of media_search can be passed as an argument of that
        function.
        The size of the list must be >0
    target_dir : str
        User can specify the directory of download
    download_type : str
        Can be 'TAR' or 'ZIP'

    Raise
    -----
    ValueError
        In case parameter media_data_list is empty

    Returns
    -------
    Files located in the target_dir directory

    Example
    -------
    >>> sdo_data_list = media_search(
                            dates=[d1,d2],
                            series='hmi.m_720s',
                            nb_res_max=10)
    >>> media_get(MEDIA_DATA_LIST=sdo_data_list)

    >>> media_get(MEDIA_DATA_LIST=sdo_data_list, target_dir='results')

    >>> media_get (media_data_list=sdo_data_list,DOWNLOAD_TYPE="tar")

    """

    allowed_params = [
        'MEDIA_DATA_LIST', 'TARGET_DIR', 'DOWNLOAD_TYPE', 'DECOMPRESS'
    ]
    for k, v in iteritems(kwds):
        if k not in allowed_params:
            mess_err = ("Error in search():\n'%s' entry for the media_get "
            "function is not allowed\n" % k)
            raise ValueError(mess_err)
        if k == 'TARGET_DIR':
            target_dir = v
        if k == 'DOWNLOAD_TYPE':
            download_type = v
        if k == 'MEDIA_DATA_LIST':
            media_data_list = v

    if 'MEDIA_DATA_LIST' in kwds:
        del kwds['MEDIA_DATA_LIST']  #don't pass it twice

    if len(media_data_list) == 0:
        mess_err = "Nothing to download\n"
        raise ValueError(mess_err)

    if download_type is None:
        for item in media_data_list:
            if item.ias_location != '':
                item.get_file(target_dir=target_dir, **kwds)
            else:
                stdout.write("The data for recnum %s is not at IAS \n" %
                                 str(item.recnum))
    else:
        media_get_selection(
            media_data_list=media_data_list,
            target_dir=target_dir,
            download_type=download_type,
            **kwds)


def media_get_selection(server=None,
                        media_data_list=[],
                        download_type="TAR",
                        **kwds):
    """Donwload a selection from MEDOC server tar or zip file

    Parameters
    ----------
    server : str
        Name of the MEDOC SOLAR server
    media_data_list : list of Sdo_data objects
        The result of media_search can be passed as an argument
    download_type : str
        Can be 'TAR' or 'ZIP'

    Raise
    -----
    ValueError
        server parameter value is not allowed
        media_data_list parameter value is empty

    Returns
    -------
    Files located in the target_dir directory

    Examples
    --------
    >>>sdo_data_list = media_search(
                                server='http://idoc-medoc.ias.u-psud.fr',
                                dates=[d1,d2],
                                series='hmi.m_720s',
                                nb_res_max=10
                       )
    >>>media_get_selection(
                            media_data_list=sdo_data_list,
                            download_type='TAR'
       )
    >>>media_get (media_data_list=sdo_data_list,download_type="tar")
    >>>media_get_selection(
                            MEDIA_DATA_LIST=sdo_data_list,
                            target_dir='results',
                            download_type='TAR'
       )
    """
    for k, v in iteritems(kwds):
        if k == 'DOWNLOAD_TYPE':
            download_type = v
        if k == 'MEDIA_DATA_LIST':
            media_data_list = v
        if k == 'SERVER':
            server = v

    if 'MEDIA_DATA_LIST' in kwds:
        del kwds['MEDIA_DATA_LIST']

# Define dateset target

#server
    allowed_server = [
        'http://medoc-sdo.ias.u-psud.fr',
        'http://medoc-sdo-test.ias.u-psud.fr',
        'http://idoc-medoc-test.ias.u-psud.fr',
        'http://idoc-medoc.ias.u-psud.fr'
    ]
    if server is None:
        server = 'http://medoc-sdo.ias.u-psud.fr'
        stdout.write(
            "server parameter not specified, default value is set: server=%s\n"
            % server)
    if server is not None and server not in allowed_server:
        raise ValueError(
            "Server %s is not allowed for media_get_selection()\nServers "
            "available : %s\n"
            % (server, allowed_server))

    sdo_dataset = Sdo_IAS_SDO_dataset(server + "/webs_IAS_SDO_dataset")

    if len(media_data_list) == 0:
        mess_err = "Nothing to download\n"
        raise ValueError(mess_err)

    media_data_sunum_list = []
    for item in media_data_list:
        if item.ias_location != '':
            media_data_sunum_list.append(item.sunum)
        else:
            stdout.write("The data for recnum %s is not at IAS\n" %
                             str(item.recnum))
    sdo_dataset.__getSelection__(
        sunum_list=media_data_sunum_list, download_type=download_type, **kwds)


def media_search(server=None, dates=None, waves=None, series=None,
                    cadence=None, nb_res_max=-1, **kwds):
    """Use the generic search() from pySitools2 library for Sitools2 SDO
    instance located at IAS

    Parameters
    ----------
    server : str
        Name of the MEDOC SOLAR server

    dates : datetime
        Interval of dates within you wish to make a research,
        It must be specifed and composed of 2 datetime elements d1 d2,
        with d2 >d1

    waves  : list
        Wavelength (in Angstrom)
        Must be a list of wave integer or str
        waves must be in the list [94,131,171,193,211,304,335,1600,1700,6173]
        default value if not specified
        ['94','131','171','193','211','304','335','1600','1700']
        So aia.lev1 data

    series : str
        Series name of the data
        Can be aia.lev1 , hmi.sharp_720s ...
        default value aia.lev1 if not specified

    cadence : str
        Can be a string and in list
        ['12 sec','1 min', '2 min', '10 min', '30 min',
        '1 h', '2 h', '6 h', '12 h' , '1 day', '12 min']
        cadence default values '1 min' or 12 min for hmi data

    nb_res_max : integer
        Nbr of results you wish to display from the results
        Must be an integer and if specified must be >0

    Raise
    -----
    ValueError
        parameter not in allowed_parmas list
        server parameter value is not allowed
        server not specified and hmi data requested ie wave = 6173
        dates parameter is not specified
        d1 > d2 error date range
        wave list have not the same type
        wave arg is not in allowed list
        series not in aia or hmi allowed_list
        series hmi and wave not 6173
        series hmi and server medoc-sdo (only for aia data)
        Cadence not a list of one element
        Cadence not allowed
        nbr_res_max different than -1 and <0
        server not known
    TypeError
        dates type is not a datetime type
        waves type is not a list of int
        series is not a str type

    Returns
    -------
    Sdo_data object list

    Example
    -------
        >>>sdo_data_list = media_search(
                                server='http://idoc-medoc.ias.u-psud.fr',
                                dates=[d1,d2],
                                series='hmi.m_720s',
                                nb_res_max=10
                           )
    """

    #Allow lower case entries
    allowed_params = [
        'DATES', 'WAVES', 'CADENCE', 'NB_RES_MAX', 'SERIES', 'SERVER'
    ]
    for k, v in iteritems(kwds):
        if k not in allowed_params:
            mess_err = ("Error in search():\n'%s' entry for the search "
                "function is not allowed\n" % k)
            raise ValueError(mess_err)
        else:
            if k == 'SERVER':
                server = v
            if k == 'DATES':
                dates = v
            if k == 'WAVES':
                waves = v
            if k == 'SERIES':
                series = v
            if k == 'CADENCE':
                cadence = v
            if k == 'NB_RES_MAX':
                nb_res_max = v

    dates_optim = []

    ######################CONTROL_START
    waves_allowed_aia_list = [
        '94', '131', '171', '193', '211', '304', '335', '1600', '1700'
    ]
    waves_allowed_hmi_list = ['6173']
    cadence_allowed_list = {
        '12s': '12 sec',
        '1m': '1 min',
        '2m': '2 min',
        '10m': '10 min',
        '30m': '30 min',
        '1h': '1 h',
        '2h': '2 h',
        '6h': '6 h',
        '12h': '12 h',
        '1d': '1 day'
    }
    allowed_server = [
        'http://medoc-sdo.ias.u-psud.fr',
        'http://medoc-sdo-test.ias.u-psud.fr',
        'http://idoc-medoc-test.ias.u-psud.fr',
        'http://idoc-medoc.ias.u-psud.fr',
        'http://idoc-solar-portal-test.ias.u-psud.fr'
    ]
    #server
    if server is None and series is None:
        server = 'http://medoc-sdo.ias.u-psud.fr'
        stdout.write(
            "server parameter not specified, default value is set : "
            "server='http://medoc-sdo.ias.u-psud.fr'\n"
        )
    elif server is None and series.startswith('aia'):
        server = 'http://medoc-sdo.ias.u-psud.fr'
        stdout.write(
            "server parameter not specified, default value is set : "
            "server='http://medoc-sdo.ias.u-psud.fr'\n"
        )
    elif server is None and series.startswith('hmi'):
        server = 'http://idoc-medoc-test.ias.u-psud.fr'
    if server is not None and server not in allowed_server:
        raise ValueError("Server %s is not allowed\nServers available : %s\n" %
                         (server, allowed_server))

#dates
    if dates is None:
        mess_err = "Error in search():\ndates entry must be specified"
        raise ValueError(mess_err)
    if type(dates).__name__ != 'list':
        mess_err = ("Error in search():\nentry type for dates is : %s\ndates "
        "must be a list type" % type(dates).__name__)
        raise TypeError(mess_err)
    if len(dates) != 2:
        mess_err = ("Error in search() : %d elements specified for dates\ndates"
        " param must be specified and a list of 2 elements" % len(dates))
        raise ValueError(mess_err)
    for date in dates:
        if type(date).__name__ != 'datetime':
            mess_err = ("Error in search() : type for dates element is %s \n"
            "dates list element must be a datetime type" % type(date).__name__)
            raise TypeError(mess_err)
        else:
            #Trick to adapt to date format on solar-portal-test
            #(to be fixed and that trick removed):
            if server.startswith('http://medoc-sdo'):
                dates_optim.append(str(date.strftime("%Y-%m-%dT%H:%M:%S")))
            else:
                dates_optim.append(
                    str(date.strftime("%Y-%m-%dT%H:%M:%S")) + ".000")
    if dates[1] <= dates[0]:
        mess_err = ("Error in search():\nd1=%s\nd2=%s\nfor dates =[d1,d2] d2 "
        "should be > d1" % (
            dates[1].strftime("%Y-%m-%dT%H:%M:%S"),
            dates[2].strftime("%Y-%m-%dT%H:%M:%S")))
        raise ValueError(mess_err)

#waves

    if waves is None and series is None:
        waves = [
            '94', '131', '171', '193', '211', '304', '335', '1600', '1700'
        ]
        stdout.write(
            "waves parameter not specified, default value is set : "
            "waves = ['94','131','171','193','211','304','335','1600','1700']"
            "\n"
        )
    if waves is None and series == 'aia.lev1':
        waves = [
            '94', '131', '171', '193', '211', '304', '335', '1600', '1700'
        ]
        stdout.write(
            "waves parameter not specified, 'aia.lev1' default value is set : "
            "waves = ['94','131','171','193','211','304','335','1600','1700'] "
            "\n"
        )
    elif waves is None and series.startswith('hmi'):
        waves = [6173]
    #print type(waves).__name__
    if type(waves).__name__ == 'int':
        waves = [str(waves)]

    elif type(waves).__name__ == 'list':
        waves_type_list = [type(wave).__name__ for wave in waves]
        #       print waves_type_list
        counter_waves_type = Counter(waves_type_list)
        #        print(counter_waves_type)
        counter_waves_type_list = list(counter_waves_type)
        #        assert isinstance(counter_waves_type_list, list)
        #        print ("keys : ", counter_waves_type_list)
        # print("type : ",counter_waves_type_list[0])
        if len(counter_waves_type_list) == 1 and counter_waves_type_list[
                0] == 'int':  #same type
            waves_STR = [str(wave) for wave in waves]
            waves = waves_STR
        elif len(counter_waves_type_list) > 1:
            raise ValueError("waves parameter must have same type !!!!\n")
    else:
        mess_err = ("Error in search():\nentry type for waves is : %s\nwaves "
        "must be a list or int type " % type(waves).__name__)
        raise TypeError(mess_err)

    for wave in waves:
        if type(wave).__name__ != 'str':
            mess_err = ("Error in search():\nEntry type for waves element is "
            "%s\nlist element for waves must be a "
            "string or a int type" % type(wave).__name__)
            raise TypeError(mess_err)

        if wave not in waves_allowed_aia_list \
        and wave not in waves_allowed_hmi_list:
            mess_err = ("Error in search():\nwaves= %s not allowed\nwaves"
            " must be in list %s" % (
                waves, waves_allowed_aia_list + waves_allowed_hmi_list))
            raise ValueError(mess_err)

#series
    series_allowed_list = [
        'aia.lev1', 'hmi.sharp_720s', 'hmi.sharp_720s_nrt', 'hmi.m_720s',
        'hmi.sharp_cea_720s_nrt', 'hmi.ic_720s', 'hmi.ic_nolimbdark_720s_nrt'
    ]
    if series is None and '6173' not in waves:
        series = 'aia.lev1'
        stdout.write(
            "series parameter not specified, default value is set :"
            " series='aia.lev1'\n"
        )
    elif series is None and '6173' in waves:
        mess_err = "series parameter must be specified"
        raise ValueError()
    if type(series).__name__ != 'str':
        mess_err = ("Error in search():\nentry type for series is : %s\n"
        "series must be a str type" % type(series).__name__)
        raise TypeError(mess_err)
    if series not in series_allowed_list:
        mess_err = ("Error in search():\nseries= %s not allowed\nseries must "
        "be in list %s" % (series, series_allowed_list))
        raise ValueError(mess_err)
    if series.startswith('hmi'):
        if waves != ['6173']:
            raise ValueError(
                "waves value %s does not correspond to the series specified :"
                " %s "% (",".join(waves), series))
        if server.startswith('http://medoc-sdo'):
            raise ValueError("server %s only for aia.lev1 data\n" % server)
        cadence_allowed_list = {
            '12m': '12 min',
            '1h': '1 h',
            '2h': '2 h',
            '6h': '6 h',
            '12h': '12 h',
            '1d': '1 day'
        }
        if cadence is None:
            cadence = ['12m']
            stdout.write(
                "cadence not specified, default value for %s is set :"
                " cadence=['12m']\n"% series)

#cadence
    if cadence is None and series.startswith('aia.lev1'):
        cadence = ['1m']
        stdout.write(
            "cadence parameter not specified, default value for aia.lev1 is "
            "set : cadence=[1m]\n"
        )
    elif cadence is None and series.startswith('hmi'):
        cadence = ['12m']
        stdout.write(
            "cadence parameter not specified, default value for %s is set :"
            " cadence=[1m]\n"% series)
    if type(cadence).__name__ == 'str':
        cadence = [cadence]
    if type(cadence).__name__ != 'list':
        mess_err = ("Entry type for cadence is : %s\ncadence must be a list or"
        " a string type" % type(cadence).__name__)
        raise ValueError(mess_err)
    if len(cadence) != 1:
        mess_err = ("Error in search():\n%d elements specified for cadence"
        "\ncadence param must be specified and a list of only one"
        "element" % len(cadence))
        raise ValueError(mess_err)

    for cadence in cadence:
        if (cadence not in cadence_allowed_list.keys()) and (
                cadence not in cadence_allowed_list.values()):
            mess_err =("Error in search():\ncadence= %s not allowed\n"
            "cadence for %s must be in list :\n%s\n" % (
                cadence, series, cadence_allowed_list))
            raise ValueError(mess_err)
        elif cadence in cadence_allowed_list.values():
            cadence = [cadence]
        else:
            cadence = [cadence_allowed_list[cadence]]

#nb_res_max
    if type(nb_res_max).__name__ != 'int':
        mess_err =("Error in search():\nentry type for nb_res_max is : "
        "%s\nnb_res_max must be a int type" % type(
            nb_res_max).__name__)
        raise TypeError(mess_err)
    if nb_res_max != -1 and nb_res_max < 0:
        mess_err =("Error in search():\nnb_res_max= %s not allowed\n"
        "nb_res_max must be >0" % nb_res_max)
        raise ValueError(mess_err)
#######################CONTROL_END

#Server definition
#Define dataset url
    if server.startswith('http://medoc-sdo'):
        sdo_dataset = Sdo_ias_sdo_dataset(server + "/webs_IAS_SDO_dataset")
    elif server.startswith('http://idoc-medoc') and series.startswith(
            'hmi'):
        sdo_dataset = Sdo_dataset(server + "/webs_IAS_SDO_HMI_dataset")
    elif server.startswith('http://idoc-medoc') and series.startswith(
            'aia'):
        sdo_dataset = Sdo_dataset(server + "/webs_IAS_SDO_AIA_dataset")
    elif server.startswith('http://localhost') and series.startswith('aia'):
        sdo_dataset = Sdo_dataset(server + "/webs_IAS_SDO_AIA_dataset")
    elif server.startswith('http://localhost') and series.startswith('hmi'):
        sdo_dataset = Sdo_dataset(server + "/webs_IAS_SDO_HMI_dataset")
    else:
        mess_err = server + " is not known"
        raise ValueError(mess_err)

#   sdo_dataset=Sdo_IAS_SDO_dataset(server+"/webs_IAS_SDO_HMI_dataset")
#   sdo_dataset=Sdo_IAS_SDO_dataset(server+"/webs_hmi_dataset")
#   print sdo_dataset
    stdout.write("Loading MEDIA Sitools2 client : %s \n" % server)

    #Param
    dates_param = [[sdo_dataset.fields_dict['date__obs']], dates_optim,
                   'DATE_BETWEEN']
    wave_param = [[sdo_dataset.fields_dict['wavelnth']], waves, 'IN']
    serie_param = [[sdo_dataset.fields_dict['series_name']], [series], 'IN']
    cadence_param = [[sdo_dataset.fields_dict['mask_cadence']], cadence,
                     'cadence']

    #OUTPUT get,recnum,sunum,series_name,date__obs,wave,ias_location,exptime,
    #t_rec_index,ias_path
    if series == 'aia.lev1':
        output_options=[sdo_dataset.fields_dict['get'],
                        sdo_dataset.fields_dict['recnum'],
                        sdo_dataset.fields_dict['sunum'],
                        sdo_dataset.fields_dict['series_name'],
                        sdo_dataset.fields_dict['date__obs'],
                        sdo_dataset.fields_dict['wavelnth'],
                        sdo_dataset.fields_dict['ias_location'],
                        sdo_dataset.fields_dict['exptime'],
                        sdo_dataset.fields_dict['t_rec_index'],
                        sdo_dataset.fields_dict['ias_path']
        ]
    elif series.startswith('hmi.sharp'):
        output_options=[sdo_dataset.fields_dict['recnum'],
                        sdo_dataset.fields_dict['sunum'],
                        sdo_dataset.fields_dict['series_name'],
                        sdo_dataset.fields_dict['date__obs'],
                        sdo_dataset.fields_dict['wavelnth'],
                        sdo_dataset.fields_dict['ias_location'],
                        sdo_dataset.fields_dict['exptime'],
                        sdo_dataset.fields_dict['t_rec_index'],
                        sdo_dataset.fields_dict['ias_path'],
                        sdo_dataset.fields_dict['harpnum']
        ]
    elif series.startswith('hmi'):
        output_options=[sdo_dataset.fields_dict['recnum'],
                        sdo_dataset.fields_dict['sunum'],
                        sdo_dataset.fields_dict['series_name'],
                        sdo_dataset.fields_dict['date__obs'],
                        sdo_dataset.fields_dict['wavelnth'],
                        sdo_dataset.fields_dict['ias_location'],
                        sdo_dataset.fields_dict['exptime'],
                        sdo_dataset.fields_dict['t_rec_index'],
                        sdo_dataset.fields_dict['ias_path']
        ]

#   output_options=[sdo_dataset.fields_dict['recnum'],
#sdo_dataset.fields_dict['sunum'],sdo_dataset.fields_dict['series_name'],\
#sdo_dataset.fields_dict['date__obs'],sdo_dataset.fields_dict['wavelnth'],
#sdo_dataset.fields_dict['ias_location'],
#sdo_dataset.fields_dict['exptime'],sdo_dataset.fields_dict['t_rec_index'],
#sdo_dataset.fields_dict['ias_path'] ]

#Sort date_obs ASC, wave ASC
    sort_options = [[sdo_dataset.fields_dict['date__obs'], 'ASC'],
                    [sdo_dataset.fields_dict['wavelnth'], 'ASC']]
    Q1 = Query(dates_param)
    Q2 = Query(wave_param)
    Q3 = Query(cadence_param)
    Q4 = Query(serie_param)
    #   print Q1
    #   print Q2
    #   print Q3
    #   print Q4

    query_list = [Q1, Q2, Q3, Q4]
    #   query_list=[Q1]

    result = sdo_dataset.search(
        query_list,
        output_options,
        sort_options,
        limit_to_nb_res_max=nb_res_max)
    sdo_data_list = []
    if len(result) != 0:
        for i, data in enumerate(result):
            sdo_data_list.append(Sdo_data(data))
    stdout.write("%s results returned\n" % len(sdo_data_list))
    return sdo_data_list


def media_metadata_search(
                            server=None,
                            media_data_list=[],
                            keywords=[],
                            recnum_list=[],
                            series=None,
                            **kwds):
    """Provide metadata information from MEDOC server

    Parameters
    ----------
    server : str
        Name of the MEDOC SOLAR server
    media_data_list : list of Sdo_data objects
        Result of media_search can be passed as an argument of that function.
    keywords : list of str
        List of names of metadata that you wish to have in the output.
    recnum_list : list of integer
        List of recnum identifier for a series given
        series MUST be provided in case recnum_list is not null
        Computed in case media_data_list is provided
    series : str
        name of the series requested
        That param is computed in case media_data_list is provided

    Raise
    -----
    ValueError
        Parameter not in allowed list
        keyword not specified
        media_data_list is none and server is not specified
        server not allowed
        recnum_list is null
        keyword does not exist for the serie name specified
    TypeError
        keyword no a list type

    Returns
    -------
        List of dictionaries of the data requested
        Returns the exact data from db

    Examples
    --------
        >>>sdo_data_list = media_search(
                                DATES=[d1,d2],
                                SERIES='hmi.m_720s',
                                nb_res_max=10)
        >>>>meta = media_metadata_search(
                MEDIA_DATA_LIST=sdo_data_list,
                KEYWORDS=['date__obs','quality','cdelt1','cdelt2','crval1'])

    """

    #       stdout.write("Keywords list is : %s \n" % keywords)
    #       stdout.write("Recnum list is : %s \n" % recnum_list)
    #       stdout.write("Serie is : %s \n" % series)

    #Allow lower case entries
    for k, v in iteritems(kwds):
        if k not in [
                'KEYWORDS', 'RECNUM_LIST', 'SERIES', 'SEGMENT', 'SERVER',
                'MEDIA_DATA_LIST'
        ]:
            raise ValueError(
                "Error media_metatada_search():\n'%s' parameter for "
                "media_search() function is not allowed\n"
                % k)
        if k == 'KEYWORDS':
            keywords = v
        if k == 'RECNUM_LIST':
            recnum_list = v
        if k == 'SERIES':
            series = v
        if k == 'SEGMENT':
            segment = v
        if k == 'MEDIA_DATA_LIST':
            media_data_list = v
        if k == 'SERVER':
            server = v

    allowed_server = [
        'http://medoc-sdo.ias.u-psud.fr',
        'http://medoc-sdo-test.ias.u-psud.fr',
        'http://idoc-medoc.ias.u-psud.fr',
        'http://idoc-medoc-test.ias.u-psud.fr'
    ]

    #Controls
    ##Keywords
    if len(keywords) == 0:
        raise ValueError("KEYWORD must be specified")
    if type(keywords).__name__ != 'list':
        mess_err =("Error in media_metadata_search():\nentry type for keywords"
        " is : %s\nkeywords must be a list type" % type(
            keywords).__name__)
        raise TypeError(mess_err)
##media_data_list
    if len(media_data_list) != 0:
        series_list = [item.series_name for item in media_data_list]
        count_series_list = Counter(series_list)
        #print count_series_list
        #print count_series_list.keys()
        if len(count_series_list.keys()) > 1:
            stdout.write(
                "Several series_name detected in media_data_list\n")
            if server is None:
                server = 'http://idoc-medoc-test.ias.u-psud.fr'
            result = [
                item.metadata_search(keywords) for item in media_data_list
            ]
            return result
        else:
            recnum_list = [item.recnum for item in media_data_list]
            series = media_data_list[0].series_name

#series
    if series is None and len(media_data_list) == 0:
        raise ValueError(
            "Error in media_metadata_search():\nseries parameter must be "
            "specified\n"
        )

##server
    if server is None and series.startswith('aia'):
        server = 'http://medoc-sdo.ias.u-psud.fr'
        stdout.write(
            "server parameter not specified, default value is set : "
            "server='http://medoc-sdo.ias.u-psud.fr'\n"
        )
    elif server is None and series.startswith('hmi'):
        server = 'http://idoc-medoc-test.ias.u-psud.fr'
    if server is not None and server not in allowed_server:
        raise ValueError("Server %s is not allowed\nServers available : %s\n" %
                         (server, allowed_server))

##recnum_list
    if len(recnum_list) == 0:
        mess_err = "Error in media_metadata_search():\nNo recnum_list "
        "provided\nPlease check your request\n"
        raise ValueError(mess_err)

#Define dataset target
    if server.startswith('http://medoc-sdo'):
        metadata_ds = Sdo_aia_dataset(server + "/webs_aia_dataset")

    elif server.startswith(
            'http://idoc-medoc') and series == 'aia.lev1':
        metadata_ds = Sdo_aia_dataset(server + "/webs_" + "aia_dataset")

    elif server.startswith('http://idoc-medoc') and series.startswith(
            'hmi'):
        metadata_ds = Sdo_aia_dataset(server + "/webs_" + series + "_dataset")

    O1_aia = []
    for key in keywords:
        if key in metadata_ds.fields_dict:
            O1_aia.append(metadata_ds.fields_dict[key])
        else:
            mess_err =("Error metadata_search(): %s keyword does not exist for"
            " series : %s \n" % (key, series))
            raise ValueError(mess_err)
    S1_aia = [[metadata_ds.fields_dict['date__obs'], 'ASC']
              ]  #sort by date_obs ascendant

    #initialize recnumlist
    recnumlist = []
    result = []
    i = 0
    # Make a request for each 500 recnum
    if len(recnum_list) > 500:
        while i < len(recnum_list):
            #               print i
            recnumlist = recnum_list[i:i + 499]
            recnumlist = list(map(str, recnumlist))
            param_query_aia = [[metadata_ds.fields_dict['recnum']], recnumlist,
                               'IN']
            Q_aia = Query(param_query_aia)
            result += metadata_ds.search([Q_aia], O1_aia, S1_aia)
            i = i + 499

#               print "taille result : ",len(result)
    else:
        recnumlist = list(map(str, recnum_list))
        #        print(recnumlist)
        param_query_aia = [[metadata_ds.fields_dict['recnum']], recnumlist,
                           'IN']
        Q_aia = Query(param_query_aia)
        result += metadata_ds.search([Q_aia], O1_aia, S1_aia)
    return result


def metadata_info(server=None, series='aia.lev1'):
    """Displays information concerning the dataset specified
    For example if you need the list of the fields in aia_dataset

    Parameters
    ------------
    series : str
    name of the series requested
    default value aia.lev1

    Raise
    -----
    ValueError
        server not in allowed list

    Returns
    -------
    dataset.display()

    """
    allowed_server = [
        'http://medoc-sdo.ias.u-psud.fr',
        'http://medoc-sdo-test.ias.u-psud.fr',
        'http://idoc-medoc-test.ias.u-psud.fr',
        'http://idoc-medoc.ias.u-psud.fr'

    ]
    #Controls
    ##server
    if server is None:
        server = 'http://medoc-sdo.ias.u-psud.fr'
        stdout.write(
            "server parameter not specified, default value is set : "
            "server='http://medoc-sdo.ias.u-psud.fr'\n"
        )
    elif server is None and series.startswith('hmi'):
        server = 'http://idoc-medoc-test.ias.u-psud.fr'
    if server is not None and server not in allowed_server:
        raise ValueError("Server %s is not allowed\nServers available : %s\n" %
                         (server, allowed_server))

    #Define dataset url
    if server == 'http://medoc-sdo-test.ias.u-psud.fr':
        metadata_ds = Sdo_IAS_SDO_dataset(server + "/webs_aia_dataset")
    elif server == 'http://idoc-medoc-test.ias.u-psud.fr':
        metadata_ds = Sdo_IAS_SDO_dataset(server + "/webs_" + series +
                                          "_dataset")

    return metadata_ds.display()


class Sdo_dataset(Dataset):
    """Definition de la classe Sdo_dataset that heritates of Dataset
    Can have several instances
    """

    def __init__(self, url):
        Dataset.__init__(self, url)


def singleton(class_def):
    """Decorate a class so only one instance exist
    """
    instances = {}

    def get_instance(Class_heritage):
        if class_def not in instances:
            instances[class_def] = class_def(Class_heritage)
        return instances[class_def]

    return get_instance

@singleton
class Sdo_aia_dataset(Dataset):
    """Definition de la classe Sdo_aia_dataset that heritates of Dataset
    This following classes will only have one instance
    """

    def __init__(self, url):
        Dataset.__init__(self, url)

@singleton
class Sdo_ias_sdo_dataset(Dataset):
    """Definition de la classe Sdo_ias_sdo_dataset that heritates of Dataset
    This following classes will only have one instance

    Methods
    -------
    __get__selection__()
        Download Tar or Zip selection

    """

    def __init__(self, url):
        Dataset.__init__(self, url)

    def __getSelection__(self,
                         sunum_list=[],
                         filename=None,
                         target_dir=None,
                         download_type="TAR",
                         quiet=False,
                         **kwds):
        """Use get_selection to retrieve a tar ball or a zip collection
        providing a list of sunum

        Parameters
        ------------
        sunum_list : list
            List of integer
        filename : str
            Name of file(s) downloaded
            You can build a patern including sunum to distinguish them
        target_dir : str
            Directory of download created if it does not exist yet
        download_type : str
            Can value 'TAR' or 'ZIP'
        quiet : boolean
            Display info during th download or not

        Raise
        -----
        ValueError
            download type not allowed
            parameter not allowed
            special char at the end of target_dir
        """
        if download_type.upper() not in ['TAR', 'ZIP']:
            stdout.write(
                "Error get_selection(): %s type not allowed\nOnly TAR or ZIP "
                "is allowed for parameter download_type"
                % download_type)

        for k, v in iteritems(kwds):
            if k not in ['FILENAME', 'TARGET_DIR', 'QUIET', 'DOWNLOAD_TYPE']:
                stdout.write(
                    "Error get_file():\n'%s' entry for the search function is"
                    " not allowed"
                    % k)
            elif k == 'FILENAME':
                filename = v
            elif k == 'TARGET_DIR':
                target_dir = v
            elif k == 'DOWNLOAD_TYPE':
                download_type = v
            elif k == 'QUIET':
                quiet = v
        if filename is None:
            filename = "IAS_SDO_export_" + datetime.utcnow().strftime(
                "%Y-%m-%dT%H-%M-%S") + "." + download_type.lower(
                )  #if not specified this is the default name
        if target_dir is not None:
            if not path.isdir(target_dir):
                stdout.write(
                    "Error get_file():\n'%s' directory did not exist.\n"
                    "Creation directory in progress ..."
                    % target_dir)
                mkdir(target_dir)
            if target_dir[-1].isalnum():
                filename = target_dir + '/' + filename
            elif target_dir[-1] == '/':
                filename = target_dir + filename
            else:
                stdout.write(
                    "Error get_file():\nCheck the param target_dir, "
                    "special char %s at the end of target_dir is not allowed."
                    % target_dir[-1])

        if download_type.upper() == "TAR":
            plugin_id = "plugin02"
        else:
            plugin_id = "plugin03"
        if not quiet:
            stdout.write("Download %s file in progress ..." %
                             download_type.lower())

    #   Dataset.execute_plugin(self,plugin_name=plugin_id, "
    #pkey_list=sunum_list, filename=filename)
        try:
            Dataset.execute_plugin(
                self,
                plugin_name=plugin_id,
                pkey_list=sunum_list,
                filename=filename)
        except:
            stdout.write("Error downloading selection %s " % filename)
        else:
            if not quiet:
                stdout.write("Download selection %s completed" % filename)


class Sdo_data():
    """Definition de la classe Sdo_data

    Attributes
    ---------
    url : str
        The url of the data on MEDOC server
    recnum : int
        Id of the resource in data db
        number of records in level-1 file
        Attention recnum is unique for a serie
    sunum : int
        Another Id of the SDO data_sums db
        Attention you can several records wih same sunum
    date_obs : str
        Observation date (UTC) without time zone of the record computed by IAS
    series_name : str
        Name of the series name , can b hmi.m_720s or aia.lev1 etc ...
    wave : int
        Wavelenght of the record
    ias_location : str
        Location of the data at IAS MEDOC disks
    ias_path : str
        URL of the data , used for hmi redonnant with url
        To analysed : remove it ...
    exptime : float
        Exposure time
    t_rec_index : int
        index of T_REC in db
        Can be used to identify a record in db
    harpnum : int
        Hmi active region patch number for hmi sharp data

    Methods
    -------
    get_file()
        Donwload the record
    metadata_search()
        Print meta information

    """

    def __init__(self, data):
        self.url = ''
        self.recnum = 0
        self.sunum = 0
        self.date_obs = ''
        self.series_name = ''
        self.wave = 0
        self.ias_location = ''
        self.ias_path = ''
        self.exptime = 0
        self.t_rec_index = 0
        self.harpnum = 0
        self.compute_attributes(data)

    def compute_attributes(self, data):
        if 'get' in data:
            self.url = data['get']
        elif 'ias_path' in data:
            self.url = data['ias_path']
        else:
            self.url = ''
        self.recnum = data['recnum']
        self.sunum = data['sunum']
        self.date_obs = data['date__obs']
        if 'series_name' in data:
            self.series_name = data['series_name']
        else:
            self.series_name = ''

        self.wave = data['wavelnth']
        if 'ias_location' in data:
            self.ias_location = data['ias_location']
        else:
            self.ias_location = ''
        if 'ias_path' in data:
            self.ias_path = data['ias_path']
        else:
            self.ias_path = ''
        if 'exptime' in data:
            self.exptime = data['exptime']
        else:
            self.exptime = 0
        self.t_rec_index = data['t_rec_index']
        if 'harpnum' in data:
            self.harpnum = data['harpnum']
        else:
            self.harpnum = 0

    def display(self):
        """Display a representation of SDO data from MEDOC server

        Returns
        -------
        print __repr__()

        """

        print(self.__repr__())

    def __repr__(self):
        if (self.series_name).startswith('hmi.sharp'):
            return (
                "url : %s,recnum : %d, sunum : %d, series_name : %s, "
                "date_obs : %s, wave : %d, ias_location : %s, exptime : %s, "
                "t_rec_index : %d, harpnum : %d\n"
                % (self.url, self.recnum, self.sunum, self.series_name,
                   self.date_obs, self.wave, self.ias_location,
                   self.exptime, self.t_rec_index, self.harpnum))
        else:
            return (
                "url : %s,recnum : %d, sunum : %d, series_name : %s, "
                "date_obs : %s, wave : %d, ias_location : %s, exptime : %s, "
                "t_rec_index : %d, ias_path : %s\n"
                % (self.url, self.recnum, self.sunum, self.series_name,
                   self.date_obs, self.wave, self.ias_location,
                   self.exptime, self.t_rec_index, self.ias_path))

    def get_file(self,
                 decompress=False,
                 filename=None,
                 target_dir=None,
                 quiet=False,
                 segment=None,
                 **kwds):
        """Download hmi and aia data from MEDOC server

        Parameters
        ----------
        decompress : boolean
            fits SDO data are rice-compressed
            That param indicated that you wish to get uncompressed data
            Defautl value is False
        filename : str
            Specify a file name so the file retrieve will be name as specified
            Default value None
        target_dir : str
            User can specify the directory of download
            By design the files are downloaded in the current dir
        quiet : boolean
            set print output active or not
            By design the output is active
            For a quiet get_file process set quiet=True
        segment : str
            Type of the file
            Can value aia.lev1 or spikes for SDO/AIA-LEV1
            Can value 'bitmap', 'Bp_err', 'Bt','conf_disambig', ...

        Raise
        -----
        ValueError
            parameter not allowed

        Returns
        -------
        Files located in the target_dir directory

        """

        #Allow upper case entries
        for k, v in iteritems(kwds):
            if k not in [
                    'DECOMPRESS', 'FILENAME', 'TARGET_DIR', 'QUIET', 'SEGMENT'
            ]:
                mess_err = "Error get_file():\n""'%s' parameter " % k
                mess_err += "for the search function is not allowed \n"
                raise ValueError(mess_err)
            elif k == 'DECOMPRESS':
                decompress = v
            elif k == 'FILENAME':
                filename = v
            elif k == 'TARGET_DIR':
                target_dir = v
            elif k == 'QUIET':
                quiet = v
            elif k == 'SEGMENT':
                segment = v

        filename_pre = ""
        segment_allowed = []
        #Define filename if not provided
        if filename is None and self.series_name == 'aia.lev1':
            filename_pre = self.series_name + "_" + str(
                self.wave) + "A_" + self.date_obs.strftime(
                    '%Y-%m-%dT%H-%M-%S.'
                )  #if not specified this is the default name

        elif filename is None and (self.series_name).startswith('hmi.sharp'):
            filename_pre = self.series_name + "_" + str(
                self.wave) + "A_" + self.date_obs.strftime(
                    '%Y-%m-%dT%H-%M-%S_') + str(self.harpnum) + "."
        #Check for Ic_720s data
        elif filename is None and (self.series_name).startswith('hmi'):
            filename_pre = self.series_name + "_" + str(
                self.wave) + "A_" + self.date_obs.strftime(
                    '%Y-%m-%dT%H-%M-%S.')
        elif filename is not None:
            stdout.write("filename defined by user : %s\n" % filename)
            filename_pre = path.splitext(filename)[0]

#Define segment if it does not exist
        if segment is None and filename is None and (
            self.series_name == 'aia.lev1'):
                segment = ['image_lev1']
        elif segment is None and filename is None and (
            self.series_name).startswith('hmi.sharp'):
            segment=[]
            kwargs={}
            kwargs.update({'media': 'json'})
            url = self.url + '?' + urlencode(kwargs)
            result = load(urlopen(url))
            if result['items']:
                for item in result['items'] :
                    segment.append(item['name'].split(".fits")[0])
                    segment_allowed.append(item['name'].split(".fits")[0])
            else :
                print ("No key 'items' found for %s " % url )
        elif segment is not None and filename is None and (
            self.series_name).startswith('hmi.sharp'):
            kwargs={}
            kwargs.update({'media': 'json'})
            url = self.url + '?' + urlencode(kwargs)
            result = load(urlopen(url))
            if result['items']:
                for item in result['items'] :
                    segment_allowed.append(item['name'].split(".fits")[0])
            else :
                print ("No key 'items' found for %s " % url )

        elif segment is None and filename is None and (
                self.series_name).startswith('hmi.ic'):
            segment = ['continuum']
            segment_allowed.append('continuum')
        elif segment is None and filename is None and (
                self.series_name).startswith('hmi.m'):
            segment = ['magnetogram']
            segment_allowed.append('magnetogram')

        elif filename is not None:
            segment = [filename]

        segment_allowed += [ 'image_lev1']
#        print ("segment : %s" % segment)
#       print (segment_allowed)
        for seg in segment:
            if seg not in segment_allowed and filename is None:
                raise ValueError(
                    "%s segment value not allowed\nSegment allowed :%s" %
                    (seg, segment_allowed))

#Create target location if it does not exist
        if target_dir is not None:
            if not path.isdir(target_dir):
                mess_warn = (("Warning get_file(): '%s' directory "
                    "does not exist.\n") % target_dir)
                mess_warn += "Creation of directory in progress ... \n"
                stdout.write( mess_warn)
                mkdir(target_dir)
            if target_dir[-1].isalnum():
                filename_pre = target_dir + '/' + filename_pre
            elif target_dir[-1] == '/':
                filename_pre = target_dir + filename_pre
            else:
                mess_err = ("Error get_file()\nCheck the parameter target_dir,"
                "special char %s at the end of the target_dir is not "
                "allowed.\n" % target_dir[-1])
                raise ValueError(mess_err)

#Specification for aia.lev1 and COMPRESS param
        if not decompress and self.series_name == 'aia.lev1':
            self.url = self.url + ";compress=rice"

#Define filename_path and file_url
        for file_suff in segment:
            if filename is None:
                filename_path = filename_pre + file_suff + '.fits'
            else:
                filename_path = filename_pre + '.fits'
                file_url = self.url

            if (self.series_name).startswith('hmi'):
                #   filename_path=filename_pre+file_suff+'.fits'
                #   print "filename_path :", filename_path
                file_url = self.url + "/" + file_suff + '.fits'
            #   file_url=self.url+"/"+file_suff+'.fits'
            #   print "filename_url :", file_url
            elif self.series_name == ('aia.lev1'):
                # filename_path=filename_pre+file_suff+'.fits'
                file_url = self.url

            #print("filename_url :", file_url)
            #print("filename_pre :", filename_pre)
            #print("filename_path :", filename_path)

#Retrieve data
            try:
                urlretrieve(file_url, filename_path)
            except:
                stdout.write("Error downloading %s\n" % filename_path)
            else:
                if not quiet:
                    stdout.write("Download file %s completed\n" %
                                     filename_path)
                    stdout.flush()

    def metadata_search(self, server=None, keywords=[], **kwds):
        """Provide metadata information from MEDOC server

        Parameters
        ----------
        server : str
            Name of the MEDOC SOLAR server
        keywords : list of str
            List of names of metadata that you wish to have in the output.

        Raise
        -----
        ValueError
            parameter is not allowed
            keyword not specified
            keyword is not a list type
            server is unknown
            keyword does not exist for the dataset
            no data returned

        Returns
        -------
            List of dictionaries of the data requested
            Returns the exact data from db
        """

        #Allow lower case entries
        for k, v in iteritems(kwds):
            if k not in ['SERVER', 'KEYWORDS']:
                raise ValueError(
                    "Error get_file():\n'%s' entry for the search function is"
                    " not allowed"
                    % k)
            elif k == 'KEYWORDS':
                keywords = v
            elif k == 'SERVER':
                server = v

        allowed_server = [
        'http://medoc-sdo.ias.u-psud.fr',
        'http://medoc-sdo-test.ias.u-psud.fr',
        'http://idoc-medoc-test.ias.u-psud.fr',
        'http://idoc-medoc.ias.u-psud.fr',
        'http://localhost:8184'
        ]

        server_url=sitools2_url
#server
        if server_url.startswith("http://localhost"):
            pass
        elif server is None and self.series_name.startswith('aia'):
            server_url = 'http://medoc-sdo.ias.u-psud.fr'
        elif server is None and self.series_name.startswith('hmi'):
            server_url = 'http://idoc-medoc-test.ias.u-psud.fr'

        if server is not None and server not in allowed_server:
            raise ValueError(
                "Server %s is not allowed \nServers available : %s\n" %
                         (server, allowed_server)
            )

 #       print ("server : %s" % server_url)

        if len(keywords) == 0:
            raise ValueError("keywords must be specified")
        if type(keywords).__name__ != 'list':
            mess_err = "Error in metadata_search():\nentry type for keywords "
            "is : %s\nkeywords must be a list type" % type(keywords).__name__
            raise TypeError(mess_err)

        if server_url.startswith('http://medoc-sdo'):
            metadata_ds = Sdo_aia_dataset(server_url + "/webs_aia_dataset")
        elif server_url.startswith('http://idoc-medoc'):
            metadata_ds = Sdo_dataset(server_url + "/webs_" +
                                      self.series_name + "_dataset")
        elif server_url.startswith('http://localhost'):
            metadata_ds = Sdo_dataset(server_url + "/webs_" +
                                      self.series_name + "_dataset")

        else:
            raise ValueError(
                "metadata_ds is not valued please check your server param\n")

#       print "Dataset targetted :" ,metadata_ds.name ,metadata_ds.uri
#       print "Query is for %s recnum %s " % (self.series_name, self.recnum)
#controls
        recnum_list = [str(self.recnum)]
        param_query = [[metadata_ds.fields_dict['recnum']], recnum_list, 'IN']
        Q1 = Query(param_query)
        O1 = []
        for key in keywords:
            if key in metadata_ds.fields_dict:
                O1.append(metadata_ds.fields_dict[key])
            else:
                raise ValueError(
                    "Error metadata_search(): %s keyword does not exist for %s"
                    % (key, metadata_ds.name))
        S1 = [[metadata_ds.fields_dict['date__obs'], 'ASC']
              ]  #sort by date_obs ascendant
        #print(metadata_ds.search([Q1], O1, S1))
        if len(metadata_ds.search([Q1], O1, S1)) != 0:
            return metadata_ds.search([Q1], O1, S1)[0]
        else:
            raise ValueError(
                "No data found for your request\nCheck your parameters")


def main():
    d1 = datetime(2016, 6, 10, 0, 0, 0)
    d2 = d1 + timedelta(days=1)
    #sdo_data_list=media_search(dates=[d1,d2],waves=['335'],cadence=['1h'],
    #nb_res_max=10)
    #   print sdo_data_list
    sdo_data_list = media_search(
        dates=[d1, d2],
        series='hmi.sharp_cea_720s_nrt',
        cadence=['1h'],
        nb_res_max=10)
    print(sdo_data_list)
    # Unit test media_metadata_search
    print("Test media_metadata_search")
    recnum_list = []
    for item in sdo_data_list:
        recnum_list.append(str(item.recnum))
    print(recnum_list)
    meta = media_metadata_search(
        keywords=[
            'recnum', 'sunum', 'date__obs', 'quality', 'cdelt1', 'cdelt2',
            'crval1'
        ],
        series="hmi.sharp_cea_720s_nrt",
        recnum_list=recnum_list)
    print(meta)


#Unit test get_file
#   for data in sdo_data_list :
#   for data in sdo_hmi_data_list :
#       data.get_file(target_dir='results', segment=['Br'])

#Unit test metadata_search
#   print "Test metadata_search"
#   for item in sdo_data_list:
#       my_meta_search=item.metadata_search(keywords=['sunum','recnum',
#       'quality','cdelt1','cdelt2','crval1'])
#       print my_meta_search
if __name__ == "__main__":
    main()
