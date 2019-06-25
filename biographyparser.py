# -*- coding: utf-8 -*-

# parses biography quasi-html format to Markdown

#import re
import regex as re

import symbolreplace

def parse(bio, extras=[], translations=[], paragraphs=False):
    # check we've got a string here
    assert type(bio) == str

    # special case for the common issue
    if bio == "Papers in the Proceedings of the EMS</i>":
        return "Papers in the Proceedings of the EMS"
    if bio == "Papers in the Proceedings and Notes of the EMS</i>":
        return "Papers in the Proceedings and Notes of the EMS"

    # escape backslashes (because we are adding them)
    #regex = re.compile('\\', re.MULTILINE | re.DOTALL)
    #bio = re.sub(regex, '\\\\', bio)
    bio = bio.replace('\\', '\\\\')
    # escape any literal square brackets
    regex = re.compile(r'\[(?!\d+])', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, '\\[', bio)
    regex = re.compile(r'(?<!\[\d+)\]', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, '\\]', bio)

    # fix lists
    bio = bio.replace('\n\n<li', '\n<li')


    # ========= BLOCKS =========


    # convert <p> - MUST BE DONE FIRST
    # this regex deserves a comment of its own
    #
    # 1. the main part is in the middle: ^(.*?)$
    #    this matches against multiple lines - not just a single line.
    #
    # 2. the bit before it is a positive lookbehind
    #    this makes the expression only match IF one of:
    #       - its the start of the document: \A
    #       - there is a closing block tag preceeded by a \n
    #
    # 3. the bit after it is a positive lookahead
    #    it essentially does the same thing as the lookbehind, but matching IF:
    #       - its the end of the document: \Z
    #       - there is a newline peceeded by an opening block tag
    if paragraphs:
        expr = r'(?<=(?<=</Q>|</ol>|</h\d>|</k>|</ind>|</cp>|</cpb>|\n)\n|\A)^(.*?)$(?=(?=\Z|\n(?=\n|<Q>|<ol.*?>|<h\d>|<k>|<ind>|<cp>|<cpb>)))'
        regex = re.compile(expr, re.MULTILINE | re.DOTALL)
        bio = re.sub(regex, r'[p]\1[/p]', bio)
        bio = bio.replace('<n>', '')
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
    #bio = re.sub(regex, r'[list]\1[/list]', bio)
    bio = re.sub(regex, listreplace, bio)
    # convert <li>...</li>
    regex = re.compile(r'<li.*?>(.*?)(?:</li>)?$', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[item]\1[/item]', bio)

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
    regex = re.compile(r'<a href ?= ?[\'"]?(.+?)[\'"]?>(.*?)<\/a>')
    bio = re.sub(regex, r'[url=\1]\2[/url]', bio)

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
    #bio = re.sub(regex, r'[e=\1]THIS LINK[/e]', bio)
    bio = re.sub(regex, lambda match: ereplace(match, extras), bio)

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


    # convert <d>...</d>
    regex = re.compile(r'<d (\S+?)(?:\s.+?)?>', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[img]\1[/img]', bio)

    # convert [refnum]
    regex = re.compile(r'\[(\d+)\]', re.MULTILINE | re.DOTALL)
    bio = re.sub(regex, r'[ref]\1[/ref]', bio)
    bio = bio.replace('<!>', '') # John's reference hack

    # convert <T num>
    regex = re.compile(r'<T (?P<number>\d+)>', re.MULTILINE | re.DOTALL)
    #bio = re.sub(regex, r'[t]\1[/t]', bio)
    bio = re.sub(regex, lambda match: treplace(match, translations), bio)

    # convert \formulae\\
    # this is now done straight after blocks, as otherwise it is affected when
    # we convert superscript/subscript/symbols/etc.


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
        print('found opening/closing croc')
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
def ereplace(match, extras):
    number = match.group('number')
    extra = list(filter(lambda extra: extra['number'] == number, extras))
    assert len(extra) != 0
    extra = extra[0]

    text = extra['text'].strip()
    url = extra['link'].strip()
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
    return '[math]%s[/math]' % math

# helper function for dealing with lists
# this needs improving so it converts symbols to KaTeX/LaTeX's format
def listreplace(match):
    contents = match.group('list')
    contents = contents.strip()
    return '[list]\n%s\n[/list]' % contents
