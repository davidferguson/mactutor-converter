# -*- coding: utf-8 -*-

# converts text string of references into array

import re
import json

import biographyparser


def parse_references(references):
    parsed_references = []
    in_reference = False
    reference = None

    for line in references.splitlines():
        line = line.strip()

        # match against reference line
        bio_regex = re.compile(r'^(?P<number>\d+)\s*,\s*(?P<reference>.+)$')
        match = re.match(bio_regex, line)
        if match:
            # this is a reference line
            reference = match.group('reference')
            reference = biographyparser.parse(reference)
            number = match.group('number')

            ref = {
                'number': number,
                'reference': reference
            }
            parsed_references.append(ref)
            in_reference = True
            continue

        # match against empty line
        if line == '':
            in_reference = False
            continue

        # any other line
        #if in_reference:
        #    references[len(references) - 1]['reference'] += (' ' + line)å

    return_str = {'data': parsed_references}
    return_str = json.dumps(return_str)
    return return_str


def parse_cross_references(references):
    parsed = []

    for line in references.splitlines():
        line = line.strip()

        # match against reference line
        bio_regex = re.compile(r'^(?P<number>\d+)\s*,\s*(?P<link>.+?)\s*,\s*(?P<text>.+?)(?:,\s*(?P<extratext>.+?))?$')
        match = re.match(bio_regex, line)
        if match:
            # this is a reference line
            number = match.group('number')
            link = match.group('link')
            text = match.group('text')
            if match.group('extratext'):
                text += ' ' + match.group('extratext')
                text = text.strip()
            if not text:
                text = link
            else:
                text = biographyparser.parse(text)
            reference = {
                'link': link,
                'text': text,
                'number': number
            }
            parsed.append(reference)
            continue

    #return json.dumps(parsed)
    return_str = {'data': parsed}
    return_str = json.dumps(return_str)
    return return_str
