#!python

import argparse
from bxl import utils
import logging as log
log.basicConfig(level=log.INFO)
import json
import os
import tempfile
from argparse import RawTextHelpFormatter

def main(args, dontdoit=False):

    c1 = utils.setup_xnat(args['source_config'])
    c2 = utils.setup_xnat(args['dest_config'])

    # download session from source XNAT
    uri = c1.host + '/data/experiments/' + args['experiment_id'] + \
        '/scans/ALL/files?format=zip'

    fd1, path = tempfile.mkstemp(suffix='.zip')

    log.info('Downloading session %s from %s at %s'\
        %(args['experiment_id'], c1.host, path))
    if not dontdoit:
        with open(path, 'wb') as tmp:
            response = c1._get_raw_data(uri)
            tmp.write(response)
    log.info('Download complete')

    # import session to destination XNAT
    uri = c2.host + '/data/services/import?format=html'
    dest_config = json.load(open(args['dest_config']))
    fd2, logfp = tempfile.mkstemp(suffix='.log')

    cmd = 'curl -u %s:%s -k -o %s -w "%%{http_code}" '\
        ' --form project=%s --form image_archive=@%s %s'\
        %(dest_config['user'], dest_config['password'], logfp,
        args['project_id'], path, uri)
    msg = 'Importing session to %s from archive %s (project %s)'\
        %(c2.host, path, args['project_id'])
    log.info(msg)
    if not dontdoit:
        os.system(cmd)
        os.close(fd1)
        os.close(fd2)
        os.remove(path)
        log.info('Log saved at %s'%logfp)


if __name__=="__main__" :
    parser = argparse.ArgumentParser(description='Downloads a given experiment/'\
        'session from an XNAT instance and uploads it to an independent one. '\
        'Only DICOM resources will be imported. \n\n'\
        'More information at: https://wiki.xnat.org/docs16/4-developer-documen'\
        'tation/xnat-rest-api-directory/data-services-import',
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('--h1', '--source_config', dest='source_config',
        help='Source XNAT configuration file', required=True)
    parser.add_argument('--h2', '--dest_config', dest='dest_config',
        help='Destination XNAT configuration file', required=True)
    parser.add_argument('-e','--experiment_id',
        help='Which resource to download? (Entity name/identifier)', required=True)
    parser.add_argument('-p','--project_id', dest='project_id',
        help='Which project to store the resource in', required=True)
    parser.add_argument('-v','--verbose', dest='verbose', action='store_true',
        default=False, help='Display verbosal information (optional)',
        required=False)

    args = vars(parser.parse_args())
    main(args)
