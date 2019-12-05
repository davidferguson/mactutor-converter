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


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'honour'
    data['_template'] = 'honour.html'

    # filename, title, headline and update date for this
    data['title'] = symbolreplace.tags_to_unicode(datasheet['TITLE'])
    data['headline'] = htmlparser.parse(datasheet['HEADLINE'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)

    # parse biography
    data['content'] = htmlparser.parse(datasheet['CONTENT'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)

    data['tags'] = '[]'

    return data
