# -*- coding: utf-8 -*-

import re

import htmlparser
import symbolreplace


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'place'
    data['_hidden'] = 'yes'

    # easily translatable info
    data['name'] = symbolreplace.tags_to_unicode(datasheet['PLACENAME'])
    data['country'] = symbolreplace.tags_to_unicode(datasheet['COUNTRY'])
    data['webref'] = datasheet['WEBREF']
    data['gaz'] = datasheet['GAZ']

    # lat and long
    pattern = re.compile(r'(?P<lat>-?[\d.]+),(?P<long>-?[\d.]+)')
    match = pattern.search(datasheet['LATLONG0'])
    data['latitude'] = ''
    data['longitude'] = ''
    if match:
        data['latitude'] = match.group('lat')
        data['longitude'] = match.group('long')

    return data
