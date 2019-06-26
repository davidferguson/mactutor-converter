# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import lektor.metaformat

import datasheetparser
import biographyparser
import referenceparser

FILEPATH = '../Datasheets'


def convert(datasheet):
    data = {}

    # metadata, the template and model
    data['_model'] = 'biography'
    data['_template'] = 'biography.html'

    # filename for this
    data['filename'] = datasheet['FILENAME']

    # name and shortname
    data['shortname'] = datasheet['SHORTNAME']
    data['fullname'] = datasheet['FULLNAME']

    # authors
    data['authors'] = datasheet['AUTHORS']

    data['summary'] = datasheet['SUMMARY']

    # dates are tricky. for now leave them as they are
    data['birthdate'] = datasheet['BIRTHDATE']
    data['birthyear'] = datasheet['BIRTHYEAR']
    data['deathdate'] = datasheet['DEATHDATE']
    data['deathyear'] = datasheet['DEATHYEAR']

    # birthplace and mapinfo
    data['birthplace'] = datasheet['BIRTHPLACE']
    data['birthlatlong'] = re.sub(r'\d+,.+?,(-?[\d.]+),(-?[\d.]+)', r'\1,\2', datasheet['MAPINFO'])

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'], datasheet['FILENAME'])
    data['references'] = references

    # parse translations (use the same format as references)
    # don't add them to data, as we're combining them with bio
    translations = referenceparser.parse_references(datasheet['TRANSLATION'], datasheet['FILENAME'])

    # parse cross references
    #xrefs = referenceparser.parse_cross_references(datasheet['XREFS'], datasheet['FILENAME'])
    #data['xrefs'] = xrefs

    # parse additional links (they use the same format as cross references)
    # don't add them to data, as we're combining them with bio
    additional = referenceparser.parse_cross_references(datasheet['ADDITIONAL'], datasheet['FILENAME'])
    data['additional'] = additional

    # parse otherweb links (they use the same format as cross references)
    otherweb = referenceparser.parse_cross_references(datasheet['OTHERWEB'], datasheet['FILENAME'])
    data['otherweb'] = otherweb

    # parse honours links (they use the same format as cross references)
    honours = referenceparser.parse_cross_references(datasheet['HONOURS'], datasheet['FILENAME'])
    data['honours'] = honours

    # parse biography, and add in extras and translations
    bio = biographyparser.parse(datasheet['BIOGRAPHY'],
                                datasheet['FILENAME'],
                                translations=json.loads(translations)['data'],
                                extras=json.loads(additional)['data'],
                                paragraphs=True)
    data['biography'] = bio.replace('\\', '')

    return data


def save(data, fs_path):
    # transorm data from key-values to list of tuples
    items = list(data.items())
    lektordata = lektor.metaformat.serialize(items)

    #for chunk in lektor.metaformat.serialize(items, encoding='utf-8'):
    #    print(chunk.decode('utf-8'))

    # make the directory if it doesn't already exist
    if not os.path.exists(fs_path):
        os.mkdir(fs_path)

    contents_file = os.path.join(fs_path, 'contents.lr')
    #print(fs_path, contents_file)
    with open(contents_file, 'wb') as f:
            for chunk in lektor.metaformat.serialize(items, encoding='utf-8'):
                f.write(chunk)



if __name__ == '__main__':
    # get all the files that need to be processed
    path = os.path.join(FILEPATH, '*')
    files = glob.glob(path)

    # process all the files
    for file in files:
        # skip these becuase they have tables
        if file == '../Datasheets/Bhaskara_I' or file == '../Datasheets/Franklin_Benjamin' or file == '../Datasheets/Terrot':
            continue

        # parse sections from datasheet
        datasheet = datasheetparser.parse_file(file)

        # convert the datasheet to dictionary
        data = convert(datasheet)

        # save the dictionary in lektor
        basepath = '/Users/david/Documents/MacTutor/actual-work/lektor/mactutor/'
        biographydir = 'content/biographies'
        filename = os.path.join(basepath, biographydir, datasheet['FILENAME'])
        save(data, filename)
        print('processed', datasheet['FILENAME'])
