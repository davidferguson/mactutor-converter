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


def parse_equations(text, filename):
    equations = []
    eqtype = None

    typeregex = re.compile(r'^<b><font color=green>(?P<type>.+?)</font></b>.*$')
    equationregex = re.compile(r'^(?P<equation>\\.+?\\\\)$')

    text = text.split('\n')
    for line in text:
        line = line.strip()
        typematch = typeregex.search(line)
        equationmatch = equationregex.search(line)
        if typematch:
            # it's a type!
            assert eqtype == None
            eqtype = typematch.group('type')
        elif equationmatch:
            # it's an equation!
            assert type
            equation = {
                'type': eqtype,
                'equation': htmlparser.parse(equationmatch.group('equation'), filename, paragraphs=False)
            }
            eqtype = None
            equations.append(equation)
        else:
            assert False

    return equations


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'curve'
    data['_template'] = 'curve.html'

    # easily translatable info
    data['filename'] = datasheet['FILENAME']
    data['name'] = symbolreplace.tags_to_unicode(datasheet['FULLNAME'])

    # need to parse the individual equations out, and convert to flow
    equations = parse_equations(datasheet['EQUATIONS'], datasheet['FILENAME'])
    data['equations'] = flow.to_flow_block('curveequation', equations)

    # parse content
    content = htmlparser.parse(datasheet['CONTENTS'],
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)
    data['content'] = content.replace('\\', '')

    return data
