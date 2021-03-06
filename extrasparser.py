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
    data['_model'] = 'extra'
    data['_template'] = 'extra.html'

    # filename, title, headline and update date for this
    data['title'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['TITLE']))
    data['headline'] = htmlparser.parse(datasheet['HEADLINE'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)
    data['update'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['UPDATE']))

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'], datasheet['FILENAME'], url_context)
    data['references'] = flow.to_flow_block('reference', json.loads(references)['data'])

    # parse biography
    data['content'] = htmlparser.parse(datasheet['EXTRA'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)

    return data
