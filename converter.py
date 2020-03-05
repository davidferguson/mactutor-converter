# -*- coding: utf-8 -*-

# this needs to be running in the virtualenv that lektor uses, in order to
# access lektor.metaformat
# however this also needs the 'regex' module, to support non-fixed-width regex
# lookbehinds. Therefore, 'regex' needs to be temporarily installed in lektor's
# virtualenv for this script to work

import glob
import os
import json
import re

import lektor.metaformat

import biographyparser
import placesparser
import extrasparser
import historytopicsparser
import honoursparser
import societiesparser
import quotationsparser
import obituariesparser
import curvesparser
import emsparser
import glossaryparser
import gazplaceparser
import gazpersonparser
import icmparser
import educationparser

import datasheetparser
import htmlparser
import flow
import cleaning
import referenceparser

LEKTOR_CONTENT_PATH = '/Users/david/Documents/MacTutor/actual-work/dev/mathshistory-site/content/'


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
    base_url_context = url_context
    # get all the files that need to be processed
    path = os.path.join(input_dir, '*')
    files = glob.glob(path)

    # process all the files
    for file in files:
        # parse sections from datasheet
        datasheet = datasheetparser.parse_file(file)
        url_context = base_url_context

        # skip all datasheets that have tables
        skip = skip_fn(datasheet)
        if skip:
            continue

        if '/' in datasheet['FILENAME']:
            print('slash in filename, modifying url context', datasheet['FILENAME'])
            url_context += datasheet['FILENAME'][:datasheet['FILENAME'].rfind('/')] + '/'

        # convert the datasheet to dictionary
        data = converter.convert(datasheet, url_context)

        # special case for biographies - add in quotations
        if output_dir == 'Biographies':
            data['quotations'] = ''
            qpath = os.path.join('../datasheets/Quotations/', datasheet['FILENAME'])
            if os.path.isfile(qpath):
                print('found quotations!')
                # has quotations! convert and add them in
                qdatasheet = datasheetparser.parse_file(qpath)
                data['quotations'] = quotationsparser.convert(qdatasheet, url_context)

        # save the dictionary in lektor
        filename = os.path.join(LEKTOR_CONTENT_PATH, output_dir, datasheet['FILENAME'].replace('Obits2@', '').replace('.html', '').replace('.', ''))
        save(data, filename)
        print('processed', datasheet['FILENAME'])


def chronology_convert(input_dir, output_dir, url_context):
    # get all the files that need to be processed
    path = os.path.join(input_dir, '*')
    files = glob.glob(path)

    dates = {}

    # process all the files
    for file in files:
        # parse sections from datasheet
        datasheet = datasheetparser.parse_file(file)
        date = datasheet['DATE']

        content = htmlparser.parse(datasheet['BIG'], os.path.basename(file), paragraphs=False, url_context=url_context)
        data = {
            'about': 'yes' if datasheet['ABOUT'] != '' else 'no',
            'content': content
        }

        if date not in dates:
            dates[date] = []
        dates[date].append(data)

    # convert to nested flow
    chronology = []
    for date, events in dates.items():
        data = {
            '_model': 'chronologyyear',
            '_hidden': 'yes',
            'year': date,
            'events': flow.to_flow_block('chronology-event', events)
        }
        filename = os.path.join(LEKTOR_CONTENT_PATH, output_dir, date)
        save(data, filename)


def project_convert(input_dir, output_dir, url_context, name):
    # get all the files that need to be processed
    path = os.path.join(input_dir, '*')
    files = glob.glob(path)

    titles = {
        'Ayel': 'The French Grandes Ecoles',
        'Brunk': 'The development of Galois theory',
        'Burslem': 'Sofia Kovalevskaya',
        'Daxenberger': 'Johan de Witt - The first calculation on the valuation of life annuities',
        'Ellison': 'Sofia Kovalevskaya',
        'Johnson': 'James Clerk Maxwell - The Great Unknown',
        'MacQuarrie': 'Mathematics and Chess',
        'Pearce': 'Indian Mathematics - Redressing the balance',
        'Watson': 'Some topics in the history of mathematical education',
        'Ledermann': 'Walter Ledermann - Encounters of a Mathematician'
    }
    authors = {
        'Ayel': 'Mathieu Ayel',
        'Brunk': 'Fiona Brunk',
        'Burslem': 'Tom Burslem',
        'Daxenberger': 'Livia Daxenberger',
        'Ellison': 'Leigh Ellison',
        'Johnson': 'Kevin Johnson',
        'MacQuarrie': 'John MacQuarrie',
        'Pearce': 'Ian G Pearce',
        'Watson': 'Helen Watson',
        'Ledermann': "J J O'Connor and E F Robertson"
    }

    pages = []
    references = ''

    # process all the files
    for file in files:
        # parse sections from datasheet
        datasheet = datasheetparser.parse_file(file)
        if datasheet['NUMBER'] == 'refs' and 'REFERENCES' in datasheet:
            # this is the references, not a page
            references = referenceparser.parse_references(datasheet['REFERENCES'], file, url_context)
            references = flow.to_flow_block('reference', json.loads(references)['data'])
            continue

        pagenum = int(datasheet['NUMBER'])
        assert pagenum == len(pages)

        content = cleaning.project_cleaning(datasheet['CONTENT'])
        data = {
            '_model': 'projectpage',
            '_template': 'projectpage.html',
            'title': datasheet['TITLE'],
            'content': htmlparser.parse(content, file, paragraphs=True, url_context=url_context),
            'chapter': str(len(pages)+1)
        }
        pages.append(data)

    # main project page
    data = {
        '_model': 'project',
        '_template': 'project.html',
        'title': titles[name],
        'author': authors[name],
        'references': '' if references is None else references
    }
    filename = os.path.join(LEKTOR_CONTENT_PATH, output_dir)
    save(data, filename)

    # the chapters
    for page in pages:
        filename = os.path.join(LEKTOR_CONTENT_PATH, output_dir, 'chapter-%s' % page['chapter'])
        save(page, filename)
    print('processed', name)


if __name__ == '__main__':
    skip = lambda datasheet: False
    convert('../datasheets/Biographies', 'Biographies', skip, biographyparser, 'Biographies/')

    # countries
    for country in biographyparser.get_countries():
        filename = os.path.join(LEKTOR_CONTENT_PATH, 'Countries', country['name'])
        save(country, filename)

    skip = lambda datasheet: False
    convert('../datasheets/Places', 'Map', skip, placesparser, 'BirthplaceMaps/')

    skip = lambda datasheet: False
    convert('../datasheets/Extras', 'Extras', skip, extrasparser, 'Extras/')

    skip = lambda datasheet: False
    convert('../datasheets/HistTopics', 'HistTopics', skip, historytopicsparser, 'HistTopics/')

    skip = lambda datasheet: False
    convert('../datasheets/Honours', 'Honours', skip, honoursparser, 'Honours/')

    skip = lambda datasheet: False
    convert('../datasheets/Societies', 'Societies', skip, societiesparser, 'Societies/')

    skip = lambda datasheet: ('Obits2@' not in datasheet['FILENAME'])
    convert('../datasheets/Obits', 'Obituaries', skip, obituariesparser, 'Obits2/')

    skip = lambda datasheet: False
    convert('../datasheets/Curves', 'Curves', skip, curvesparser, 'Curves/')

    skip = lambda datasheet: False
    convert('../datasheets/EMS', 'EMS', skip, emsparser, 'ems/')

    skip = lambda datasheet: ('Zagier/' not in datasheet['FILENAME'])
    convert('../datasheets/EMS', 'EMS', skip, emsparser, 'ems/Zagier/')

    skip = lambda datasheet: False
    convert('../datasheets/Glossary', 'Glossary', skip, glossaryparser, 'Glossary/')

    files_to_process = ['Strick/', 'Tait/', 'Wallace/', 'Wallace/butterfly', 'Curves/Definitions', 'Curves/Definitions2']
    skip = lambda datasheet: datasheet['FILENAME'] not in files_to_process and not datasheet['FILENAME'].startswith('Astronomy')
    convert('../datasheets/Files', '', skip, emsparser, '/')

    chronology_convert('../datasheets/Chronology', 'Chronology', 'Chronology/')

    # special case for Ledermann
    project_convert('../datasheets/Projects/Ledermann/', 'Ledermann', 'Ledermann/', 'Ledermann')

    projects = ['Ayel','Brunk','Burslem','Daxenberger','Ellison','Johnson','MacQuarrie','Pearce','Watson']
    for project in projects:
        project_convert('../datasheets/Projects/%s/' % project, 'Projects/%s' % project, 'Projects/%s/Chapters/' % project, project)

    skip = lambda datasheet: False
    convert('../datasheets/GazData', 'Gaz', skip, gazplaceparser, 'Gaz/')

    skip = lambda datasheet: False
    convert('../datasheets/GazData2', 'Gaz', skip, gazpersonparser, 'Gaz/')

    skip = lambda datasheet: datasheet['FILENAME'] == 'index'
    convert('../datasheets/ICMData', 'ICM', skip, icmparser, 'ICM/')

    skip = lambda datasheet: datasheet['FILENAME'] == 'index'
    convert('../datasheets/EducationData', 'Education', skip, educationparser, 'Education/')
