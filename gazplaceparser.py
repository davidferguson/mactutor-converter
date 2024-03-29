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
import datasheetparser


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'gazplace'
    data['_template'] = 'gazplace.html'

    data['place'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['TITLE']))

    pattern = re.compile(r'(?P<lat>-?[\d.]+),(?P<long>-?[\d.]+)')
    match = pattern.search(datasheet['COORDS'])
    data['latitude'] = ''
    data['longitude'] = ''
    if match:
        data['latitude'] = match.group('lat')
        data['longitude'] = match.group('long')

    # i was an idiot, and made a mistake in generating the datasheets for GazData
    # the correct CONTENTS is in GazData3
    # so we have to read that instead
    path = os.path.join('../datasheets/GazData3/', datasheet['FILENAME'])
    datasheet2 = datasheetparser.parse_file(path)


    # convert the references to the new style of references
    refcount = 1
    parsed_references = []
    references = datasheet['REFERENCES'].strip().split('\n')
    for reference in references:
        reference = reference.strip()
        if reference == '':
            continue
        parts = reference.split('@')
        if len(parts) != 3:
            print(reference)
            assert len(parts) == 3
        replacement = parts[0].strip()
        text = parts[2].strip()

        if replacement not in datasheet2['CONTENTS']:
            print(reference)
        assert replacement in datasheet2['CONTENTS']
        datasheet2['CONTENTS'] = datasheet2['CONTENTS'].replace(replacement, '[%s]' % refcount)

        parsed_references.append({
            'number': str(refcount),
            'reference': htmlparser.parse(text, datasheet['FILENAME'])
        })

        refcount = refcount + 1

    data['references'] = flow.to_flow_block('reference', parsed_references)

    # parse biography, and add in extras and translations
    data['content'] = htmlparser.parse(datasheet2['CONTENTS'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)

    if data['place'] == 'Whitburn, Tyne & Wear':
        # add in the missing lat and long
        data['latitude'] = '54.9550395'
        data['longitude'] = '-1.3867149'

    if data['latitude'] == '' and data['longitude'] == '':
        # this is not a place, it should just be a page
        newdata = {}
        newdata['_model'] = 'page'
        newdata['_template'] = 'page.html'
        newdata['title'] = data['place']
        newdata['authors'] = ''
        newdata['content'] = data['content']
        return newdata

    return data
