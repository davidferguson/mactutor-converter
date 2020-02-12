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

    regex = re.compile(r'<html>(?P<content>.*?)</html>', re.MULTILINE | re.DOTALL)
    content = re.sub(regex, strip, content)

    regex = re.compile(r'<head>(?P<content>.*?)</head>', re.MULTILINE | re.DOTALL)
    content = re.sub(regex, strip_all, content)

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


def strip(match):
    content = match.group('content')
    content = content.strip()
    return content

def strip_all(match):
    content = match.group('content')
    content = content.strip()
    content = content.replace('\n','')
    return content
