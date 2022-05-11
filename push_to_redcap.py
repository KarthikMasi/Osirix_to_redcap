#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redcap
import os
import sys 
import argparse
import logging as LOGGER


def open_file(filepath):
	"""
    Opens file and returns the file object ready to be read.
    :param filepath:string of path to file
    :return: file object
    """
    try:
        xl_file = open(filepath,"r")
        return xl_file
    except:
        LOGGER.error("Check path and permissions of file:"+filepath)
        sys.exit(1)

def redcap_project_access(API_KEY):
	"""
    Access point to REDCap form
    :param API_KEY:string with REDCap database API_KEY
    :return: redcap Project Object
    """
    try:
        project = redcap.Project('https://redcap.vanderbilt.edu/api/', API_KEY)
    except:
        LOGGER.error('ERROR: Could not access redcap. Either wrong API_URL/API_KEY or redcap down.')

def link_csv_to_redcap_variables(table_data):

def push_to_redcap(redcap_dict):

def add_to_parser():
	"""
	Method to add arguments to default parser
	:return: parser object
	"""
	parser = argparse.ArgumentParser(description='Crontabs manager')
    parser.add_argument("-k","--key",dest='API_KEY',default=None, required=True,\
                        help='API key to REDCap Database')
    parser.add_argument("-p","--path",dest='path',default=None, required=True,\
                        help = 'path of directory containing files that need to be uploaded')
    parser.add_argument("-l","--logfile",dest='log',default=None, required=True,\
                        help='Log file path and name')
	return parser

def execute():

if __name__ == '__main__':
    execute()
