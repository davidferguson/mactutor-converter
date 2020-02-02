# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import htmlparser
import referenceparser
import symbolreplace
import flow


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'society'
    data['_template'] = 'society.html'

    # easily translatable info
    data['name'] = symbolreplace.tags_to_unicode(datasheet['TITLENAME'])
    data['headline'] = htmlparser.parse(datasheet['HEADLINE'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)
    data['update'] = datasheet['UPDATE']
    data['foundation'] = datasheet['FOUNDATION']

    # external site parsing
    link = re.compile(r'<a\s+href ?= ?[\'"]?(?P<href>.+?)[\'"]?\s*>(?P<text>.*?)<\/a>')
    if datasheet['OTHERWEB'].strip() == '':
        data['website'] = ''
    else:
        match = link.search(datasheet['OTHERWEB'].strip())
        if not match:
            print('not link "%s"' % datasheet['OTHERWEB'].strip())
            assert match
        data['website'] = match.group('href')

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'], datasheet['FILENAME'], url_context)
    data['references'] = flow.to_flow_block('reference', json.loads(references)['data'])

    # parse additional links (they use the same format as cross references)
    # don't add them to data, as we're combining them with bio
    additional = referenceparser.parse_cross_references(datasheet['EXTRAS'], datasheet['FILENAME'], url_context)
    data['additional'] = flow.to_flow_block('otherweb', json.loads(additional)['data'])

    # parse biography, and add in extras and translations
    data['content'] = htmlparser.parse(datasheet['CONTENT'],
                                datasheet['FILENAME'],
                                extras=json.loads(additional)['data'],
                                paragraphs=True,
                                url_context=url_context)

    data['tags'] = '[]'

    return data
