# -*- coding: utf-8 -*-

# parses datasheet quasi-xml format to JSON

import re

TAGS = [
    'FILENAME',
    'SHORTNAME',
    'FULLNAME',
    'BIRTHDATE',
    'DEATHDATE',
    'BIRTHYEAR',
    'DEATHYEAR',
    'BIRTHPLACE',
    'DEATHPLACE',
    'MAPINFO',
    'COUNTRY',
    'NUMPICTS',
    'REFERENCES',
    'XREFS',
    'ADDITIONAL',
    'HONOURS',
    'SUMMARY',
    'QUOTATIONSNUMBER',
    'TRANSLATION',
    'OTHERWEB',
    'BIOGRAPHY',
    'AUTHORS',
    'INDEXREF',
    'INDEXREFFILE',
    'HISTTOPIC',
    'UPDATE',
    'TITLE',
    'HEADLINE',
    'EXTRA',
    'CONTENT',
    'TITLENAME',
    'EXTRAS',
    'FOUNDATION',
    'NAME',
    'NUMQUOTES',
    'HEADING1',
    'RANGES',
    'EQUATIONS',
    'JAVA',
    'CONTENTS',
    'WHODIDIT',
    'NONSTANDARDHEAD',
    'NONSTANDARDFOOT',
    'JSCRIPT',
    'USEHTMLFORMAT',
    'WORD',
    'SUPPLEMENT',
    'DATE',
    'ABOUT',
    'BIG',
    'NUMBER',
    'PLACENAME',
    'WEBREF',
    'GAZ',
    'LATLONG0',
    'INDEXNAMES',
    'COORDS',
    'LINKS',
    'HEADING2',
    'BIRTH',
    'DEATH',
    'ELECTED',
    'PROFESSION',
    'FELLOWSHIP',
    'BIOGRAPHY'
]

def parse_file(filename):
    # the encoding of these files is a bit of a guess. I *think* it's MacRoman
    # because MacRoman was used on Mac OS 9 and earlier (which MacTutor was
    # originally written on), and it decodes fine in TextEdit, which narrows it
    # down to utf8, mac_roman, or latin_1. From these, I think it's mac_roman as
    # I got some errors about control chatacters, and mac_roman stores normal
    # display characters in control code positions.
    with open(filename, 'r', encoding='mac_roman') as f:
        data = f.read()
    return parse_data(data)

def parse_data(data):
    # check we've got a string here
    assert type(data) == str

    parsed_data = {}
    for tag in TAGS:
        regex = re.compile(r'<%s>(.*?)<\/%s>' % (tag, tag), re.MULTILINE | re.DOTALL)
        match = re.search(regex, data)
        if match:
            parsed_data[tag] = match.group(1).strip()

    #slight hack for authors
    if 'AUTHORS' in parsed_data and parsed_data['AUTHORS'] == 'JOC/EFR':
        parsed_data['AUTHORS'] = "J J O'Connor and E F Robertson"
    return parsed_data
