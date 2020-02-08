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
    data['name'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['HEADING1']))
    data['summary'] = htmlparser.parse(datasheet['HEADING2'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)
    data['wherefrom'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['TITLE']))

    # parse biography, and add in extras and translations
    data['content'] = htmlparser.parse(datasheet['CONTENT'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)

    return data
