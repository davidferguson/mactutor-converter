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
import honoursparser
import societiesparser
import quotationsparser
import obituariesparser
import curvesparser
import emsparser

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


def convert(input_dir, output_dir, skip_fn, converter, url_context):
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
        data = converter.convert(datasheet, url_context)

        # save the dictionary in lektor
        filename = os.path.join(LEKTOR_CONTENT_PATH, output_dir, datasheet['FILENAME'].replace('Obits2@', '').replace('.html', '').replace('.', ''))
        save(data, filename)
        print('processed', datasheet['FILENAME'])


if __name__ == '__main__':
    skip = lambda datasheet: '<table' in datasheet['BIOGRAPHY']
    convert('../datasheets/Biographies', 'Biographies', skip, biographyparser, 'Biographies/')

    # manually do the maplocations discovered from biographies
    mapdata = biographyparser.get_map_locations()
    filename = os.path.join(LEKTOR_CONTENT_PATH, 'Maplocations')
    save(mapdata, filename)

    skip = lambda datasheet: '<table' in datasheet['EXTRA']
    convert('../datasheets/Extras', 'Extras', skip, extrasparser, 'Extras/')

    skip = lambda datasheet: '<table' in datasheet['HISTTOPIC'] or '<area' in datasheet['HISTTOPIC']
    convert('../datasheets/HistTopics', 'HistTopics', skip, historytopicsparser, 'HistTopics/')

    skip = lambda datasheet: '<table' in datasheet['CONTENT'].lower() or '<area' in datasheet['CONTENT'].lower()
    convert('../datasheets/Honours', 'Honours', skip, honoursparser, 'Honours/')

    skip = lambda datasheet: '<table' in datasheet['CONTENT'].lower() or '<area' in datasheet['CONTENT'].lower()
    convert('../datasheets/Societies', 'Societies', skip, societiesparser, 'Societies/')

    skip = lambda datasheet: '<table' in datasheet['CONTENT'].lower() or '<area' in datasheet['CONTENT'].lower()
    convert('../datasheets/Quotations', 'Quotations', skip, quotationsparser, 'Quotations/')

    skip = lambda datasheet: ('Obits2@' not in datasheet['FILENAME']) or '<table' in datasheet['CONTENT'].lower() or '<area' in datasheet['CONTENT'].lower()
    convert('../datasheets/Obits', 'Obituaries', skip, obituariesparser, 'Obits2/')

    skip = lambda datasheet: '<table' in datasheet['CONTENTS'].lower() or '<area' in datasheet['CONTENTS'].lower()
    convert('../datasheets/Curves', 'Curves', skip, curvesparser, 'Curves/')

    skip = lambda datasheet: datasheet['FILENAME'] == 'EMS_poster' or ('Zagier/' in datasheet['FILENAME']) or '<table' in datasheet['CONTENT'].lower() or '<area' in datasheet['CONTENT'].lower()
    convert('../datasheets/EMS', 'EMS', skip, emsparser, 'EMS/')

    skip = lambda datasheet: ('Zagier/' not in datasheet['FILENAME']) or '<table' in datasheet['CONTENT'].lower() or '<area' in datasheet['CONTENT'].lower()
    convert('../datasheets/EMS', 'EMS', skip, emsparser, 'EMS/Zagier/')
