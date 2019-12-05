# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import datasheetparser
import htmlparser
import referenceparser
import symbolreplace
import flow
import alphaindexparser

def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'biography'
    data['_template'] = 'biography.html'

    # name and shortname
    data['shortname'] = symbolreplace.tags_to_unicode(datasheet['SHORTNAME'])
    data['fullname'] = symbolreplace.tags_to_unicode(datasheet['FULLNAME'])

    # authors
    data['authors'] = symbolreplace.tags_to_unicode(datasheet['AUTHORS'])

    data['summary'] = htmlparser.parse(datasheet['SUMMARY'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)

    # dates are tricky. for now leave them as they are
    data['birthdate'] = datasheet['BIRTHDATE']
    data['deathdate'] = datasheet['DEATHDATE']

    # birth and death year - remove the ,? if necessary
    date_pattern = re.compile(r'(\d+)(?:,\??)?')
    data['birthyear'] = re.sub(date_pattern, r'\1', datasheet['BIRTHYEAR'])
    data['deathyear'] = re.sub(date_pattern, r'\1', datasheet['DEATHYEAR'])

    # birthplace, deathplace
    data['birthplace'] = datasheet['BIRTHPLACE']
    data['deathplace'] = datasheet['DEATHPLACE']

    # mapinfo - just take the name, ignore mapnum and lat/long
    mapinfo = re.compile(r'\d,(?P<name>.+?),(?:(?P<lat>-?[\d.]+),(?P<long>-?[\d.]+))?')
    match = mapinfo.search(datasheet['MAPINFO'])
    data['maplocation'] = ''
    if match:
        data['maplocation'] = match.group('name')

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'], datasheet['FILENAME'], url_context)
    data['references'] = flow.to_flow_block('reference', json.loads(references)['data'])

    # parse translations (use the same format as references)
    # don't add them to data, as we're combining them with bio
    translations = referenceparser.parse_references(datasheet['TRANSLATION'], datasheet['FILENAME'], url_context)

    # parse cross references
    #xrefs = referenceparser.parse_cross_references(datasheet['XREFS'], datasheet['FILENAME'])
    #data['xrefs'] = xrefs

    # parse additional links (they use the same format as cross references)
    # don't add them to data, as we're combining them with bio
    additional = referenceparser.parse_cross_references(datasheet['ADDITIONAL'], datasheet['FILENAME'], url_context)
    data['additional'] = flow.to_flow_block('otherweb', json.loads(additional)['data'])

    # parse otherweb links (they use the same format as cross references)
    otherweb = referenceparser.parse_cross_references(datasheet['OTHERWEB'], datasheet['FILENAME'], url_context)
    data['otherweb'] = flow.to_flow_block('otherweb', json.loads(otherweb)['data'])

    # parse honours links (they use the same format as cross references)
    honours = referenceparser.parse_cross_references(datasheet['HONOURS'], datasheet['FILENAME'], url_context)
    data['honours'] = flow.to_flow_block('otherweb', json.loads(honours)['data'])

    # parse biography, and add in extras and translations
    data['content'] = htmlparser.parse(datasheet['BIOGRAPHY'],
                                datasheet['FILENAME'],
                                translations=json.loads(translations)['data'],
                                extras=json.loads(additional)['data'],
                                paragraphs=True,
                                url_context=url_context)

    # discover categories for this mathematician
    path = '/Biographies/%s' % datasheet['FILENAME']
    tags = []
    with open('../datasheets/Indexes/data.json') as f:
        category_data = json.load(f)
    for category in category_data:
        if path in category['entries']:
            tags.append(category['name'])
    data['tags'] = json.dumps(tags)

    # discover alphabetical tags for this mathematician
    displays = alphaindexparser.get_displays(datasheet['FILENAME'])
    displays = '\n'.join(displays)
    data['alphabetical'] = displays

    return data
