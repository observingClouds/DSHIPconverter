"""
Script to convert DSHIP data to netCDF
"""

import sys, os
import glob
import argparse
import logging
import subprocess as sp
import time
import numpy as np
import pandas as pd

curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)
from _helpers_dship import *


def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-o', '--outputfile', metavar="/path/to/outputfile.nc",
                        required=True, help='Provide filename of output.')
    parser.add_argument('-i', '--inputfilefmt', metavar="/path/to/DSHIP/txt/files",
                        help='Provide the DSHIP files or its file format', required=True)
    parser.add_argument('-m', '--metadatafile', metavar="metadata.json",
                        help='Provide the location of the metadata JSON file', required=False,
                        default=curr_dir+'/metadata_DSHIP.json')
    parser.add_argument('-v', '--verbose', metavar="DEBUG",
                        help='Set the level of verbosity [DEBUG, INFO,'
                             ' WARNING, ERROR]',
                        required=False, default="INFO")

    args = vars(parser.parse_args())

    return args


def setup_logging(verbose):
    assert verbose in ["DEBUG", "INFO", "WARNING", "ERROR"]
    logging.basicConfig(
        level=logging.getLevelName(verbose),
        format="%(levelname)s - %(name)s - %(funcName)s - %(message)s",
        handlers=[
            logging.FileHandler("{}.log".format(__file__)),
            logging.StreamHandler()
        ])


def main():
    args = get_args()
    setup_logging(args['verbose'])

    logging.debug('Gathering version information')
    try:
        import dshipconverter as DSHIPconverter
        __version__ = DSHIPconverter.__version__
        package_version_set = True
    except (ModuleNotFoundError, AttributeError):
        logging.debug('No DSHIPconverter package version found')
        __version__ = 'see git_version'
        package_version_set = False

    try:
        git_module_version = sp.check_output(
            ["git", "describe", "--always", "--dirty"], stderr=sp.STDOUT).strip().decode()
        git_version_set = True
    except sp.CalledProcessError:
        logging.debug('No git-version could be found.')
        git_module_version = "--"
        git_version_set = False

    if (not git_version_set and not package_version_set):
        logging.warning('No version of the converter could be found!'
                        ' Please consider the installation via conda'
                        ' or if this is not working clone the git re'
                        'pository')

    logging.info('Version of script: {} (conda package), {} (git version)'.format(__version__, git_module_version))

    DSHIP_path_in = args['inputfilefmt']
    DSHIP_nc_out = args['outputfile']
    DSHIP_metadata = args['metadatafile']

    # Gather files
    logging.info('Gather files')
    files = sorted(glob.glob(DSHIP_path_in))
    logging.debug('Files found: {}'.format(files))

    # Read and convert files
    logging.info('Read DSHIP data')
    df_DSHIP = read_dship(files)

    # Gather global attributes
    global_attr = {}
    global_attr['source'] = files
    global_attr['git_version'] = git_module_version
    global_attr['created_with'] = '{file} with its last modifications on {time}'. \
        format(time=time.ctime(os.path.getmtime(os.path.realpath(__file__))),
               file=os.path.basename(__file__))
    global_attr['created_on'] = str(time.ctime(time.time()))
    global_attr['python_version'] = "{} (DSHIPconverter:{})". \
        format(sys.version, __version__)
    global_attr['Conventions'] = 'CF-1.7'
    global_attr['featureType'] = "trajectory"

    # Export converted files to netCDF
    logging.info('Export to netCDF')
    export_dship(df_DSHIP, DSHIP_nc_out, DSHIP_metadata, global_attr)
    logging.info('Output written to {}'.format(DSHIP_nc_out))


if __name__ == "__main__":
    main()
