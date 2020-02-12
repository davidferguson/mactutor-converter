# -*- coding: utf-8 -*-

# corrects image hrefs and link hrefs
# converts formulae to katex
# strips w links
# converts font to John format
# converts symbolgifs to unicode

import regex as re
import json
import html
from bs4 import BeautifulSoup
import os

import symbolreplace
import urls
import cleaning

def parse(bio, name, extras=[], translations=[], paragraphs=False, url_context='/'):
    # check we've got a string here
    assert type(bio) == str

    # run the new and improved cleaning
    bio = cleaning.clean(bio, name)

    # remove html special characters
    bio = html.unescape(bio)

    # convert formula to katex
    regex = re.compile(r'\\(?P<math>.+?)\\\\', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, mathreplace, bio)

    # check that the link location is correct
    regex = re.compile(r'<a\s+href\s*=\s*[\'"]?(?P<href>.+?)[\'"]?\s*>(?P<text>.*?)<\/a>')
    bio = re.sub(regex, lambda match: urlreplace(match, url_context), bio)

    # convert m links to w links
    regex = re.compile(r'<w(?:\s+(?P<name>.+?))?>(?P<text>.*?)\<\/w\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, mreplace, bio)

    # convert <font color=...>...</font> to f+, etc.
    regex = re.compile(r'<font color\s*=\s*[\'"]?(?P<color>\w+)[\'"]?\s*>(?P<text>.*?)</font>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, fontreplace, bio)

    # check that the image location is correct
    regex = re.compile(r'<d\s+(?P<content>.+?)>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, lambda match: dreplace(match, url_context, name), bio)

    # convert to normal diagrams
    regex = re.compile(r'(?P<tag><img\s+.+?>)', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, lambda match: imgreplace(match, url_context), bio)

    # convert symbolgifs to unicode
    bio = symbolreplace.symbols_to_unicode(bio)

    # we can do smart quotes here too, actually
    bio = bio.replace('’', '"')
    bio = bio.replace('‘', '"')
    bio = bio.replace("“", "'")
    bio = bio.replace("”", "'")

    # remove any print-only tags
    bio = bio.replace('<pr>', '')
    bio = bio.replace('</pr>', '')

    return bio


# helper function for dealing with \...\\
# this needs improving so it converts symbols to KaTeX/LaTeX's format
def mathreplace(match):
    entire = match.group(0)
    math = match.group('math')
    math = symbolreplace.symbols_to_unicode(math, katex=True)
    math = symbolreplace.tags_to_unicode(math, katex=True)

    # remove <b>...</b>
    regex = re.compile(r'<b>(.*?)</b>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    # remove <i>...</i>
    regex = re.compile(r'<i>(.*?)</i>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    # remove <u>...</u>
    regex = re.compile(r'<u>(.*?)</u>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    # remove <r>...</r>, <bl>...</bl>, <gr>...</gr> and <bro>...</bro>
    regex = re.compile(r'<(?:r|bl|gr|bro)>(.*?)</(?:r|bl|gr|bro)>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    # remove <f+>...</f+>
    regex = re.compile(r'<f\+>(.*?)</f>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    regex = re.compile(r'<fp>(.*?)</fp>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    # remove <f++>...</f>
    regex = re.compile(r'<f\+\+>(.*?)</f>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    # remove <f->...</->
    regex = re.compile(r'<f->(.*?)</f>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    regex = re.compile(r'<fm>(.*?)</fm>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)
    # remove <ovl>...</ovl>
    regex = re.compile(r'<ovl>(.*?)</ovl>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\1', math)

    # convert fractions
    regex = re.compile(r'\^(\S+) ?\/¬(\S+) ?', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'{{\1}\over{\2}}', math)

    # convert ^superscript
    regex = re.compile(r'\^(\S+)(?: ?)', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'^{\1}', math)
    regex = re.compile(r'<sup>(.*?)</sup>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'^{\1}', math)

    # convert ¬subscript
    regex = re.compile(r'¬(\S+)(?: ?)', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'_{\1}', math)
    regex = re.compile(r'<sub>(.*?)</sub>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'_{\1}', math)

    # fix functions
    mappings = ['isin','arcsin','arccos','arctan','arctg','arg','ch','cosec','cosh',
        'cos','cotg','coth','cot','argmin','csc','ctg','cth','deg','dim','exp',
        'hom','ker','lg','ln','log','sec','sinh','sin','tanh','tan',#'sh','tg','th'
        'det','gcd','inf','lim','liminf','limsup','Pr','sup','argmax',
        'max','min']
    for mapping in mappings:
        old_math = math
        regex = re.compile(r'(?<!(?:(?:\\)|(?:\\i)|(?:\\arc)))(%s)' % mapping)
        math = re.sub(regex, r'\\\1', math)

    # remove multiline formulas
    lines = math.split('\n')
    output = ''
    for line in lines:
        line = line.strip()
        if line == '':
            output += '\n\n'
            continue
        output += '\n<latex>%s</latex>' % line

    return output.strip()



# helper function for dealing with urls
# need to translate old URLs to new lektor format
def urlreplace(match, url_context):
    text = match.group('text')
    href = match.group('href')
    href = urls.convert(href, url_context)

    # convert biography links into m links
    if href.startswith('/Biographies/') and '#' not in href:
        if (href.endswith('/') and href.count('/') == 3) or href.count('/') == 2:
            name = href[13:]
            if href.endswith('/'):
                name = name[:-1]

            if text == name:
                return '<m>%s</m>' % (name)
            else:
                return '<m %s>%s</m>' % (name, text)

    return '<a href="%s">%s</a>' % (href, text)

# helper function for dealing with <m>...</m> and <m name>...</m>
def mreplace(match):
    name = match.group('name')
    text = match.group('text')
    if name == None:
        return r'<m>%s</m>' % text
    return r'<m=%s>%s</m>' % (name, text)

# convert font colours to John's format
def fontreplace(match):
    color = match.group('color')
    text = match.group('text')

    if color == 'red':
        return r'<r>%s</r>' % text
    elif color == 'blue':
        return r'<bl>%s</bl>' % text
    elif color == 'green':
        return r'<gr>%s</gr>' % text
    elif color == 'brown':
        return r'<bro>%s</bro>' % text
    else:
        return r'<font color="%s">%s</m>' % (color, text)


# helper function for dealing with images
def dreplace(match, url_context, datasheet_name):
    content = match.group('content')

    align = ''
    other = ''

    items = content.split(',')
    words = items[0].split(' ')

    name = words[0]

    if len(words) > 1:
        align = words[1]

    if len(items) > 1:
        other = items[1]

    fullname = name
    if '.' not in name:
        fullname = '%s.gif' % name

    href = '/Diagrams/%s' % fullname
    href = urls.convert(href, url_context)
    if (not href.startswith('/Diagrams/')):
        print('eek! (%s) (%s)' % (fullname, href))
        assert False
    fullname = href[10:]

    # try and match it with a diagram
    DIAGRAM_DIR = '/Users/david/Documents/MacTutor/actual-work/dev/mathshistory-site/content/Diagrams/'
    if not os.path.isfile(os.path.join(DIAGRAM_DIR, fullname)):
        print('NOT A DIAGRAM (%s), (%s)' % (name, fullname))
        with open('diagram-errors-converter.txt', 'a') as f:
            f.write('(%s) :: (%s) :: (%s)\n' % (datasheet_name, name, fullname))
        return ''

    return generate_diagram(fullname, align, other)

def generate_diagram(fullname, align, other):
    if align == '' and other == '':
        return '<d %s>' % fullname
    if other == '':
        return '<d %s %s>' % (fullname, align)
    return '<d %s %s,%s>' % (fullname, align, other)

def imgreplace(match, url_context):
    tag = match.group('tag')
    soup = BeautifulSoup(tag, 'html5lib')
    img = soup.find('img')
    src = img['src']
    converted = urls.convert(src, url_context)
    if converted.startswith('/Diagrams/'):
        fullname = converted[10:]
        # work out alignment
        align = ''
        if img.has_attr('align'):
            align = img['align']
        # work out the attributes
        attrs = img.attrs
        attrs.pop('src', None)
        attrs.pop('align', None)
        properties = ['%s="%s"' % (k, v) for k,v in attrs.items()]
        other = ' '.join(properties)
        return generate_diagram(fullname, align, other)

    img['src'] = urls.convert(src, url_context)
    fixed = img.prettify().strip()
    with open('fixed-images.txt', 'a') as f:
        f.write('%s :: %s :: %s\n' % (tag, fixed, url_context))
    return fixed
