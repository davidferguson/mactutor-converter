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
    data['shortname'] = symbolreplace.tags_to_unicode(datasheet['SHORTNAME'])
    data['fullname'] = htmlparser.parse(datasheet['FULLNAME'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)
    data['authors'] = datasheet['AUTHORS']
    data['update'] = datasheet['UPDATE']

    # something about indexes, not sure how this is used yet
    data['indexref'] = datasheet['INDEXREF']
    data['indexreffile'] = datasheet['INDEXREFFILE']

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'], datasheet['FILENAME'], url_context)
    data['references'] = flow.to_flow_block('reference', json.loads(references)['data'])

    # parse additional links (they use the same format as cross references)
    additional = referenceparser.parse_cross_references(datasheet['ADDITIONAL'], datasheet['FILENAME'], url_context)
    data['additional'] = flow.to_flow_block('otherweb', json.loads(additional)['data'])

    # parse translations (use the same format as references)
    # don't add them to data, as we're combining them with bio
    translations = referenceparser.parse_references(datasheet['TRANSLATION'], datasheet['FILENAME'], url_context)

    # parse otherweb links (they use the same format as cross references)
    otherweb = referenceparser.parse_cross_references(datasheet['OTHERWEB'], datasheet['FILENAME'], url_context)
    data['otherweb'] = flow.to_flow_block('otherweb', json.loads(otherweb)['data'])

    # parse history topic
    data['content'] = htmlparser.parse(datasheet['HISTTOPIC'],
                                datasheet['FILENAME'],
                                translations=json.loads(translations)['data'],
                                extras=json.loads(additional)['data'],
                                paragraphs=True,
                                url_context=url_context)

    return data
