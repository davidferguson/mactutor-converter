# -*- coding: utf-8 -*-

# this is the same as emsparser, but without the author field

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
    data['_model'] = 'page'
    data['_template'] = 'page.html'

    # sidebar
    data['sidebar'] = ''

    # easily translatable info
    data['title'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['TITLE']))

    # parse biography, and add in extras and translations
    data['content'] = htmlparser.parse(datasheet['CONTENT'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)

    return data
