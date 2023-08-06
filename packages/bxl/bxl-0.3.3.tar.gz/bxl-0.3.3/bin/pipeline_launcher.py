#! /usr/bin/env python2

import sys
import argparse
import os.path as op
import logging as log
log.basicConfig(level=log.INFO)
import bxl.utils
import bxl.xnat

def get_pipeline_alias(connexion, project_id, pipeline_id):
    ''' Get project's archive_spec metainfo from XNAT and parse the project's
    available pipeline names VERSUS stepIds. Returns a pipeline stepId
    (pipeline runnable alias) for the given pipeline identified by pipeline_name '''

    import xml.etree.ElementTree as etree

    uri = connexion.host + '/data/projects/%s/archive_spec' % project_id
    proj_archspec_xml = etree.fromstring(connexion._get_raw_data(uri))
    namespace = {'archive': 'http://nrg.wustl.edu/arc'}

    # traverse XML subelements named 'pipeline' and get pipeline name VS stepId
    # attribute. XNAT Pipeline Engine uses the later as actual names/ids for
    # launching a pipeline programatically.
    pip_list = proj_archspec_xml.findall(
        'archive:pipelines/archive:descendants/archive:descendant/archive:pipeline',
        namespace)
    pip_aliases = {(item.find('archive:name', namespace)).text: item.attrib['stepId']
                   for item in pip_list}
    return pip_aliases[pipeline_id]


def main(arguments):
    ''' Top level function '''
    if arguments.verbose :
        log.basicConfig(level=log.INFO)

    project = arguments.project
    pipeline = arguments.pipeline
    experiment = arguments.experiment
    parameters = arguments.param

    if parameters is not None:
        parameters = {}
        for p in arguments.param :
            item = p.split('=')
            parameters[item[0]] = item[1]

    credentials = None
    if args.jsession is not None:
        credentials = args.jsession
    elif args.usrpwd is not None:
        credentials = tuple(args.usrpwd.split(':'))

    if credentials :
        c = bxl.xnat.Connection(arguments.host, credentials, verbose=True)
    elif op.isfile(args.cfgfile) :
        c = bxl.utils.setup_xnat(args.cfgfile)
    else :
        log.error('Unable to connect to %s' %(arguments.host))
        sys.exit(1)

    if pipeline not in c.get_project_pipelines(project):
        log.error('Pipeline %s is not set up for %s project' % (project, pipeline))
        sys.exit(1)

    # check if pipeline has an alias ID (scheduled to run automode)
    alias = get_pipeline_alias(c, project, pipeline)
    if pipeline != alias:
        log.warning('Using pipeline `%s` alias: `%s`' % (pipeline, alias))
    c.launch_pipeline(alias, experiment, parameters)
    log.info('Pipeline `%s` launched --> %s %s' % (pipeline, experiment, parameters))

    if args.jsession is None:
        c.close_jsession()

    return


if __name__=="__main__" :

    parser = argparse.ArgumentParser(
        description='Handle pipeline execution based on pipeline dependencies status')
    parser.add_argument('--host',
                        help='XNAT hostname',
                        required=True)
    auth = parser.add_mutually_exclusive_group(required=True)
    auth.add_argument('--jsession',
                      help='XNAT jsessionid authentication token')
    auth.add_argument('--usrpwd',
                      help='XNAT user name + password string (usr:pwd)')
    auth.add_argument('--cfgfile',
                      help='XNAT configuration file')
    parser.add_argument('--project',
                        help='XNAT project identifier',
                        required=True)
    parser.add_argument('--pipeline',
                        help='XNAT (project-enabled) pipeline',
                        required=True)
    parser.add_argument('--experiment',
                        help='XNAT experiment unique identifier',
                        required=True)
    parser.add_argument('--param',
                        action='append',
                        help='Pipeline input parameter (name=value), '
                             'multiple parameter occurrences supported',
                        required=False)
                        #type=json.loads)
    parser.add_argument('-v','--verbose',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help='Display verbosal information (optional)',
                        required=False)

    args = parser.parse_args()

    # script entry point
    main(args)
    sys.exit(0)