#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redcap
import os
import sys
import argparse
import logging as LOGGER



def redcap_project_access(API_KEY):
    """
    Access point to REDCap form
    :param API_KEY:string with REDCap database API_KEY
    :return: redcap Project Object
    """
    try:
        project = redcap.Project('https://redcap.vanderbilt.edu/api/', API_KEY)
    except Exception:
        raise SystemExit('Could not access redcap. Either wrong API_URL/API_KEY \
                    or redcap down.')
        
    return project


def add_to_parser():
    """
    Method to add arguments to default parser
    :return: parser object
    """
    parser = argparse.ArgumentParser(description='Crontabs manager')
    parser.add_argument("-k","--key",dest='API_KEY',default=None, \
                        help='API key to REDCap Database')
    return parser

if __name__ == '__main__':
    
