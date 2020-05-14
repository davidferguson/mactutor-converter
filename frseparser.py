# -*- coding: utf-8 -*-

# this is the same as emsparser, but without the author field

import glob
import os
import json
import re
import datetime

import htmlparser
import referenceparser
import symbolreplace


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'frse'
    data['_template'] = 'frse.html'

    # easily translatable info
    data['name'] = symbolreplace.tags_to_unicode(datasheet['NAME'])
    data['birth'] = datasheet['BIRTH']
    data['birth'] = datasheet['DEATH']
    data['birthplace'] = symbolreplace.tags_to_unicode(datasheet['BIRTHPLACE'])
    data['profession'] = datasheet['PROFESSION']
    data['fellowship'] = datasheet['FELLOWSHIP']
    #data['biography'] = datasheet['BIOGRAPHY']

    if datasheet['BIOGRAPHY'] != '':
        assert datasheet['BIOGRAPHY'] == datasheet['FILENAME']

    elected = datasheet['ELECTED']
    if '/  /' in elected:
        # hack to make it work
        elected = elected.replace('/  /', '01/01/')
    electedDate = datetime.datetime.strptime(elected, '%d/%m/%Y')
    data['elected'] = electedDate.strftime('%Y-%m-%d')

    return data
