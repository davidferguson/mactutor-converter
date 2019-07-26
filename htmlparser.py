# -*- coding: utf-8 -*-

# parses biography quasi-html format to Markdown

#import re
import regex as re
import json
import html

import symbolreplace
import cleaning
import block_parser
import urls

def parse(bio, name, extras=[], translations=[], paragraphs=False, url_context='/'):
    # check we've got a string here
    assert type(bio) == str

    # clean the data
    bio = cleaning.clean(bio, name)

    # remove html special characters
    bio = html.unescape(bio)

    if paragraphs:
        bio = bio.replace('<n>', '')
        blocks = block_parser.process_blocks(bio, name)
        parsed_blocks = []
        for block in blocks:
            parsed = _parse(block, name, extras, translations, paragraphs, url_context)
            parsed = parsed.strip()
            parsed_blocks.append(parsed)
        output = '\n\n'.join(parsed_blocks)
        return output
    else:
        return _parse(bio, name, extras, translations, paragraphs, url_context)


def _parse(bio, name, extras, translations, paragraphs, url_context):
    # escape backslashes (because we are adding them)
    #regex = re.compile('\\', re.MULTILINE | re.DOTALL)
    #bio = re.sub(regex, '\\\\', bio)
    bio = bio.replace('\\', '\\\\')
    # escape any literal square brackets
    regex = re.compile(r'\[(?!\d+])', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, '\\[', bio)
    regex = re.compile(r'(?<!\[\d+)\]', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, '\\]', bio)


    # ========= BLOCKS =========
    # paragraphs are converted into <p>...</p> above
    regex = re.compile(r'<p>(.*?)</p>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[p]\1[/p]', bio)
    # convert <cp>...</cp>
    regex = re.compile(r'<cp>(.*?)</cp>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[p=gray]\1[/p]', bio)
    # convert <cpb>...</cpb>
    regex = re.compile(r'<cpb>(.*?)</cpb>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[p=cyan]\1[/p]', bio)
    # convert <br>
    regex = re.compile(r'<br>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'\n', bio)

    # convert <h1>...</h1>
    regex = re.compile(r'<h1>(.*?)</h1>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[h1]\1[/h1]', bio)
    # convert <h2>...</h2>
    regex = re.compile(r'<h2>(.*?)</h2>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[h2]\1[/h2]', bio)
    # convert <h3>...</h3>
    regex = re.compile(r'<h3>(.*?)</h3>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[h3]\1[/h3]', bio)
    # convert <h4>...</h4>
    regex = re.compile(r'<h4>(.*?)</h4>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[h4]\1[/h4]', bio)
    # convert <h5>...</h5>
    regex = re.compile(r'<h5>(.*?)</h5>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[h5]\1[/h5]', bio)
    # convert <h6>...</h6>
    regex = re.compile(r'<h6>(.*?)</h6>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[h6]\1[/h6]', bio)

    # convert <Q>...</Q>
    # also look for lowercase as there are two instances (Maclaurin, Magnus) of that
    regex = re.compile(r'<[Qq]>(.*?)</[Qq]>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[quote]\1[/quote]', bio)

    # convert <ol>...</ol>
    regex = re.compile(r'<ol.*?>(?P<list>.*?)</ol>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, listreplace, bio)

    # convert <k>...</k>
    regex = re.compile(r'<k>(.*?)</k>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[centre]\1[/centre]', bio)
    # convert <ind>...</ind>
    regex = re.compile(r'<ind>(.*?)</ind>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[ind]\1[/ind]', bio)

    # convert <pre>...</pre>
    regex = re.compile(r'<pre>(.*?)</pre>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[pre]\1[/pre]', bio)


    # OUT OF PLACE - do math NOW as it's affected by marks
    # convert \formulae\\
    # we do double the amount of slashes becuase we doubled them at the start
    regex = re.compile(r'\\\\(?P<math>.+?)\\\\\\\\', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, mathreplace, bio)


    # ========= MARKS =========


    # convert <a href="..">...</a>
    regex = re.compile(r'<a\s+href ?= ?[\'"]?(?P<href>.+?)[\'"]?\s*>(?P<text>.*?)<\/a>')
    bio = re.sub(regex, lambda match: urlreplace(match, url_context), bio)

    # convert <b>...</b>
    regex = re.compile(r'<b>(.*?)</b>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[b]\1[/b]', bio)
    # convert <i>...</i>
    regex = re.compile(r'<i>(.*?)</i>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[i]\1[/i]', bio)
    # convert <u>...</u>
    regex = re.compile(r'<u>(.*?)</u>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[u]\1[/u]', bio)

    # convert ^superscript
    regex = re.compile(r'\^(\S+)', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[sup]\1[/sup]', bio)
    regex = re.compile(r'<sup>(.*?)</sup>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[sup]\1[/sup]', bio)
    # convert ¬subscript
    regex = re.compile(r'¬(\S+)', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[sub]\1[/sub]', bio)
    regex = re.compile(r'<sub>(.*?)</sub>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[sub]\1[/sub]', bio)

    # convert <m>...</m> and <m name>...</m>
    regex = re.compile(r'<m(?:\s+(?P<name>.+?))?>(?P<text>.*?)\<\/m\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, mreplace, bio)
    # convert <w>...</w> and <w name>...</w>
    regex = re.compile(r'<w(?:\s+(?P<name>.+?))?>(?P<text>.*?)\<\/w\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, wreplace, bio)
    # convert <g glossary>...</g>
    regex = re.compile(r'<g\s+(.+?)>(.*?)\<\/g\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[gl=\1]\2[/gl]', bio)
    # convert <ac academy>...</g>
    regex = re.compile(r'<ac\s+(.+?)>(.*?)\<\/ac\>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[ac=\1]\2[/ac]', bio)
    # convert <E num>
    regex = re.compile(r'<E (?P<number>\d+)>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, lambda match: ereplace(match, extras, url_context), bio)

    # convert <r>...</r>
    regex = re.compile(r'<r>(.*?)</r>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=red]\1[/color]', bio)
    # convert <bl>...</bl>
    regex = re.compile(r'<bl>(.*?)</bl>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=blue]\1[/color]', bio)
    # convert <gr>...</gr>
    regex = re.compile(r'<gr>(.*?)</gr>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=green]\1[/color]', bio)
    # convert <bro>...</bro>
    regex = re.compile(r'<bro>(.*?)<bro>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=brown]\1[/brown]', bio)
    # convert <font color=...>...</font>
    regex = re.compile(r'<font color ?= ?[\'"]?(\w+)[\'"]?>(.*?)</font>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[color=\1]\2[/color]', bio)

    # convert <f+>...</f+>
    regex = re.compile(r'<f\+>(.*?)</f>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[big]\1[/big]', bio)
    # convert <f++>...</f++>
    regex = re.compile(r'<f\+\+>(.*?)</f>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[big][big]\1[/big][/big]', bio)
    # convert <f->...</f->
    regex = re.compile(r'<f->(.*?)</f>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[small]\1[/small]', bio)

    # convert <c>...</c>
    regex = re.compile(r'<c>(.*?)</c>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[code]\1[/code]', bio)

    # convert <ovl>...</ovl>
    regex = re.compile(r'<ovl>(.*?)</ovl>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[ovl]\1[/ovl]', bio)


    # ========= INLINE =========


    # convert <d ...>
    regex = re.compile(r'<d (?P<href>\S+?)(?:\s.+?)?>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, lambda match: imgreplace(match, url_context), bio)

    # bit of a hack - convert <allow_img ...>
    regex = re.compile(r'<allow_img (\S+?)>', re.MULTILINE | re.DOTALL)
    #bio = re.sub(regex, lambda match: imgreplace(match, url_context), bio)
    bio = re.sub(regex, r'[img]\1[/img]', bio)

    # convert [refnum]
    regex = re.compile(r'\[(\d+)\]', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[ref]\1[/ref]', bio)

    # convert <T num>
    regex = re.compile(r'<T (?P<number>\d+)>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, lambda match: treplace(match, translations), bio)

    # convert \formulae\\
    # this is now done straight after blocks, as otherwise it is affected when
    # we convert superscript/subscript/symbols/etc.

    # convert <a name=".."></a>
    regex = re.compile(r'<a\s+name ?= ?[\'"]?(.+?)[\'"]?\s*><\/a>')
    bio = re.sub(regex, r'[anchor]\1[/anchor]', bio)


    # ========= OTHER =========


    # convert symbols
    bio = symbolreplace.symbols_to_unicode(bio)
    # and convert custom symbol tags too
    bio = symbolreplace.tags_to_unicode(bio)

    # deal with smart quotes
    bio = bio.replace('’', '"')
    bio = bio.replace('‘', '"')
    bio = bio.replace("“", "'")
    bio = bio.replace("”", "'")

    # not done yet: clear, clearl, proofend
    bio = bio.replace('<clear>', '\\n')

    # check we haven't left any tags behind
    open_croc = re.compile(r'<(?!\s)', re.MULTILINE | re.DOTALL)
    close_croc = re.compile(r'(?<!\s)>', re.MULTILINE | re.DOTALL)
    match = open_croc.search(bio) or close_croc.search(bio)
    if match:
        print('found opening/closing croc in', name)
        print()
        print(bio)
        assert False


    return bio



# helper function for dealing with <d because we want to see what the image is
images = []
def dreplace(match):
    global images
    image = match.group('image')
    image = image.strip()
    images.append(image)
    return '![%s](%s)' % (image, image)

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

# helper function for converting extras links to normal links
def ereplace(match, extras, url_context):
    number = match.group('number')
    extra = list(filter(lambda extra: extra['number'] == number, extras))
    assert len(extra) != 0
    extra = extra[0]

    text = extra['text'].strip()
    url = extra['link'].strip()
    #url = urls.convert(url, url_context) # urls already converted
    res = r'[url=%s]%s[/url]' % (url, text)
    return res

# helper function for converting translation links to inline links
def treplace(match, translations):
    number = match.group('number')
    translation = list(filter(lambda tran: tran['number'] == number, translations))
    #assert len(translation) != 0
    if len(translation) == 0:
        print('can\'t find reference ', number)
        assert False
    translation = translation[0]

    text = translation['reference'].strip()
    res = r'[t]%s[/t]' % text
    return res

# helper function for dealing with \...\\
# this needs improving so it converts symbols to KaTeX/LaTeX's format
def mathreplace(match):
    entire = match.group(0)
    math = match.group('math')
    math = symbolreplace.symbols_to_unicode(math, katex=True)
    math = symbolreplace.tags_to_unicode(math, katex=True)

    # convert <b>...</b>
    regex = re.compile(r'<b>(.*?)</b>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\textbf{\1}', math)
    # convert <i>...</i>
    regex = re.compile(r'<i>(.*?)</i>', re.MULTILINE | re.DOTALL)
    math = re.sub(regex, r'\textit{\1}', math)

    return '[math]%s[/math]' % math

# helper function for dealing with lists
def listreplace(match):
    s = match.group('list').strip()
    items = []
    pos = 0
    in_item = False
    current_item = ''

    while pos < len(s):
        if pos+3 <= len(s) and s[pos:pos+3] == '<li':
            in_item = True
            pos += 3
            # skip until the end of the opening tag
            while s[pos] != '>':
                pos += 1
            pos += 1
            current_item = current_item.strip()
            if current_item == '':
                continue
            items.append(current_item)
            current_item = ''
            continue

        if pos+4 <= len(s) and s[pos:pos+4] == '</li':
            assert in_item
            in_item = False
            pos += 4
            # skip until the end of the opening tag
            while s[pos] != '>':
                pos += 1
            pos += 1
            continue

        if in_item and pos < len(s):
            current_item += s[pos]

        pos += 1

    if in_item and current_item.strip() != '':
        items.append(current_item.strip())

    for i, item in enumerate(items):
        items[i] = '[item]%s[/item]' % item

    bbcode = '\n\n'.join(items)

    return '[list]\n%s\n[/list]' % bbcode

# helper function for dealing with urls
# need to translate old URLs to new lektor format
def urlreplace(match, url_context):
    text = match.group('text')
    href = match.group('href')
    href = urls.convert(href, url_context)
    return '[url=%s]%s[/url]' % (href, text)

# helper function for dealing with urls
# need to translate old URLs to new lektor format
def imgreplace(match, url_context):
    href = match.group('href')
    href = '../Diagrams/' + href
    href = urls.convert(href, url_context)
    return '[img]%s[/img]' % href
