# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import datasheetparser
import htmlparser
import referenceparser

savedir = 'biographies'


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
    data['birthlatlong'] = re.sub(r'\d+,.+?,(?:(-?[\d.]+),(-?[\d.]+))?', r'\1,\2', datasheet['MAPINFO'])

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
    bio = htmlparser.parse(datasheet['BIOGRAPHY'],
                                datasheet['FILENAME'],
                                translations=json.loads(translations)['data'],
                                extras=json.loads(additional)['data'],
                                paragraphs=True)
    data['biography'] = bio.replace('\\', '')

    return data
