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
    data['_model'] = 'obituary'
    data['_template'] = 'obituary.html'

    # easily translatable info
    data['filename'] = datasheet['FILENAME']
    data['title'] = symbolreplace.tags_to_unicode(datasheet['TITLE'])
    data['heading'] = htmlparser.parse(datasheet['HEADING1'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)

    # parse biography, and add in extras and translations
    bio = htmlparser.parse(datasheet['CONTENT'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)
    data['content'] = bio.replace('\\', '')

    return data
