# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os

import datasheetparser

FILEPATH = '../Datasheets'

# get all the files that need to be processed
path = os.path.join(FILEPATH, '*')
files = glob.glob(path)


# process all the files
for file in files:
    # parse sections from datasheet
    datasheet = datasheetparser.parse_file(file)
    print(datasheet['FULLNAME'])
