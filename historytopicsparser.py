# -*- coding: utf-8 -*-

# converter for extras datasheets

import glob
import os
import json
import re

import datasheetparser
import htmlparser
import referenceparser
import symbolreplace
import flow


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'historytopic'
    data['_template'] = 'historytopic.html'

    # filename, short and full name, authors, update
    data['filename'] = datasheet['FILENAME']
    data['shortname'] = symbolreplace.tags_to_unicode(datasheet['SHORTNAME'])
    data['fullname'] = htmlparser.parse(datasheet['FULLNAME'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)
    data['authors'] = datasheet['AUTHORS']
    data['update'] = datasheet['UPDATE']

    # something about indexes, not sure how this is used yet
    data['indexref'] = datasheet['INDEXREF']
    data['indexreffile'] = datasheet['INDEXREFFILE']

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'], datasheet['FILENAME'])
    data['references'] = flow.to_flow_block('reference', json.loads(references)['data'])

    # parse additional links (they use the same format as cross references)
    additional = referenceparser.parse_cross_references(datasheet['ADDITIONAL'], datasheet['FILENAME'])
    data['additional'] = flow.to_flow_block('otherweb', json.loads(additional)['data'])

    # parse translations (use the same format as references)
    # don't add them to data, as we're combining them with bio
    translations = referenceparser.parse_references(datasheet['TRANSLATION'], datasheet['FILENAME'])

    # parse otherweb links (they use the same format as cross references)
    otherweb = referenceparser.parse_cross_references(datasheet['OTHERWEB'], datasheet['FILENAME'])
    data['otherweb'] = flow.to_flow_block('otherweb', json.loads(otherweb)['data'])

    # parse history topic
    bio = htmlparser.parse(datasheet['HISTTOPIC'],
                                datasheet['FILENAME'],
                                translations=json.loads(translations)['data'],
                                extras=json.loads(additional)['data'],
                                paragraphs=True,
                                url_context=url_context)
    data['histtopic'] = bio.replace('\\', '')

    return data
