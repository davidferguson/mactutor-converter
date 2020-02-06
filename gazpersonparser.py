# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import htmlparser
import referenceparser
import symbolreplace
import flow


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'gazperson'
    data['_template'] = 'gazperson.html'

    data['name'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['TITLE']))


    # parse the list of people
    parsed_places = []
    places = datasheet['LINKS'].strip().split('\n')
    for place in places:
        place = place.strip()
        if place == '':
            continue

        addFragment = 'no'
        if place.endswith('*'):
            place = place[:-1]
            addFragment = 'yes'

        parsed_places.append({
            'place': place,
            'fragment': addFragment
        })

    data['places'] = flow.to_flow_block('gazplaceflow', parsed_places)

    return data
