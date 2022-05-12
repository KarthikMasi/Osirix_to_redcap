#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redcap
import os
import sys 
import argparse
import logging as LOGGER
import glob

redcap_variables=['record_id','username','current_date','id','studyid',\
 'slice_thickness','muscle_area_surf','imat_area_surf','vat_area_surf',\
 'sat_area_surf','muscle_mean','imat_mean','vat_mean','sat_mean']

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

def link_csv_to_redcap_variables(csv_path,png_path,project):
    """
    """
    try:
        csv_file = open(csv_path,"r")
    except:
        LOGGER.error("Check path and permissions of file:" + csv_path)
    redcap_upload_list=[]
    all_lines = csv_file.read().splitlines()
    lines_for_upload = all_lines[3:] #Removing the headers
    record_id = png_path.spit('/')[-1].split('.')[0] 
    for line in all_lines:
        records = line.split(',')
        redcap_dict = {redcap_variables[0]:record_id,\
          redcap_variables[1]:records[0],redcap_variables[2]:records[1],\
          redcap_variables[3]:records[2],redcap_variables[4]:records[3],\
          redcap_variables[5]:records[4],redcap_variables[6]:records[5],\
          redcap_variables[7]:records[6],redcap_variables[8]:records[7],\
          redcap_variables[9]:records[8],redcap_variables[10]:records[9],\
          redcap_variables[11]:records[10],redcap_variables[12]:records[11],\
          redcap_variables[13]:records[12]
                }
        redcap_update_list.append(redcap_dict)
    return redcap_upload_list

def push_to_redcap(redcap_list,project):

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
    parser = add_to_parser()
    OPTIONS = parser.parse_args()
    LOGGER.basicConfig(filename=OPTIONS.log, level=LOGGER.DEBUG,\
           format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',\
           datefmt='%Y-%m-%d %H:%M:%S')
    console = LOGGER.StreamHandler()
    console.setLevel(LOGGER.INFO)
    project = redcap_project_access(OPTIONS.API_KEY)
    csv_file = glob.glob(OPTIONS.path+"/*.csv")[0]
    png_file = glob.glob(OPTIONS.path+"/*.png")[0]

if __name__ == '__main__':
    execute()
