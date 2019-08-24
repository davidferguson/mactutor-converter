# -*- coding: utf-8 -*-

# converter for quotations datasheets

import glob
import os
import json
import re

import datasheetparser
import htmlparser
import symbolreplace
import flow

NUMBER_CORRECTIONS = {
    'Aristotle': 32,
    'Bernoulli_Jacob': 5,
    'Bohr_Niels': 15,
    'Bronowski': 8,
    'Campanus': 1,
    'Cauchy': 1,
    'Dieudonne': 6,
    'Dyson': 3,
    'Euler': 7,
    'Feynman': 8,
    'Renyi': 2,
    'Thomson': 8,
}


def parse_quote(quote):
    parsed = {}
    # is there a source for this quote?
    lines = quote.split('\n')
    if len(lines) > 1:
        lastline = lines[-1]
        source = re.compile(r'<i>(.*?)</i>')
        match = source.search(lastline)
        if match and '</f' not in lastline:
            lines.pop()
            # found a source!
            return {'quote': '\n'.join(lines), 'source': lastline}
    return {'quote': quote, 'source': ''}


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'quotation'
    data['_template'] = 'quotation.html'

    # filename, name
    data['name'] = symbolreplace.tags_to_unicode(datasheet['NAME'])

    content = datasheet['CONTENT']
    numquotes = datasheet['NUMQUOTES']

    # special case cleaning rules
    if datasheet['FILENAME'] == 'Carmichael':
        content = content.replace('<p>', '')
    if datasheet['FILENAME'] in NUMBER_CORRECTIONS:
        numquotes = NUMBER_CORRECTIONS[datasheet['FILENAME']]

    # now parse the individual quotes
    content = content.split('<p>')
    quotes = []
    for quote in content:
        if quote.strip() != '':
            quotes.append(quote.strip())

    # holding 'more quotes' links, or 'translations by'
    data['more'] = ''

    if len(quotes) != 0 and 'More ' in quotes[-1] and '<a href' in quotes[-1]:
        #print('I *think* this is a *more quotes* paragraph:', quotes[-1])
        data['more'] = quotes.pop()

    if len(quotes) != 0 and data['more'] == '' and 'Translations ' in quotes[-1]:
        #print('I *think* this is a *translations by* paragraph:', quotes[-1])
        data['more'] = quotes.pop()

    if len(quotes) != int(numquotes):
        print('ERROR', len(quotes), 'expcting', int(numquotes))
        print(quotes)
        assert False

    # now parse the quotes and convert to html
    for idx, quote in enumerate(quotes):
        q = parse_quote(quote)
        q['quote'] = htmlparser.parse(q['quote'], 'Quotations/%s' % datasheet['FILENAME'], paragraphs=True, url_context=url_context)
        q['source'] = htmlparser.parse(q['source'], 'Quotations/%s' % datasheet['FILENAME'], paragraphs=False, url_context=url_context)
        quotes[idx] = q

    quotations = flow.to_flow_block('quotation', quotes)
    data['quotations'] = quotations

    return quotations
