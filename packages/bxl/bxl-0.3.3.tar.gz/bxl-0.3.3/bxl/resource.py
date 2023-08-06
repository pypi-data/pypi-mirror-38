import sys
import urllib
import datetime
import logging as log
import os.path as op
import xnat
import utils

# CLASSES
# class Entity():
    # ''' Class defining the structure of an XNAT entity, understanding a entity as an element of the set {project,subject,experiment}'''

    # def __init__(self, type=None, identifier=None):
        # self.type = type
        # self.id = identifier


# class RC_metainfo():
    # ''' Class defining the attributes of Resource Collection metainformation (metadata)'''

    # def __init__(self, format=None, content=None):
        # self.format = format
        # self.content = content


class ResourceManager(object):
    def __init__(self):
        pass

    def create_resource_collection(self, entity_type, entity_name, label,
            meta_rcFormat=None, meta_rcContent=None, force_create=False):
        '''Create a entity-related resource collection (RC) for hosting data,
        understanding a entity as an element of the set {project,subject,experiment}
        Returns the xnat_abstractresource_id of the created resource if successful'''

        #Compose the root-entity URL
        root_entity_URL = self.host + '/data/%s/%s' %(entity_type, entity_name)

        #Verify root entity exists in XNAT (security check)
        if not self.resource_exist(root_entity_URL):
            msg = 'No %s with ID "%s" reachable at: %s'\
                % (entity_type, entity_name, self.host)
            raise xnat.XNATException(msg)

        #Compose the resource collection URL
        URL = root_entity_URL + '/resources/%s' %label

        #Verify if resource collection already exists OR there's an Internal Server Error (Subject entities REST API inconsistency)
        if self.resource_exist(URL):
            if force_create :
                msg ='A %s-based Resource Collection with such name (%s) already '\
                    'exists in the current context' %(entity_type,label)
                raise xnat.XNATException(msg)
            else :
                msg ='[Warning] A %s-based Resource Collection with such name (%s) '\
                    'already exists in the current context' %(entity_type,label)
                log.warning(msg)

        #Otherwise, lets create it!
        else:
            #When present, encode meta-information attributes (i.e. Resource Collection format and content) for the HTTP PUT request
            opts = None
            opts_dict = {}
            if meta_rcFormat :
                opts_dict.update({'format': meta_rcFormat.upper()})
            if meta_rcContent :
                opts_dict.update({'content': meta_rcContent})

            if opts_dict :
                opts = urllib.urlencode(opts_dict)

            #Create the resource collection
            response = self._put_data(URL, data="", options=opts)

            if response.status_code == 200 :
                msg = '[Info] Resource collection "%s" successfully created' %label
                log.info(msg)

        #Verify it was created and get the xnat_abstractresource_id
        resources_set = self.get_resources(entity_type, entity_name)
        matched_res = [resources_set[current_resource] for current_resource in resources_set if resources_set[current_resource]['label'] == label]
        assert(len(matched_res) == 1)

        return matched_res[0]['xnat_abstractresource_id']


    def add_resource_file(self, entity_type, entity_name, resource_filepath,
            resource_collection=None, meta_rFormat=None, meta_rContent=None,
            extract_dir=False):
        '''Upload an entity-related file resource, understanding a entity as an
        element of the set {project,subject,experiment}.
        If 'resource_collection' is not specified, XNAT will create a 'NO LABEL' one
         or use an already existing one. Field 'resource_collection' accepts both a
        label or a unique id (xnat_abstractresource_id).
        If meta-information attribute meta_rFormat is not set, function will attempt
         to pull it out from the filename by isolating the file extension.
        Returns an HTTP response object'''

        #Compose the root URL for the REST call
        root_entity_URL = self.host + '/data/%s/%s' %(entity_type,entity_name)
        if resource_collection :
            root_entity_URL += '/resources/%s' %resource_collection

        #Check if root entity exists
        if not self.resource_exist(root_entity_URL):
            raise xnat.XNATException('Resource %s is not reachable' %root_entity_URL )

        if not op.exists(resource_filepath) :
            raise ValueError('"%s" is not a valid path in the file system' %resource_filepath )
        if not op.isfile(resource_filepath) :
            raise ValueError('"%s" is not a file' %resource_filepath )

        resource_basename = op.basename(resource_filepath)
        _,resource_extension = op.splitext(resource_basename)
        resource_extension = resource_extension[1:]
        resource_basename = utils.normalize_name(resource_basename)

        URL = root_entity_URL + '/files/%s' %resource_basename

        #Check if resource file already exists or there's an Internal Server Error
        #(subjects REST API inconsistency)
        if self.resource_exist(URL):
            msg = 'A %s-based Resource file with such name (%s) already exists in '\
                'the current context' %(entity_type,resource_basename)
            raise xnat.XNATException(msg)
        #Otherwise, lets upload it!

        #If present, encode metainformation attributes (i.e. Resource Collection
        #format and content) for the HTTP PUT request
        opts = None
        opts_dict = {}
        if meta_rFormat :
            opts_dict.update({'format': meta_rFormat.upper()})
        elif resource_extension and not extract_dir :
            opts_dict.update({'format': resource_extension.upper()})
        if meta_rContent :
            opts_dict.update({'content': meta_rContent})
        if extract_dir :
            opts_dict.update({'extract': 'true'})

        if opts_dict :
            opts = urllib.urlencode(opts_dict)

        response = self._put_file(URL, resource_filepath, opts)

        if response.status_code == 200 :
            msg = '[Info] Resource "%s" successfully uploaded' %resource_basename
            log.info(msg)

        return response


    def get_resources(self, entity_type, entity_name):
        '''Helper: Query for resource collections given an entity'''
        '''Returns a dictionary with all resource collections found'''

        #compose the URL for the REST call
        URL = self.host + '/data/%s/%s/resources' %(entity_type, entity_name)

        resultSet = self._query_data(URL)

        #parse the results out
        resourceDict = {}
        for record in resultSet :
            resourceDict[record['xnat_abstractresource_id']] = record

        return resourceDict


    def get_scan_resources(self, experimentID, scanID='ALL', options=None):
        '''Query XNAT for a list of Scan(s) Resources of a given ImageSession
        :param experimentID: XNAT ID of the experiment to list data from
        :param scanID: Specific scan to list resources from
        :param options: dictionary with options
        :return: A resourceID-keyed dictionary containing scan resources info
        '''

        URI = self.host + '/data/experiments/%s/scans/%s/resources' %(experimentID,scanID)

        if not options:
            options = {}

        rlist = self._query_data(URI, options)

        # parse the results
        scan_resources = {}
        for resource in rlist:
            #scan_resources[(resource['cat_id'],resource['label'])] = resource
            scan_resources[resource['xnat_abstractresource_id']] = resource

        return scan_resources


    def get_experiment_resources(self, experimentID, options=None):
        '''Query XNAT for a list of Resources of a given Experiment
        :param experimentID: XNAT ID of the experiment to list resources from
        :param options: dictionary with options
        :return: A resourceID-keyed dictionary containing scan resources info
        '''

        URI = self.host + '/data/experiments/%s/resources' %(experimentID)

        if not options:
            options = {}

        rlist = self._query_data(URI, options)

        # parse the results
        resources = {}
        for resource in rlist:
            resources[resource['xnat_abstractresource_id']] = resource

        return resources


    def get_scan_resource_files(self, experimentID, scanID, resourceID=None, options=None):
        '''Query XNAT for a list of Scan resource files of a given ImageSession
        :param experimentID: XNAT ID of the experiment to list resource files from
        :param scanID: Specific scan(s) to list files from (multiple scanIDs as comma-seppareted values accepted)
        :param resourceID: Specific resource collection to list files from (optional)
        :param options: dictionary with options
        :return: A URI-keyed dictionary containing scan resources info
        '''

        if resourceID :
            URI = self.host + '/data/experiments/%s/scans/%s/resources/%s/files' % (experimentID, scanID, resourceID)
        else :
            URI = self.host + '/data/experiments/%s/scans/%s/files' % (experimentID, scanID)

        if not options:
            options = {}

        flist = self._query_data(URI, options)

        # parse the results
        resource_files = {}
        for f in flist:
            resource_files[f['URI']] = f

        return resource_files


    def get_experiment_resource_files(self, experimentID, resourceID=None, options=None):
        '''Query XNAT for a list of Experiment resource files
        :param experimentID: XNAT ID of the experiment to list resource files from
        :param options: dictionary with options
        :param resourceID: Specific resource collection to list files from (optional)
        :return: A URI-keyed dictionary containing scan resources info
        '''

        if resourceID :
            URI = self.host + '/data/experiments/%s/resources/%s/files' % (experimentID, resourceID)
        else :
            URI = self.host + '/data/experiments/%s/files' % (experimentID)

        if not options:
            options = {}

        flist = self._query_data(URI, options)

        # parse the results
        resource_files = {}
        for f in flist:
            resource_files[f['URI']] = f

        return resource_files


    def download_resource(self, URI, options=None):
        '''
        Retrieves resource from XNAT (GET action) as stream
        :param URI: XNAT resource URI
        :param options: dictionary with query options and flags
        :return: Raw data structure object (string formatted data chunk)
        '''
        import requests
        import os
        response = requests.get(URI,
                                stream=True,
                                params=options,
                                cookies=self.jsession_id,
                                verify=self.verified_SSL_context,
                                timeout=100
                                )

        if response.status_code != requests.codes.ok:
            raise xnat.XNATException('HTTP response: #%s%s%s' % (response.status_code, os.linesep, response.content))

        return response.content


    def delete_resource(self, URI, options=None):
        '''
        Deletes an XNAT entity (DELETE action)
        :param URI: XNAT resource URI
        :return: An HTTP response object
        '''
        import requests
        import os

        if not options :
            options = {}
        options['removeFiles'] = 'true'

        response = requests.delete(URI,
                                   params=options,
                                   cookies=self.jsession_id,
                                   verify=self.verified_SSL_context,
                                   timeout=100
                                   )
        if response.status_code != requests.codes.ok:
            raise xnat.XNATException('HTTP response: #%s%s%s' % (response.status_code, os.linesep, response.content))

        self.log.info('Resource (%s) deleted' % self.host)

        return response
