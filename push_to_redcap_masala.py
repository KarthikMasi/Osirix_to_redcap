#!/usr/bin/env python
# -*- coding: utf-8 -*-


import redcap
import os
import sys
import argpars
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
        LOGGER.error('ERROR: Could not access redcap. Either wrong API_URL/API_KEY or redcap down.')
        sys.exit(1)
    return project



def execute():
    """
    point of execution
    """
    parser = add_to_parser()
    OPTIONS = parser.parse_args()


if __name == '__main__':
    execute()

