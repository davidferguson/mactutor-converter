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
    data['_model'] = 'glossary'
    data['_template'] = 'glossary.html'

    # easily translatable info
    data['term'] = datasheet['WORD']

    # parse biography, and add in extras and translations
    data['content'] = htmlparser.parse(datasheet['CONTENTS'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)

    return data
