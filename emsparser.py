# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import htmlparser
import referenceparser
import symbolreplace


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'contentpage'
    data['_template'] = 'contentpage.html'

    # easily translatable info
    data['filename'] = datasheet['FILENAME'].replace('Zagier/', '').replace('.', '')
    data['authors'] = datasheet['WHODIDIT']
    data['title'] = symbolreplace.tags_to_unicode(datasheet['TITLE'])

    # check that this is a standard page
    assert datasheet['USEHTMLFORMAT'] == 'Y'

    # parse biography, and add in extras and translations
    content = htmlparser.parse(datasheet['CONTENT'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)
    data['content'] = content.replace('\\', '')

    return data
