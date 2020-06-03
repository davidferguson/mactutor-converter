# -*- coding: utf-8 -*-

import re

import htmlparser
import symbolreplace
import urls
import flow


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'place'
    data['_hidden'] = 'yes'

    # easily translatable info
    data['name'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['PLACENAME']))
    data['country'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['COUNTRY']))
    #data['webref'] = datasheet['WEBREF']
    data['gaz'] = datasheet['GAZ']

    # some places are missing a country
    if datasheet['FILENAME'] == 'Higham_Ferrers':
        data['country'] = 'England'
    elif datasheet['FILENAME'] == 'Kansas_City':
        data['country'] = 'USA'
    elif datasheet['FILENAME'] == 'Lit':
        data['country'] = 'Sweden'
    elif datasheet['FILENAME'] == 'Martos':
        data['country'] = 'Spain'

    # and some places have a malformed country
    if data['country'] == 'Czech_Republic':
        data['country'] = 'Czech Republic'
    elif data['country'] == 'Sicily':
        data['country'] = 'Italy'
    elif data['country'].endswith(')'):
        data['country'] = data['country'][:-1]
    elif data['country'] == '':
        data['country'] == '--Unknown--'

    # lat and long
    pattern = re.compile(r'(?P<lat>-?[\d.]+),(?P<long>-?[\d.]+)')
    match = pattern.search(datasheet['LATLONG0'])
    data['latitude'] = ''
    data['longitude'] = ''
    if match:
        data['latitude'] = match.group('lat')
        data['longitude'] = match.group('long')

    # links
    links = []
    if datasheet['WEBREF'] != '':
        links.append({
            'url': datasheet['WEBREF'],
            'text': data['name']
        })
    for line in datasheet['OTHER'].split('\n'):
        line = line.strip()
        if line == '':
            continue
        wiki, text = line.split(',')
        links.append({
            'url': 'https://en.wikipedia.org/wiki/%s' % wiki,
            'text': text
        })
    for line in datasheet['OTHER2'].split('\n'):
        line = line.strip()
        if line == '':
            continue
        href, text = line.split(',')
        links.append({
            'url': urls.convert(href, url_context),
            'text': text
        })
    data['links'] = flow.to_flow_block('maplink', links)

    return data
