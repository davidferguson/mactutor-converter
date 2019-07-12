# -*- coding: utf-8 -*-

# converter for extras datasheets

import glob
import os
import json
import re

import datasheetparser
import htmlparser
import referenceparser


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'historytopic'
    data['_template'] = 'historytopic.html'

    # filename, short and full name, authors, update
    data['filename'] = datasheet['FILENAME']
    data['shortname'] = datasheet['SHORTNAME']
    data['fullname'] = htmlparser.parse(datasheet['FULLNAME'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)
    data['authors'] = datasheet['AUTHORS']
    data['update'] = datasheet['UPDATE']

    # something about indexes, not sure how this is used yet
    data['indexref'] = datasheet['INDEXREF']
    data['indexreffile'] = datasheet['INDEXREFFILE']

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'], datasheet['FILENAME'])
    data['references'] = references

    # parse additional links (they use the same format as cross references)
    additional = referenceparser.parse_cross_references(datasheet['ADDITIONAL'], datasheet['FILENAME'])
    data['additional'] = additional

    # parse translations (use the same format as references)
    # don't add them to data, as we're combining them with bio
    translations = referenceparser.parse_references(datasheet['TRANSLATION'], datasheet['FILENAME'])

    # parse otherweb links (they use the same format as cross references)
    otherweb = referenceparser.parse_cross_references(datasheet['OTHERWEB'], datasheet['FILENAME'])
    data['otherweb'] = otherweb

    # parse history topic
    bio = htmlparser.parse(datasheet['HISTTOPIC'],
                                datasheet['FILENAME'],
                                translations=json.loads(translations)['data'],
                                extras=json.loads(additional)['data'],
                                paragraphs=True,
                                url_context=url_context)
    data['histtopic'] = bio.replace('\\', '')

    return data
