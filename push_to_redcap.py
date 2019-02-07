#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redcap
import os
import sys
import argparse
import logging as LOGGER
import re

def redcap_project_access(API_KEY):
    """
    Access point to REDCap form
    :param API_KEY:string with REDCap database API_KEY
    :return: redcap Project Object
    """
    try:
        project = redcap.Project('https://redcap.vanderbilt.edu/api/', API_KEY)
    except:
        raise SystemExit('ERROR: Could not access redcap. Either wrong API_URL/API_KEY or redcap down.')
    return project

def get_form_names(project):
    """
    Fetches all form objects from the REDCap project and converts unicode values 
    to string
    :param project: redcap.Project object
    :return: list containing names of forms as string
    """
    forms_unicode = project.forms
    forms_str = []
    for form in forms_unicode:
        forms_str.append(form.encode('ascii','ignore'))
    return forms_str

def open_file(filepath):
    """
    """
    try:
        xl_file = open(filepath,"r")
        LOGGER.info("Opening "+filepath)
        return xl_file
    except:
        raise SystemExit("ERROR: Check path and permissions of file you are trying to upload")

def list_data_by_line(data):
    """
    """
    lines = data.read().splitlines()
    stagnant_data = []
    table_data = []
    for line in lines:
        if ":" in line:
            stagnant_data.append(line)
        else:
            table_data.append(line)
    return table_data,stagnant_data

def table_to_dict(table_data,OPTIONS):
    """

    """
    roi_list = []
    table_values = get_values_and_variables(table_data,OPTIONS)
    return table_values

def get_values_and_variables(table_data,OPTIONS):
    """
    """
    table_values = []
    settings_dict = read_settings_file(OPTIONS)
    for line in table_data:
        if "ROI" in line or "VOI" in line:
            headers = line
            headers = re.split(r'\t+',headers)
        elif line!='':
            line = re.split(r'\t+',line)
            dictionary = dict(zip(headers,line))
            for key in dictionary.keys():
                if key in settings_dict.keys():
                    table_values.append(dictionary.get('ROI_Name')+"_"+ \
                               settings_dict.get(key)+" : "+dictionary.get(key))
    return table_values

def update_redcap(table_values,settings_dict,project):
    """
    """
#    for pair in table_values:


def read_settings_file(OPTIONS):
    """
    """
    settings = open_file(OPTIONS.settings)
    settings_file = settings.read()
    data_var,redcap_var = [],[]
    for line in settings_file.splitlines():
        if line!='':
            data_var.append(re.split(r'=+',line)[0])
            redcap_var.append(re.split(r'=+',line)[1])
    var_dict = dict(zip(data_var,redcap_var))
    return var_dict


def add_to_parser():
    """
    Method to add arguments to default parser
    :return: parser object
    """
    parser = argparse.ArgumentParser(description='Crontabs manager')
    parser.add_argument("-k","--key",dest='API_KEY',default=None, \
                        help='API key to REDCap Database')
    parser.add_argument("-f","--file",dest='path',default=None, \
                        help = 'path of file that needs to be uploaded')
    parser.add_argument("-s","--study",dest='form',default=None,\
                        help='Name of study on redcap. Replace spaces with _')
    parser.add_argument("-i","--settings",dest='settings',default=None,\
                        help='path to settings file of the study')
    return parser

def execute():
    """
    point of execution
    """
    LOGGER.basicConfig(level=LOGGER.DEBUG,\
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',\
                       datefmt='%Y-%m-%d %H:%M:%S')
    console = LOGGER.StreamHandler()
    console.setLevel(LOGGER.INFO)
    parser = add_to_parser()
    OPTIONS = parser.parse_args()
    project = redcap_project_access(OPTIONS.API_KEY)
    forms = get_form_names(project)
    doc = open_file(OPTIONS.path)
    table_data,stagnant_data = list_data_by_line(doc)
    formatted_table_data = table_to_dict(table_data,OPTIONS)
    upload_to_redcap(project,stagnant_data,formatted_table_data)

if __name__ == '__main__':
    execute()
