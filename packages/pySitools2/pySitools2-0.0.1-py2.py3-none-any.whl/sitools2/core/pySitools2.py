#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
This is a generic python Sitools2 tool
pySitools2 tool has been designed to perform all operations available within
Sitools2. The code defines several classes SitoolsInstance, Field, Query,
Dataset and Project.
Example of application :
A Solar tool to request and retrieve SDO data from IAS (Institut
d'Astrophysique Spatiale)
see http://sdo.ias.u-psud.fr/python/sdo_client_idoc.html



@author: Pablo ALINGERY for IAS 28-08-2012
"""
__license__ = "GPLV3"
__author__ = "Pablo ALINGERY"
__credit__ = ["Pablo ALINGERY", "Elie SOUBRIE"]
__maintainer__ = "Pablo ALINGERY"
__email__ = "pablo.alingery.ias.u-psud.fr"

from sys import stdout, stderr
from datetime import datetime, timedelta
from future.moves.urllib.parse import urlencode
from future.moves.urllib.request import urlopen, urlretrieve
from future.moves.urllib.error import HTTPError

try:
    from simplejson import load
except:
    stderr.write(
        "Import failed in module sdo_client_medoc :\n\tsimplejson module is"
        "required\n"
    )
    raise ImportError
try:
    from xml.dom.minidom import parseString

except:
    stderr.write(
        "Import failed in module sdo_client_medoc :\n\txml.dom.minidom module "
        "is required\n"
    )
    raise ImportError


class Sitools2Instance():
    """Define an server instance of Sitools2.
    An instance of Sitools2Instance is defined using its url.

    Attributes
    ----------
    instanceUrl : str
        The url of the MEDOC server

    Methods
    -------
    list_project()
        Return a list of the projects available for the instance
    """


    def __init__(self, url):
        """Initialize class Sitools2Instance"""

        self.instanceUrl = url
        try:
            load(urlopen(url + "/sitools/portal"))
        except:
            err_mess = ("Error in Sitools2Instance.__init__() :\nSitools2 "
            "instance %s not available please contact admin for more info\n"
            "" % url)
            stderr.write(err_mess)
            raise Exception


    def list_project(self, **kwargs):
        """List all projects available for that SitoolsInstance

        parameters
        ----------
        kwargs : object
            Any param that can be usefull for the function urlencode()

        Raise
        -----
        Exception
            Cannot create project a Project instance

        Return
        ------
        list of objects project instance of Project
        """
        sitools_url = self.instanceUrl
        data = []
        kwargs.update({'media': 'json'})
        url = sitools_url + '/sitools/portal/projects' + '?' + urlencode(
            kwargs)
 #       print("url portal : %s" % url)
        result = load(urlopen(url))
        out_mess = "%s projects detected\n" % result['total']
        stdout.write(out_mess)
        stdout.flush()
        projects = result['data']
#        print ("projects : %s\n" % projects)
        for i, project in enumerate(projects):
            p_url = sitools_url + project['sitoolsAttachementForUsers']
#             print ("project url : %s" % p_url)
            try:
                data.append(Project(p_url))
            except:
                out_mess = ("Error in Sitools2Instance.list_project() :"
                "\nCannot create object project %s, %s protected \n"
                "Contact admin for more info\n" % (project['name'], p_url))
                stdout.write(out_mess)
                stdout.flush()
                raise Exception
        return data


class Field():
    """Definition of a Field class.
    A field is a item from a dataset.
    It has several attributes : name, ftype, ffilter(boolean), sort(boolean),
    behavior.

    Attributes
    ----------
    name : str
        name of the field
    ftype : str
        type of the field
    ffilter : boolean
        Stand of the field is filtered or not
    sort : boolean
        Stand if the field if sorted or not
    behavior : str
        Apply special behavior on field like datasetlink

    Methods
    -------
    list_project()
        Return a list of the projects available for the instance
    """


    def __init__(self, dictionary):
        """Initialize class Field"""
        self.name = ""
        self.ftype = ""
        self.ffilter = False
        self.sort = False
        self.behavior = ""
        self.compute_attributes(dictionary)

    def compute_attributes(self, dictionary):
        """Compute attribute from web service dataset description"""
        keys_list_ = []
        if 'columnAlias' in dictionary:
            #print ("type : %s" % type(dictionary['columnAlias']).__name__)
            #print (dictionary['columnAlias'])
            self.name = dictionary['columnAlias']
        if 'sqlColumnType' in dictionary:
            self.ftype = dictionary['sqlColumnType']
        if 'filter' in dictionary:
            self.ffilter = dictionary['filter']
        if 'sortable' in dictionary:
            self.sort = dictionary['sortable']
        if 'columnRenderer' in dictionary:
            self.behavior = dictionary['columnRenderer']['behavior']

    def display(self) :
        """Display a representation of the data"""
        print(self.__repr__())

    def __repr__(self):
        return (
            "Field object display() :\n\t%s\n\t\tftype : %s\n\t\tffilter : "
               "%s\n\t\tsort : %s\n\t\tbehavior : %s" % (self.name,
                    self.ftype, self.ffilter, self.sort, self.behavior))


class Query():
    """Definition of a Query class.
       A Query defines the request passed to the server.


    Attributes
    ----------
    fields_list : list
        list of objects field
    name_list : list
        list of field.name attribute
    value_list : list
        List the value of the objetc(s) field above
    operation : str
        Name of operation ge, le, gte, lte, lt, eq, gt,
       lte, like, in, numeric_between, date_between, cadence

    Raise
    -----
    TypeError
        Query first argument is not a list
        Query second argument is not a list
    """


    def __init__(self, param_list) :
        """Initialize class Query"""
        self.fields_list = []
        self.name_list = []
        self.value_list = []
        self.operation = ""
        self.compute_attributes(param_list)

    def compute_attributes(self, param_list):
        """Compute attribute from client request
        """
        if type(param_list[0]).__name__ != 'list':
            mess_err = ("Error in Query.compute_attributes() :\n"
            "Query first argument type is : %s\nQuery first argument type "
            "should be : list\n" % type(param_list[0]).__name__)
            stderr.write(mess_err)
            raise TypeError(mess_err)
        if type(param_list[1]).__name__ != 'list':
            mess_err = ("Error in Query.compute_attributes() :\n"
            "Query second argument type is : %s\nQuery second argument type "
            "should be : list\n\n\n" % type(param_list[1]).__name__)
            stderr.write(mess_err)
            raise TypeError(mess_err)
        for field in param_list[0]:
            self.name_list.append(str(field.name))
        self.fields_list = param_list[0]
        self.value_list = param_list[1]
        self.operation = param_list[2]

#Ouptut attributes of Query

    def display(self):
        print(self.__repr__())

#Define a repr of this Class

    def __repr__(self):
        return ("name : % s\nvalue : %s\nOperation : %s" %
                (", ".join(self.name_list), ", ".join(self.value_list),
                 self.operation))


class Dataset():
    """Definition of a Dataset class.
       It is related to a Sitools2 dataset, which is a set of instances of
       the class Field with specific properties.
       Dataset provides .

    Attributes
    ----------
    name : str
        name of the dataset
    description : str
        description of the dataset
    uri : str
        uniform resource id of the dataset
    url : str
        uniform resource location of the dataset
    fields_list : list
        list of field objects instance of Field
    fields_dict : dict
        dictionary of fields with key equals the name of the field
    filter_list : list
        list of field object that can be filtered
    allowed_filter_list : list
        list of the filtered field.name attributes of field
    sort_list : list
        list of field object that can be sorted
    allowed_sort_list : list
        list of the sorted field.name attributes of field
    resource_target : list
        list of str of the resources associated with the dataset like tar zip
        plugin
    noClientAccess_list : list
        list of str of the restricted field for the web user
    primary_key : str
        Field object of the primary in sitools2 db

    Methods
    -------
    search()
       The generic powerfull search method that allows a python client to
       make a request on a Sitools2 server
    resources_list()
        List all the resources available for the current dataset

    Raise
    -----
    Exception
        Dataset not accessible
    """


    def __init__(self, url):
        """Initialize class Dataset"""
        #        print("url to load :",url)
        #        dataset_url_txt=urlopen(url)
        try:
            load(urlopen(url))
        except:
            err_mess = ("Error in Dataset.__init__() :\nDataset %s not "
            "available, please send an email to medoc-contact@ias.u-psud.fr "
            "to get some help\n" % url)
            stderr.write(err_mess)
            raise Exception
        self.name = ""
        self.description = ""
        self.uri = "/" + url.split("/")[-1]
        self.url = url
        self.fields_list = []
        self.fields_dict = {}
        self.filter_list = []
        self.allowed_filter_list = []
        self.sort_list = []
        self.allowed_sort_list = []
        self.resources_target = []
        self.noClientAccess_list = []
        self.primary_key = ""
        self.compute_attributes()
        self.resources_list()


    def compute_attributes(self, **kwargs):
        """Compute attribute from web service answer dataset description

        Raise
        -----
        Exception
            Compute attributes failed
        """
        kwargs.update({'media': 'json'})
        url = self.url + '?' + urlencode(kwargs)
        #print ("url : %s " % url)
        try:
            result = load(urlopen(url))
            #print ("result : \n %s " % result)
            self.name = result['dataset']['name']
            self.description = result['dataset']['description']
            columns = result['dataset']['columnModel']
            for column in columns:
                #print(type(column).__name__)
                self.fields_list.append(Field(column))
                self.fields_dict.update({column['columnAlias']: Field(column)})
                if ('filter' in column and column['filter']):
                    self.filter_list.append(Field(column))
                if ('sortable' in column and column['sortable']):
                    self.sort_list.append(Field(column))
                if ('primaryKey' in column and column['primaryKey']):
                    self.primary_key = (Field(column))
                if ('columnRenderer' in column and
                        column['columnRenderer']['behavior'] ==
                        "noClientAccess"):
                    self.noClientAccess_list.append(column['columnAlias'])
        except:
            err_mess = ("Error in Dataset.compute_attributes(), "
            "please contact medoc-contact@ias.u-psud.fr for more info\n")
            stderr.write(err_mess)
            raise Exception
        for field in self.filter_list:
            self.allowed_filter_list.append(field.name)
        for field in self.sort_list:
            self.allowed_sort_list.append(field.name)


    def resources_list(self):
        """Explore and list dataset resources, method=options has to be allowed
        """
        try:
            url = urlopen(self.url + '?method=OPTIONS')
            wadl = url.read()
            domWadl = parseString(wadl)
            resources = domWadl.getElementsByTagName('resource')
            for i in range(len(resources)):
                self.resources_target.append(self.url + "/" + resources[i]
                                             .getAttribute('path'))
        except:
            out_mess = ("\t\t\tError in Dataset.ressources_list() not "
            "accessible, please contact admin for more info\n")
            raise ValueError(out_mess)



    def search(self,
               query_list,
               output_list,
               sort_list,
               limit_request=350000,
               limit_to_nb_res_max=-1,
               **kwargs):
        """This is the generic search() method of a Sitools2 instance.
        Throw a research request on Sitools2 server, inside limit 350000
        so > 1 month full cadence for SDO project

        parameters
        ----------
        query_list : list
            List of query objects
        output_list :
            list of field objects
        sort_list :
            list of field object sorted
        limit_request :
            limit answers from server set by design to 350000
        limit_to_nb_res_max :
            From the results sent by the server limit to that value

        Raise
        -----
        ValueError
            field provided for filter is not allowed
            operation not allowed
            field provided for sort is not allowed

        Return
        ------
            List of dictionaries

        Example
        -------
        >>>result=ds1.search([Q1,Q2,Q3,Q4],O1,S1,limit_to_nb_res_max=10)
        Where Q1, Q2, Q3 & Q4 can be :
        >>>Q1=Query(param_query1)
        >>>Q2=Query(param_query2)
        >>>Q3=Query(param_query3)
        >>>Q4=Query(param_query4)
        Where param _query1, param_query2, param_query3, param_query4 can
        value :
        >>>param_query1=[[ds1.fields_list[4]],['2012-08-10T00:00',
                        '2012-08-10T01:00'],'DATE_BETWEEN']
        >>>param_query2=[[ds1.fields_list[5]],['335'],'IN']
        >>>param_query3=[[ds1.fields_list[10]],['1 min'],'CADENCE']
        >>>param_query4=[[ds1.fields_list[8]],['2.900849'],'LTE']
        """
        kwargs.update({'media': 'json', 'limit': 300, 'start': 0})
        #Initialize counter
        j = 0  #filter counter
        i = 0  #p counter
        for num_query, query in enumerate(
                query_list):  #create url options p[$i] and filter[$j]
            operation = query.operation.upper(
            )  #transform entries as upper letter
            if operation == 'GE':
                operation = 'GTE'
            elif operation == 'LE':
                operation = 'LTE'
            if operation in ['LT', 'EQ', 'GT', 'LTE', 'GTE']:
                for field in query.fields_list:
                    if field.name not in self.allowed_filter_list:
                        err_mess = ("Error in Dataset.search() :\nfilter on %s"
                        "is not allowed\n" % field.name)
                        stdout.write(err_mess)
                        raise ValueError(err_mess)
                kwargs.update({
                    'filter[' + str(j) + '][columnAlias]':
                    "|".join(query.name_list),
                    'filter[' + str(j) + '][data][type]': 'numeric',
                    'filter[' + str(j) + '][data][value]':
                    "|".join(query.value_list),
                    'filter[' + str(j) + '][data][comparison]': operation
                })
                j += 1  #increment filter counter
            elif operation in ['LIKE']:
                operation = 'TEXT'
                i += 1  #increment p counter
            elif operation in ['IN']:
                operation = 'LISTBOXMULTIPLE'
                kwargs.update({
                    'p[' + str(i) + ']': operation + "|" + "|".join(
                        query.name_list) + "|" + "|".join(query.value_list)
                })
                i += 1  #increment p counter
            elif operation in ['DATE_BETWEEN', 'NUMERIC_BETWEEN', 'CADENCE']:
                #print (operation)
                #print (query.name_list)
                #print (query.value_list)
                kwargs.update({
                    'p[' + str(i) + ']': operation + "|" + "|".join(
                        query.name_list) + "|" + "|".join(query.value_list)
                })
                i += 1  #increment p counter
            else:
                allowed_operations = "ge, le, gte, lte, lt, eq, gt, lte, like,"
                "  in, numeric_between, date_between"
                err_mess = ("Operation not available : %s \nAllowed operations"
                "are : %s\n" % (operation, allowed_operations))
                stderr.write(err_mess)
                raise ValueError(err_mess)
        output_name_list = []
        output_name_dict = {}
        for i, field in enumerate(
                output_list
        ):  #build output object list and output object dict with name as a key
            output_name_list.append(str(field.name))
            output_name_dict.update({str(field.name): field})
        kwargs.update({#build colModel url options
            'colModel' : '"'+", ".join(output_name_list)+'"'
        })
        sort_dic_list = []
        for field in sort_list:  #build sort output options
            if field[0].name not in self.allowed_sort_list:
                err_mess = ("Error in Dataset.search():\nsort on %s is not "
                "allowed\n" % field.name)
                stderr.write(err_mess)
                raise ValueError(err_mess)
            sort_dictionary = {}
            sort_dictionary.update({
#                 "field" : (field[0].name).encode('utf-8') ,
                "field": (str(field[0].name)),
                "direction": field[1]
            })
            sort_dic_list.append(sort_dictionary)
        temp_kwargs = {}
        temp_kwargs.update({'sort': {"ordersList": sort_dic_list}})
        temp_url = urlencode(temp_kwargs).replace('+', '').replace('%27',
                                                                   '%22')
        #        stdout.write( "temp_url : "+temp_url+"\n")
        #        stdout.write( "kwargs : "+urlencode(kwargs)+"\n")
        url_count = self.url + "/count" + '?' + urlencode(
            kwargs) + "&" + temp_url  #Build url just for count
        #stdout.write( "url_count : "+url_count+"\n")
        url = self.url + "/records" + '?' + urlencode(
            kwargs) + "&" + temp_url  #Build url for the request
        #stdout.write( "url : "+url+"\n")
        result_count = load(urlopen(url_count))
        nbr_results = result_count['total']
        result = []
        #Check if the request does not exceed 350 000 items
        if nbr_results < limit_request:
            if limit_to_nb_res_max > 0 and limit_to_nb_res_max < kwargs[
                    'limit']:  #if nbr to display is specified and < 300
                kwargs['limit'] = limit_to_nb_res_max
                kwargs['nocount'] = 'true'
                nbr_results = limit_to_nb_res_max
                url = self.url + "/records" + '?' + urlencode(
                    kwargs) + "&" + temp_url
        #        stdout.write( "if url : "+url+"\n")
            elif limit_to_nb_res_max > 0 and limit_to_nb_res_max >= kwargs[
                    'limit']:  #if nbr to display is specified and >= 300
                if limit_to_nb_res_max < nbr_results:
                    nbr_results = limit_to_nb_res_max
                kwargs['nocount'] = 'true'
                url = self.url + "/records" + '?' + urlencode(
                    kwargs) + "&" + temp_url
        #        stdout.write( "elif url : "+url+"\n")
            while (nbr_results - kwargs['start']
                   ) > 0:  #Do the job per 300 items till nbr_result is reached
                #Check that request is done each 300 items
                result_temp = load(urlopen(url))
                for data in result_temp['data']:
                    result_dict = {}
                    for k, v in data.items():
                        if (k not in self.noClientAccess_list and
                                k != 'uri' and k in output_name_list
                            ) or k in output_name_list:
                            if output_name_dict[k].ftype.startswith('int'):
                                result_dict.update({k: int(v)})
                            elif output_name_dict[k].ftype.startswith('float'):
                                result_dict.update({k: float(v)})
                            elif output_name_dict[k].ftype.startswith(
                                    'timestamp'):
                                (dt, mSecs) = v.split(".")
                                dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
                                mSeconds = timedelta(microseconds=int(mSecs))
                                result_dict.update({k: dt + mSeconds})
                            else:
                                result_dict.update({k: v})
                    result.append(result_dict)
                kwargs['start'] += kwargs[
                    'limit']  #increment the job by the kwargs limit given
                    #(by design)
                url = self.url + "/records" + '?' + urlencode(
                    kwargs
                ) + "&" + temp_url  #encode new kwargs and build new url
                #for request
#                stdout.write( "url : "+url+"\n")
            return result
        else:
            out_mess = ("Not allowed\nNbr results (%d) exceeds limit_request"
            " param: %d\n" % ( result_count['total'], limit_request))
            raise ValueError(out_mess)


    def display(self):
        """Output attributes of Dataset
        """
        print(self.__repr__())

    def __repr__(self):
        """Representation of an instance of Dataset

        return
        ------
        All info available for a dataset
        """
        phrase = ""
        phrase += ("\n\nDataset object display() :\n\t%s\n\t\tdescription : "
        "%s\n\t\turi : %s\n\t\turl : %s\n\t\tprimary_key : %s" % (
            self.name, self.description, self.uri, self.url,
            self.primary_key.name))
        phrase += "\n\t\tresources_list :"
        for i, res in enumerate(self.resources_target):
            phrase += "\n\t\t\t%d) %s" % (i, res)
        phrase += "\n\t\tfields list :"
        for i, field in enumerate(self.fields_list):
            phrase += "\n\t\t\t%d) %s" % (i, str(field.name))
        phrase += "\n\t\tfilter list :"
        for i, field in enumerate(self.filter_list):
            phrase += "\n\t\t\t%d) %s" % (i, str(field.name))
        phrase += "\n\t\tsort list :"
        for i, field in enumerate(self.sort_list):
            phrase += "\n\t\t\t%d) %s" % (i, str(field.name))
        return phrase

    def execute_plugin(self,
                       plugin_name=None,
                       pkey_list=[],
                       FILENAME=None,
                       **kwargs):
        """Donwload a selection of data

        parameter
        ---------
        plugin_name
            name of the plugin within sitools2
        pkey_list
            list of ids primary_key for the currecnt dataset
        FILENAME
            name of the file donwloaded

        raise
        -----
        ValueError
            No plugin name provided
            plugin name does not exist
            No filename provided

        Return
        ------
            result execution of the plugin
            can be a tar zip etc...
        """
        resources_list = []
        if plugin_name is None:
            err_mess = "Error execute_plugin():\nNo plugin_name provided\n"
            raise ValueError (err_mess)
        for resource in self.resources_target:
            resources_list.append(resource.split("/")[-1])
        if plugin_name not in resources_list:
            err_mess = ("Error execute_plugin():\nThis plugin_name %s does not"
            "exist in %s dataset\n" % (plugin_name, self.name))
            raise ValueError (err_mess)
        if len(pkey_list) == 0:
            err_mess = "Error execute_plugin():\n"
            "No identifiers pkey provided\n"
            raise ValueError (err_mess)
        if FILENAME is None:
            err_mess = "Error execute_plugin():\nNo FILENAME provided\n"
            raise ValueError (err_mess)
        operation = 'LISTBOXMULTIPLE'
        kwargs.update({
            'p[0]': operation + "|" + self.primary_key.name + "|" + "|".join(
                str(pkey) for pkey in pkey_list)
        })
        url = self.url + "/" + plugin_name + "?" + urlencode(kwargs)
        print ("url plugin : %s\n" % url)
        try :
            request=urlopen(url)
            print ("info : \n%s" % request.info())
            print ("code : \n%s" % request.getcode())
        except HTTPError as e :
            print (e.code)
            print (e.reason)
        else :
            return urlretrieve('%s' % url, FILENAME)


class Project():
    """Define a Project class.
       A Project instance gives details about a project of Sitools2.

    attributes
    ----------
    name : str
        name of the Project
    description : str
        desciption of the project
    uri ; str
        uniform resource location
    url : str
        uniform resource identifier
    resource_target : list
        list of resources target

    methods
    -------
    dataset_list()
        returns information about the number of datasets available,
        their name and uri.
    """


    def __init__(self, url):
        """Initialize Project"""
        self.name = ""
        self.description = ""
        self.uri = "/" + url.split("/")[-1]
        self.url = url
        self.resources_target = []
        self.compute_attributes()
        self.resources_list()

    def compute_attributes(self, **kwargs):
        """Compute_attributes builds value for instance Project
        """
        kwargs.update({'media': 'json'})
        url = self.url + '?' + urlencode(kwargs)
        result = load(urlopen(url))
        self.name = result['project']['name']
        self.description = result['project']['description']


    def resources_list(self):
        """Explore Project resources (method=options should be allowed)
        """
        url = urlopen(self.url + '?method=OPTIONS')
        wadl = url.read()
        try:
            domWadl = parseString(wadl)
        except:
            out_mess = ("Project %s : project.resources_list() not allowed, "
            "please contact admin for more info\n" % self.name)
            raise ValueError(out_mess)
        else:
            resources = domWadl.getElementsByTagName('resource')
            for i in range(len(resources)):
                self.resources_target.append(self.url + "/" + resources[i]
                                             .getAttribute('path'))


    def display(self):
        """Ouptut Project attributes"""
        print(self.__repr__())


    def __repr__(self):
        """Represention of Project instance

        return
        ------
        Name, description, uri, url
        """
        phrase = ""
        phrase += ("\n\nProject object display() :\n\t"
        "%s\n\t\tdescription : %s\n\t\turi : %s\n\t\turl : %s" % (self.name,
            self.description, self.uri, self.url))
        phrase += "\n\t\tresources list :"
        if len(self.resources_target) != 0:
            for i, res in enumerate(self.resources_target):
                phrase += "\n\t\t\t%d) %s" % (i, res)
        return phrase



    def dataset_list(self, **kwargs):
        """Return relevant information concerning the datasets of your project
        List all datasets in the Project and create the dataset objects

        raise
        -----
        Exception
            Dataset not accessible
        """
        sitools_url = self.url.split("/")[0] + "//" + self.url.split(
            "//")[1].split("/")[0]
        kwargs.update({'media': 'json'})
        url = self.url + '/datasets' + '?' + urlencode(kwargs)
        data = []
        try:
            result = load(urlopen(url))
            if len(result['data']) != 0:
                for i, dataset in enumerate(result['data']):
                    ds_url = sitools_url + dataset['url']
                    data.append(Dataset(ds_url))
        except:
            out_mess = ("Error in Project.dataset_list() :\nCannot access "
            "dataset %s is protected\nContact admin for more info\n" % url)
            raise Exception(out_mess)
        return data
