#!/usr/bin/env python
# -*- coding: utf-8 -*-


import redcap
import os
import sys
import argpars
import logging as LOGGER
import re

def execute():
    """
    point of execution
    """
    parser = add_to_parser()
    OPTIONS = parser.parse_args()


if __name == '__main__':
    execute()

