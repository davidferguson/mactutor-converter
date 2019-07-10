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
    data['_model'] = 'extra'
    data['_template'] = 'extra.html'

    # filename, title, headline and update date for this
    data['filename'] = datasheet['FILENAME']
    data['title'] = datasheet['TITLE']
    data['headline'] = datasheet['HEADLINE']
    data['update'] = datasheet['UPDATE']

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'], datasheet['FILENAME'])
    data['references'] = references

    # parse biography
    bio = htmlparser.parse(datasheet['EXTRA'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)
    data['extra'] = bio.replace('\\', '')

    return data
