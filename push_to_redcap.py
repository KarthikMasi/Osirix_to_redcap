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
    try:
        xl_file = open(filepath,"r")
        return xl_file
    except:
        LOGGER.error("Check path and permissions of file:"+filepath)
        sys.exit(1)

def redcap_project_access(API_KEY):
    """
    Returns the redcap project object
    """
    try:
        project = redcap.Project('https://redcap.vanderbilt.edu/api/',API_KEY)
    except:
        LOGGER.error('ERROR: Could not access redcap. Either wrong API_URL/API_KEY or redcap down.')
    return project
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
    #record_id = png_path.split('/')[-1].split('.')[0]
    for line in lines_for_upload:
        records = line.split(',')
        redcap_dict = {unicode(redcap_variables[0], "utf-8"):records[2],\
          redcap_variables[1]:records[0],redcap_variables[2]:records[1],\
          redcap_variables[3]:records[2],redcap_variables[4]:records[3],\
          redcap_variables[5]:records[4],redcap_variables[6]:records[5],\
          redcap_variables[7]:records[6],redcap_variables[8]:records[7],\
          redcap_variables[9]:records[8],redcap_variables[10]:records[9],\
    redcap_variables[11]:records[10],redcap_variables[12]:records[11],\
          redcap_variables[13]:records[12],'abdominal_area_analysis_complete':2
                }
        redcap_upload_list.append(redcap_dict)
    return redcap_upload_list

def push_to_redcap(redcap_list,csv_file,png_file,project,OPTIONS,record_id):
    """
    """
    try:
        log_var = project.import_records(redcap_list, overwrite='normal',\
                                return_format='json', date_format='MDY')
        LOGGER.info("Records Upload COMPLETE! " + OPTIONS.path)
        response_csv = project.import_file(record_id,'csv_file',csv_file,open(csv_file,"r"))
        response_png = project.import_file(record_id,'png_file',png_file,open(png_file,"r"))
        LOGGER.info("Files uploaded to record: " + record_id)
    except (redcap.RedcapError, ValueError) as redcaperror:
        LOGGER.error(str(redcaperror))
        LOGGER.error(OPTIONS.path)
        sys.exit(1)

def add_to_parser():
    """
	Method to add arguments to default parser
	:return: parser object
	"""
    parser = argparse.ArgumentParser(description='Crontabs manager')

    parser.add_argument("-k","--key",dest='API_KEY',default=None, required=True,help='API key to REDCap Database')
    parser.add_argument("-p","--path",dest='path',default=None, required=True,help = 'path of directory containing files that need to be uploaded')
    parser.add_argument("-l","--logfile",dest='log',default=None, required=True,help='Log file path and name')
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
    upload_data = link_csv_to_redcap_variables(csv_file,png_file,project)
    push_to_redcap(upload_data,csv_file,png_file,project,OPTIONS,png_file.split('/')[-1].split('.')[0])

if __name__ == '__main__':
    execute()
