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
    data['_model'] = 'honours'
    data['_template'] = 'honours.html'

    # filename, title, headline and update date for this
    data['filename'] = datasheet['FILENAME']
    data['title'] = datasheet['TITLE']
    data['headline'] = datasheet['HEADLINE']

    # parse biography
    bio = htmlparser.parse(datasheet['CONTENT'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)
    data['content'] = bio.replace('\\', '')

    return data
