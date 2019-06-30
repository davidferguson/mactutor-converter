# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import lektor.metaformat

import biographyparser
import datasheetparser

LEKTOR_CONTENT_PATH = '/Users/david/Documents/MacTutor/actual-work/lektor/mactutor/content/'

def save(data, fs_path):
    # transorm data from key-values to list of tuples
    items = list(data.items())
    lektordata = lektor.metaformat.serialize(items)

    # make the directory if it doesn't already exist
    if not os.path.exists(fs_path):
        os.mkdir(fs_path)

    contents_file = os.path.join(fs_path, 'contents.lr')
    with open(contents_file, 'wb') as f:
            for chunk in lektor.metaformat.serialize(items, encoding='utf-8'):
                f.write(chunk)


def convert_biographies():
    INPUT_DIR = '../Datasheets' # where the datasheets are
    OUTPUT_DIR = 'biographies' # where the lektor content files are saved

    # get all the files that need to be processed
    path = os.path.join(INPUT_DIR, '*')
    files = glob.glob(path)

    # process all the files
    for file in files:
        # skip these becuase they have tables
        if file == '../Datasheets/Bhaskara_I' or file == '../Datasheets/Franklin_Benjamin' or file == '../Datasheets/Terrot':
            continue

        # parse sections from datasheet
        datasheet = datasheetparser.parse_file(file)

        # convert the datasheet to dictionary
        data = biographyparser.convert(datasheet)

        # save the dictionary in lektor
        filename = os.path.join(LEKTOR_CONTENT_PATH, OUTPUT_DIR, datasheet['FILENAME'])
        save(data, filename)
        print('processed', datasheet['FILENAME'])

if __name__ == '__main__':
    convert_biographies()
