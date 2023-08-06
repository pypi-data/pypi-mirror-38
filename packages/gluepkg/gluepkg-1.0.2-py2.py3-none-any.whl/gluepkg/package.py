"""
package module hosting the functionalities to package a certain directory
structure of a python into a package readily consumed for AWS Glue.
"""
import os
import sys
import zipfile
import uuid
import argparse

from urlparse import urlparse

import boto3


def zip_dir(path, ziph):
    """Zip a directory"""
    for root, _, files in os.walk(path):
        for filen in files:
            ziph.write(os.path.join(root, filen))


def zip_local(source_dir_path, zip_result_path):
    """Create a zip file at zip_result_path from a directory of source_dir_path
    """
    zipf = zipfile.ZipFile(zip_result_path, 'w', zipfile.ZIP_DEFLATED)
    zip_dir(source_dir_path, zipf)
    zipf.close()


def glue_local_packaging(source_dir_path, s3_path, zip_tmp_dir="."):
    """Package the given local directory structures and upload it into library
    folder in AWS S3. Raise exception if upload failed"""
    # create the zip file
    print "zip the directory '{}'".format(source_dir_path)
    zip_tmp_result_path = "{}/{}.zip".format(zip_tmp_dir, str(uuid.uuid4()))
    zip_local(source_dir_path, zip_tmp_result_path)

    # upload to s3
    print "upload to {}".format(s3_path)
    parsed_s3_uri = urlparse(s3_path)
    s3_resource = boto3.resource("s3")
    s3_resource.meta.client.upload_file(
        zip_tmp_result_path, parsed_s3_uri.netloc, parsed_s3_uri.path[1:])

    # clean the temporary zip file
    print "clean the temporary zip file {}".format(zip_tmp_result_path)
    os.remove(zip_tmp_result_path)
    print "DONE!"


def parse_args(args):
    """parsing arguments for cli"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--src_dir', help='the source directory path to be packaged')
    parser.add_argument(
        '--pkg_s3_path', help='s3 path where the zip packaged shall be stored')

    args = parser.parse_args(args)
    return args


def main():
    """main entry for cli"""
    args = parse_args(sys.argv[1:])
    glue_local_packaging(
        args.src_dir, args.pkg_s3_path)


if __name__ == '__main__':
    main()
