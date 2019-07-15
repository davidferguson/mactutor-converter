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

maplocations = []
done_maplocations = []

def get_map_locations():
    data = {}
    data['_model'] = 'maplocations'
    data['_template'] = 'maplocations.html'
    data['maplocations'] = flow.to_flow_block('maplocation', maplocations)
    data['filename'] = 'maplocations'
    return data

def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'biography'
    data['_template'] = 'biography.html'

    # filename for this
    data['filename'] = datasheet['FILENAME']

    # name and shortname
    data['shortname'] = symbolreplace.tags_to_unicode(datasheet['SHORTNAME'])
    data['fullname'] = symbolreplace.tags_to_unicode(datasheet['FULLNAME'])

    # authors
    data['authors'] = symbolreplace.tags_to_unicode(datasheet['AUTHORS'])

    data['summary'] = htmlparser.parse(datasheet['SUMMARY'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)

    # dates are tricky. for now leave them as they are
    data['birthdate'] = datasheet['BIRTHDATE']
    data['birthyear'] = datasheet['BIRTHYEAR']
    data['deathdate'] = datasheet['DEATHDATE']
    data['deathyear'] = datasheet['DEATHYEAR']

    # birthplace
    data['birthplace'] = datasheet['BIRTHPLACE']

    # mapinfo - this is special
    # we add it to an array, so that it can be added to the maplocations file later
    mapinfo = re.compile(r'\d,(?P<name>.+?),(?:(?P<lat>-?[\d.]+),(?P<long>-?[\d.]+))?')
    match = mapinfo.search(datasheet['MAPINFO'])
    data['maplocation'] = ''
    if match and match.group('lat') and match.group('long'):
        if match.group('name') not in done_maplocations:
            location = {
                'name': match.group('name'),
                'lat': match.group('lat'),
                'long': match.group('long')
            }
            maplocations.append(location)
            done_maplocations.append(match.group('name'))
        data['maplocation'] = match.group('name')

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
                                paragraphs=True,
                                url_context=url_context)
    data['biography'] = bio.replace('\\', '')

    return data
