# -*- coding: utf-8 -*-

# converts text string of references into array

import re
import json

import htmlparser
import urls


def parse_references(references, name, url_context):
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
            number = match.group('number')

            ref = {
                'number': number,
                'reference': reference.strip()
            }
            parsed_references.append(ref)
            in_reference = True
            continue

        # match against url
        if (line.startswith('http://') or line.startswith('https://')) and in_reference:
            # check there's not an issue with the line
            assert '<' not in line and '>' not in line
            # make the entire reference a link
            href = line
            href = urls.convert(href, url_context)
            text = parsed_references[-1]['reference']
            text = text.replace('<br>','')
            link = '<a href="%s">%s</a>' % (href, text)
            # only do this if there isn't already a link in the reference
            if '<a' not in text:
                parsed_references[-1]['reference'] = link
            in_reference = False

        # match against empty line
        if line == '' or '<p>' in line:
            in_reference = False
            continue

        # any other line
        if in_reference:
            parsed_references[-1]['reference'] += (' ' + line.strip())

    for reference in parsed_references:
        reference['reference'] = htmlparser.parse(reference['reference'], name)

    return_str = {'data': parsed_references}
    return_str = json.dumps(return_str)
    return return_str


def parse_cross_references(references, name, url_context):
    parsed = []

    for line in references.splitlines():
        line = line.strip()

        # match against reference line
        #bio_regex = re.compile(r'^(?P<number>\d+)\s*,\s*(?P<link>.+?)\s*,\s*(?P<text>.+?)(?:,\s*(?P<extratext>.+?))?$')
        bio_regex = re.compile(r'^(?P<number>\d+)\s*,\s*(?P<link>.+?)\s*(?:,\s*(?P<text>.+?))?(?:,\s*(?P<extratext>.+?))?$')
        match = re.match(bio_regex, line)
        if match:
            # this is a reference line
            number = match.group('number')
            link = match.group('link')
            text = match.group('text')
            if not text:
                text = 'THIS LINK'
            link = urls.convert(link, url_context)
            if match.group('extratext'):
                text += ' ' + match.group('extratext')
                text = text.strip()
            if not text:
                text = link
            else:
                text = htmlparser.parse(text, name)
            reference = {
                'link': link,
                'text': text,
                'number': number
            }
            parsed.append(reference)
            continue

    return_str = {'data': parsed}
    return_str = json.dumps(return_str)
    return return_str
