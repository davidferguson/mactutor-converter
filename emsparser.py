# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import htmlparser
import referenceparser
import symbolreplace


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'page'
    data['_template'] = 'page.html'

    # sidebar
    data['sidebar'] = ''

    # easily translatable info
    data['authors'] = htmlparser.parse(datasheet['WHODIDIT'], datasheet['FILENAME'], paragraphs=False, url_context=url_context)
    data['title'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['TITLE']))

    # check that this is a standard page
    #assert datasheet['USEHTMLFORMAT'] == 'Y'

    # need to convert it to a standard page
    content = datasheet['CONTENT']
    content = content.replace('<html>', '')
    content = content.replace('</html>', '')
    content = content.replace('<head>', '')
    content = content.replace('</head>', '')
    regex = re.compile(r'<title>(.*?)</title>', re.MULTILINE | re.DOTALL)
    content = re.sub(regex, r'', content)
    regex = re.compile(r'<meta (.*?)/>', re.MULTILINE | re.DOTALL)
    content = re.sub(regex, r'', content)
    regex = re.compile(r'<style>(.*?)</style>', re.MULTILINE | re.DOTALL)
    content = re.sub(regex, r'', content)
    regex = re.compile(r'<body(.*?)>', re.MULTILINE | re.DOTALL)
    content = re.sub(regex, r'', content)
    content = content.replace('</body>', '')
    content = content.strip()

    # also get rid of the 'show larger image' button
    regex = re.compile(r'<form>(.*?)</form>', re.MULTILINE | re.DOTALL)
    content = re.sub(regex, r'', content)

    # parse biography, and add in extras and translations
    data['content'] = htmlparser.parse(content,
                                datasheet['FILENAME'],
                                paragraphs=True,
                                url_context=url_context)

    return data
