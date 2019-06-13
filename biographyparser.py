# -*- coding: utf-8 -*-

# parses biography quasi-html format to Markdown

import re

import symbolreplace

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
    'AUTHORS'
]

def parse(bio):
    # check we've got a string here
    assert type(bio) == str

    # strip whitespace
    bio = bio.strip()

    # convert <a href="..">...</a>
    regex = re.compile(r'<a href=[\'"](.+?)[\'"].*?>(.*?)<\/a>')
    bio = re.sub(regex, r'[\1](\2)', bio)

    # convert <b>...</b>
    regex = re.compile(r'<b>(.*?)</b>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'**\1**', bio)

    # convert <h1>...</h1>
    regex = re.compile(r'<h1>(.*?)</h1>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'# \1', bio)

    # convert <h2>...</h2>
    regex = re.compile(r'<h2>(.*?)</h2>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'## \1', bio)

    # convert <h3>...</h3>
    regex = re.compile(r'<h3>(.*?)</h3>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'### \1', bio)

    # convert <h4>...</h4>
    regex = re.compile(r'<h4>(.*?)</h4>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'#### \1', bio)

    # convert <h5>...</h5>
    regex = re.compile(r'<h5>(.*?)</h5>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'##### \1', bio)

    # convert <h6>...</h6>
    regex = re.compile(r'<h6>(.*?)</h6>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'###### \1', bio)

    # convert <ol>...</ol>
    regex = re.compile(r'(<ol>(?P<list>.*?)</ol>)', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, olreplace, bio)

    # convert <br> and <p> and <n>
    regex = re.compile(r'<(?:br|p)>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'\n', bio)

    # convert <n>
    regex = re.compile(r'<n>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'\n', bio)

    # convert <u>...</u>
    regex = re.compile(r'<u>(.*?)</u>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[u]\1[/u]', bio)

    # convert <u>...</u>
    regex = re.compile(r'<u>(.*?)</u>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[u]\1[/u]', bio)

    # convert <ovl>...</ovl>
    regex = re.compile(r'<ovl>(.*?)</ovl>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[ovl]\1[/ovl]', bio)

    # convert <u>...</u>
    regex = re.compile(r'<k>(.*?)</k>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[centre]\1[/centre]', bio)

    # convert <c>...</c>
    regex = re.compile(r'<c>(.*?)</c>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'```\n\1\n```', bio)

    # convert <d>...</d>
    regex = re.compile(r'(<d (?P<image>\w+).*?>)', re.MULTILINE | re.DOTALL)
    images = []
    bio = re.sub(regex, dreplace, bio)

    # convert <q>...</q>
    regex = re.compile(r'<Q>(?P<quote>.*?)</Q>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, qreplace, bio)

    # convert <r>...</r>
    regex = re.compile(r'<r>(.*?)</r>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=red]\1[/color]', bio)

    # convert <bl>...</bl>
    regex = re.compile(r'<bl>(.*?)</bl>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=blue]\1[/color]', bio)

    # convert <g>...</g>
    regex = re.compile(r'<g>(.*?)</g>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=green]\1[/color]', bio)

    # convert <cp>...</cp>
    regex = re.compile(r'<cp>(.*?)</cp>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[bgcolor=gray]\1[/bgcolor]', bio)

    # convert <cpb>...</cpb>
    regex = re.compile(r'<cpb>(.*?)</cpb>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[bgcolor=cyan]\1[/bgcolor]', bio)

    # convert <m>...</m> and <m name>...</m>
    regex = re.compile(r'<m\s*(?: \s*(?P<name>\w+)\s*)?>(?P<text>.*?)\<\/m\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, mreplace, bio)

    # convert <w>...</w> and <w name>...</w>
    regex = re.compile(r'<w\s*(?: \s*(?P<name>\w+)\s*)?>(?P<text>.*?)\<\/w\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, mreplace, bio)

    # convert <g glossary>...</g>
    regex = re.compile(r'<g\s*(\w+)\s*>(.*?)\<\/g\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[gl=\1]\2[/gl]', bio)

    # convert <E num>
    regex = re.compile(r'<E (\d+)>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[e=\1]THIS LINK[/e]', bio)

    # convert <T num>
    regex = re.compile(r'<T (\d+)>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[t=\1]', bio)

    # convert <ac academy>...</g>
    regex = re.compile(r'<ac\s*(\w+)\s*>(.*?)\<\/ac\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[ac=\1]\2[/ac]', bio)

    # convert [ref]
    #regex = re.compile(r'\[(\d+)\]', re.MULTILINE | re.DOTALL)
    #bio = re.sub(regex, r'[ref=\1]', bio)

    # convert \formulae\\
    regex = re.compile(r'\\(.+?)\\\\', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'$$\1$$', bio)

    # convert ^superscript
    regex = re.compile(r'\^(\S+)', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[sup]\1[/sup]', bio)

    # convert ¬subscript
    regex = re.compile(r'¬(\S+)', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[sub]\1[/sub]', bio)

    # convert symbols
    bio = symbolreplace.symbols_to_unicode(bio)

    # and convert custom symbol tags too
    bio = symbolreplace.tags_to_unicode(bio)

    # things not mentioned in the sheet are below:

    # deal with smart quotes
    bio = bio.replace('’', '"')
    bio = bio.replace('‘', '"')
    bio = bio.replace("“", "'")
    bio = bio.replace("”", "'")

    # convert <i>...</i>
    regex = re.compile(r'<i>(.*?)</i>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'*\1*', bio)

    # convert <bro>...</bro>
    regex = re.compile(r'<g>(.*?)</g>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=brown]\1[/color]', bio)

    # not done yet: clear, clearl, proofend, f+, f++, f-, ind

    return bio


# two helper functions for converting ordered lists because they have state
licounter = 0
def lireplace(match):
    global licounter
    licounter += 1
    item = match.group('item')
    item = item.strip()
    return '%s %s' % (licounter, item)
def olreplace(match):
    global licounter
    licounter = 0
    list = match.group('list')
    list = list.strip()
    item_regex = re.compile(r'<li.*?>(?P<item>.*)')
    newlist = re.sub(item_regex, lireplace, list)
    return '\n\n%s\n\n' % newlist

# helper function for dealing with <d because we want to see what the image is
images = []
def dreplace(match):
    global images
    image = match.group('image')
    image = image.strip()
    images.append(image)
    return '![%s](%s)' % (image, image)

# helper function for dealing with <Q>...</Q>
def qreplace(match):
    quote = match.group('quote')
    quote = quote.strip()
    quote = quote.split('\n')
    quote = '\n> '.join(quote)
    quote = '\n\n> ' + quote + '\n\n'
    return quote

# helper function for dealing with <m>...</m> and <m name>...</m>
def mreplace(match):
    name = match.group('name')
    text = match.group('text')
    if name == None:
        return r'[m]%s[/m]' % text
    return r'[m=%s]%s[/m]' % (name, text)

# helper function for dealing with <w>...</w> and <w name>...</w>
def wreplace(match):
    name = match.group('name')
    text = match.group('text')
    if name == None:
        return r'[w]%s[/w]' % text
    return r'[w=%s]%s[/w]' % (name, text)
