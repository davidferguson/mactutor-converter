# -*- coding: utf-8 -*-

# converts text string of references into array

import re

import biographyparser


def parse_references(references):
    parsed = []
    in_reference = True
    reference = None

    for line in references.splitlines():
        line = line.strip()

        # match against reference line
        bio_regex = re.compile(r'^\d+,\W(?P<reference>.+)$')
        match = re.match(bio_regex, line)
        if match:
            # this is a reference line
            reference = match.group('reference')
            parsed.append(reference)
            in_reference = True
            continue

        # match against empty line
        if line == '':
            in_reference = False
            continue

        # any other line
        if in_reference:
            reference += (' ' + line)

    for idx, reference in enumerate(parsed):
        parsed[idx] = biographyparser.parse(reference)

    return parsed


def parse_cross_references(references):
    parsed = []

    for line in references.splitlines():
        line = line.strip()

        # match against reference line
        bio_regex = re.compile(r'^\d+,(?P<link>\S+),(?P<text>.+)?$')
        match = re.match(bio_regex, line)
        if match:
            # this is a reference line
            link = match.group('link')
            text = match.group('text')
            if not text:
                text = link
            else:
                text = biographyparser.parse(text)
            reference = {
                'link': link,
                'text': text
            }
            parsed.append(reference)
            continue

    return parsed
