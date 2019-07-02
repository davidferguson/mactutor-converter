# -*- coding: utf-8 -*-

# main converter file, converts datasheets and extras

import glob
import os
import json
import re

import lektor.metaformat

import biographyparser
import extrasparser
import historytopicsparser
import datasheetparser

LEKTOR_CONTENT_PATH = '/Users/david/Documents/MacTutor/actual-work/lektor/mactutor/content/'


def save(data, fs_path):
    # transorm data from key-values to list of tuples
    items = list(data.items())
    lektordata = lektor.metaformat.serialize(items)

    # make the directory if it doesn't already exist
    if not os.path.exists(fs_path):
        os.makedirs(fs_path)

    contents_file = os.path.join(fs_path, 'contents.lr')
    with open(contents_file, 'wb') as f:
            for chunk in lektor.metaformat.serialize(items, encoding='utf-8'):
                f.write(chunk)


def convert(input_dir, output_dir, skip_fn, converter):
    # get all the files that need to be processed
    path = os.path.join(input_dir, '*')
    files = glob.glob(path)

    # process all the files
    for file in files:
        # parse sections from datasheet
        datasheet = datasheetparser.parse_file(file)

        # skip all datasheets that have tables
        skip = skip_fn(datasheet)
        if skip:
            continue

        # convert the datasheet to dictionary
        data = converter.convert(datasheet)

        # save the dictionary in lektor
        filename = os.path.join(LEKTOR_CONTENT_PATH, output_dir, datasheet['FILENAME'])
        save(data, filename)
        print('processed', datasheet['FILENAME'])


if __name__ == '__main__':
    skip = lambda datasheet: '<table' in datasheet['BIOGRAPHY']
    convert('../Datasheets', 'Biographies', skip, biographyparser)

    skip = lambda datasheet: '<table' in datasheet['EXTRA']
    convert('../ExtrasData', 'Extras', skip, extrasparser)

    skip = lambda datasheet: '<table' in datasheet['HISTTOPIC'] or '<area' in datasheet['HISTTOPIC']
    convert('../HistTopicsData', 'HistTopics', skip, historytopicsparser)
