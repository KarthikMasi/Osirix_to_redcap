#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redcap
import os
import sys
import argparse
import logging as LOGGER
import re
import csv

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
        sys.exit(1)
    return project

def open_file(filepath):
    """ 
    Opens file and returns the file object ready to be read.
    :param filepath:string of path
    :return: file object
    """
    try:
        for file in os.listdir(filepath):
            if file.endswith(".csv"):
                xl_file = open(filepath+file,"r")
                return xl_file,file.split(".csv")[0].split("Masala")[1]
    except:
        LOGGER.error("Check path and permissions of file:"+filepath+file)
        sys.exit(1)

def open_image(filepath):
    """
    Returns name of jpg file in directory
    :param filepath: string of path
    return: image filepath as string
    """
    try:
        for file in os.listdir(filepath):
            if file.endswith(".jpg"):
                return filepath+file
    except:
        LOGGER.error("Check path and permissions of file:"+filepath+file)
        sys.exit(1)

def csv_to_dict(csv_file):
    """
    Opens file and returns the file object ready to be read.
    :param filepath:string of path to file
    :return: file object
    """
    redcap_dict = {}
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    for line in csv_reader:
        line_number = int(csv_reader.line_num)-1
        redcap_dict.update({("img_no_"+str(line_number),line[0]), \
           ("roi_no_"+str(line_number),line[1]),("roi_mean_"+str(line_number),line[2]),\
           ("roi_min_"+str(line_number),line[3]),("roi_max_"+str(line_number),line[4]),\
           ("roi_total_"+str(line_number),line[5]),("roi_dev_"+str(line_number),line[6]),\
           ("roi_name_"+str(line_number),line[7]),\
           ("roi_center_x_"+str(line_number),line[8]),\
           ("roi_center_y_"+str(line_number),line[9]),\
           ("roi_center_z_"+str(line_number),line[10]),\
           ("roi_dia_cm_"+str(line_number),line[11]),\
           ("length_cm_"+str(line_number),line[12]),\
           ("length_pix_"+str(line_number),line[13]),\
           ("area_pix_"+str(line_number),line[14]),\
           ("area_cm2_"+str(line_number),line[15]),\
           ("num_of_points_"+str(line_number),line[16]),\
           })
    redcap_dict.update({("record_id","20590-4716-CPR_LAD_3ROI")})
    redcap_dict.update({('masala_image_and_data_complete',u'2')})
    redcap_upload_ready_array=[redcap_dict] 
    return redcap_upload_ready_array
    
def add_to_parser():
    """ 
    Method to add arguments to default parser
    :return: parser object
    """
    parser = argparse.ArgumentParser(description='Crontabs manager')
    parser.add_argument("-k","--key",dest='API_KEY',default=None, required=True,\
                        help='API key to REDCap Database')
    parser.add_argument("-f","--file",dest='path',default=None, required=True,\
                        help = 'path of file that needs to be uploaded')
    parser.add_argument("-l","--logfile",dest='log',default=None, required=True,\
                        help='Log file path and name')
    return parser

def execute():
    """ 
    point of execution
    """
    parser = add_to_parser()
    OPTIONS = parser.parse_args()
    LOGGER.basicConfig(filename = OPTIONS.log,level=LOGGER.DEBUG,\
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',\
                       datefmt='%Y-%m-%d %H:%M:%S')
    console = LOGGER.StreamHandler()
    console.setLevel(LOGGER.INFO)
    project = redcap_project_access(OPTIONS.API_KEY)
    csv,record_name = open_file(OPTIONS.path)
    redcap_record = csv_to_dict(csv)
    image_file_name = open_image(OPTIONS.path)
    print(OPTIONS.path)
    csv_file_name = ""+OPTIONS.path+"Masala"+record_name+".csv"
    print(csv_file_name,record_name)
    project.import_records(redcap_record,overwrite='normal',return_format='json')
    project.import_file(record_name,'csv',csv_file_name, \
                         open(csv_file_name,"r"))
    project.import_file(record_name,'image',image_file_name,\
                        open(image_file_name,"r"))

if __name__ == '__main__':
    execute()

