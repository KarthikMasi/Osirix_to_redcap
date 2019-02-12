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
    Opens file and returns the file object ready to be read.
    :param filepath:string of path to file
    :return: file object
    """
    try:
        xl_file = open(filepath,"r")
        return xl_file
    except:
        raise SystemExit("ERROR: Check path and permissions of file:"+filepath)

def list_data_by_line(data):
    """
    Splits the stagnant and table data and returns a tuple
    :param data:file object containing all the values from the spreadsheet
    :return: tuple(list,list) table_data and stagnant_data
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
    :param table_data:values from the spreadsheet that are 
                    in a table like a 2 dimensional array
    :param OPTIONS:parsed arguments from the user
    :return: dict
    """
    table_values = get_values_and_variables(table_data,OPTIONS)
    return table_values

def get_values_and_variables(table_data,OPTIONS):
    """
    Separates the headers and values from table_data.
    Reads the settings file and fetches the variable names and 
    makes a dictionary with redcap field variable names and corresponding values 
    from the table data
    :param table_data: passed from table_to_dict method
    :param OPTIONS: parsed arguments form terminal
    :return:dict of redcap ready values and keys of table data
    """
    table_values = []
    table_dict = {}
    settings_dict = read_settings_file(OPTIONS)
    for line in table_data:
        if "ROI" in line or "VOI" in line:
            headers = line
            headers = re.split(r'\t+',headers)
        elif line!='':
            line = re.split(r'\t+',line)
            try:
                dictionary = dict(zip(headers,line))
            except UnboundLocalError:
                LOGGER.error("The xls file corrupted "+ OPTIONS.path)
                raise SystemExit("Soft Exit")
            for key in dictionary.keys():
                if dictionary.has_key('ROI_Name'):
                    roi_key='ROI_Name'
                elif dictionary.has_key('VOI_Name'):
                    roi_key='VOI_Name'
                if key in settings_dict.keys():
                    redcap_field_name = (dictionary.get(roi_key)+"_"+ \
                         settings_dict.get(key)).replace(" ","_")
                    table_dict.update({(redcap_field_name,dictionary.get(key))})
    return table_dict

def format_stagnant_data(stagnant_data,settings_file):
    """
    Takes the stagnant data, refers the settings file and
    gets the stagnant data in a dictionary with redcap field variable
    names as keys.
    :param stagnant_data:list where each element is a line from the stagnant section
                            of the spreadsheet
    :param settings_file:file object of settings file referenced by user
    :return: dict of redcap ready values and keys of stagnant data
    """
    lines = {}
    for line in stagnant_data:
        if line!='':
            line_key = re.split(r":+",line)[0].strip()
            if line_key in settings_file.keys():
                lines.update({(settings_file.get(line_key), \
                  re.split(r":+",line)[1].strip())})
            if line_key=="Patient ID":
                lines.update({("record_id",re.split(r":+",line)[1].strip())})
                print settings_file.get('COMPLETE')
                lines.update({(settings_file.get('COMPLETE'),u'2')})
    return lines


def upload_to_redcap(project,stagnant_data,formatted_data,OPTIONS):
    """
    Concatenates stagnant and table data in a dictionary. Adds dict to a list 
    where multiple records may exist. Pushes the list to redcap
    :param project:redcap Project
    :param stagnant_data:list of stagnant data
    :param formatted_data:dict of table data
    :param OPTIONS: parsed arguments from user
    :return:returns the count after attempting to import data to redcap project
    """
    redcap_dict = format_stagnant_data(stagnant_data,\
         settings_file = read_settings_file(OPTIONS))
    redcap_dict.update(formatted_data)
    records = [redcap_dict]
    try:
        log_var= project.import_records(records,overwrite='normal' \
                                    ,return_format='json',date_format='MDY')
        LOGGER.info("Upload COMPLETE! "+OPTIONS.path)
    except redcap.RedcapError as redcaperror:
        raise SystemExit(redcaperror)
    return log_var

def read_settings_file(OPTIONS):
    """
    Reads settings file and returns a dict with replacement pairs
    from the settings file
    :param OPTIONS: arguments parsed from user input
    :return: dict with settings file data
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
    parser.add_argument("-s","--settings",dest='settings',default=None,\
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
    log=upload_to_redcap(project,stagnant_data,formatted_table_data,OPTIONS)

if __name__ == '__main__':
    execute()
