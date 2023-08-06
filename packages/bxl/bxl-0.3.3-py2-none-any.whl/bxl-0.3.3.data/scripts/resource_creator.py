#!python

import argparse
import contextlib
import tempfile
import shutil
import zipfile
import getpass
import os.path as op
import os
import sys
import traceback
import logging as log
log.basicConfig(level=log.INFO)
from bxl import resource as res
from bxl import xnat

@contextlib.contextmanager
def make_temp_directory():
    '''Helper: Automatically creates a temporary directory. The contextmanager
    decorator allows defining as factory functionself. As decorated function,
    it can be bound in a 'with' statement as clause. Exceptions from the with
    block are handled there '''

    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


def zipdir(input_dir, zip_filename):
    '''Helper: Zip-compress a whole directory'''
    '''Returns a dictionary with all resource collections found'''

    with contextlib.closing(zipfile.ZipFile(zip_filename, "w",
            zipfile.ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(input_dir):
            #NOTE: ignore empty directories
            for filename in files:
                abs_fp = op.join(root, filename)
                relative_fp = abs_fp[len(input_dir)+len(os.sep):] #relative path!
                z.write(abs_fp, relative_fp)

    return zip_filename


def main (connection, args):

    if op.isfile(args['input']):
        # case: resource file upload
        if args['resource_collection'] :
            rc_name = args['resource_collection']
        else :
            msg = '[Warning] No resource collection specified, archiving "%s" '\
                'under UNSPECIFIED resource collection' % args['input']
            log.warning(msg)
            rc_name = 'UNSPECIFIED'

        rc_id = res.create_resource_collection(connection, args['e_type'],
            args['e_name'], rc_name, force_create=False) #,meta_rcFormat=None,meta_rcContent=None)
        res.add_resource_file(connection, args['e_type'], args['e_name'],
            args['input'], str(rc_id))#,meta_rFormat=None,meta_rContent=None)

    elif op.isdir(args['input']):
        # case: directory (or set of files) batch upload
        if args['resource_collection'] :
            rc_name = args['resource_collection']
        else :
            msg = '[Warning] No resource collection specified, archiving "%s" '\
                'under its root directory name: %s' \
                %(args['input'], op.basename(args['input']))
            log.warning(msg)
            rc_name = res.normalize_name(op.basename(args['input']))

        # Force the creation of the resource collection, otherwise may be
        #reusing an existing one and resource files might be overwrote
        rc_id = res.create_resource_collection(connection, args['e_type'],
            args['e_name'], rc_name, force_create=True) #,meta_rcFormat=None,meta_rcContent=None)

        # Compress directory content
        with make_temp_directory() as temp_dir:
            # Create a temporary directory and filename
            temp_name = res.normalize_name(op.basename(args['input']))
            temp_zipfile = op.join(temp_dir,temp_name)
            # ZIP-compress all data to the temporary file
            zipdir(args['input'], temp_zipfile)
            res.add_resource_file(connection,args['e_type'], args['e_name'],
                temp_zipfile,str(rc_id),extract_dir=True) #,meta_rFormat=None,meta_rContent=None)


if __name__=="__main__" :
    print ''

    # argparse trickery
    parser = argparse.ArgumentParser(description='%s :: Create and uploads '\
        'additional resource files into XNAT' %op.basename(sys.argv[0]))
    parser.add_argument('-H','--host', dest="hostname",
        help='XNAT hostname URL (e.g. https://3tmri.nl/xnat)', required=True)
    parser.add_argument('-u','--user', dest="username",
        help='XNAT username (will be prompted for password)', required=True)
    parser.add_argument('-t','--type', dest="e_type",
        help='Entity type/level where to create resource; can either be: '\
        '{projects,subjects,experiments}', required=True)
    parser.add_argument('-id','--identifier', dest="e_name",
        help='Entity name/identifier where to create resource', required=True)
    parser.add_argument('-i','--input', dest="input",
        help='Input file/directory location', required=True)
    parser.add_argument('-rc','--resource_collection', dest="resource_collection",
        default=None, help='Resource collection name (optional)', required=False)
    parser.add_argument('-v','--verbose', dest="verbose", action='store_true',
        default=False, help='Display verbosal information (optional)',
        required=False)

    args = vars(parser.parse_args())

    # compose the HTTP basic authentication credentials string
    password = getpass.getpass('Password for user %s:' %args['username'])
    usr_pwd = args['username']+':'+password
    log.warning('')

    try:
        # connect to XNAT
        with xnat.Connection(args['hostname'],usr_pwd) as xnat_connection :
            if args['verbose'] :
                log.info('[Info] session %s opened' %xnat_connection.jsession)

            main(xnat_connection, args)

            if args['verbose'] :
                log.info('[Info] session %s closed' %xnat_connection.jsession)
            # disconnect from XNAT

    except xnat.XNATException as xnatErr:
        print '[Error] XNAT-related issue:', xnatErr
        sys.exit(1)

    except Exception as e:
        print '[Error]', e
        print(traceback.format_exc())
        sys.exit(1)

    sys.exit(0)
