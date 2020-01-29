import regex as re
from urllib.parse import urljoin, urlparse
import glob
import os
import json

def biography_rename(name):
    map = {
        "Abu'l-Wafa": "Abul-Wafa",
        "D'Adhemar": "DAdhemar",
        "D'Alembert": "DAlembert",
        "D'Ocagne": "DOcagne",
        "D'Ovidio": "DOvidio",
        "De_L'Hopital": "De_LHopital",
        "Krasnosel'skii": "Krasnoselskii",
        "Thompson_D'Arcy": "Thompson_DArcy"
    }
    if name in map:
        name = map[name]
    return name

def convert(href, url_context):
    original_href = href

    # generate the current context url
    base_url = urljoin('https://www-history.mcs.st-andrews.ac.uk/', url_context)

    href = href.strip()
    href = href.replace('" target=_blank', '')
    href = href.replace('target=_blank', '')
    href = href.replace('target=blank_', '')
    href = href.replace('" target="_blank', '')
    href = href.replace('target="_blank', '')
    href = href.replace('height=800', '')
    if href.endswith(' ,'): href = href[:-1]
    href = href.strip()

    if href.startswith('\\http://'):
        href = href[1:]
    elif href.startswith('href=http://'):
        href = href[5:]

    pattern = re.compile(r'^https?://www-history.mcs.st-and(?:rews)?.ac.uk(?P<page>.*)$')
    match = pattern.search(href)
    if match:
        # this is an external link that goes to us! convert to absolute
        href = match.group('page')

    # if a anchor link, return it
    if href.startswith('#'):
        return href

    # if a email link, return it
    if href.startswith('mailto:'):
        return href

    # win0 javascript pattern
    pattern = re.compile(r'^javascript:win0\(\'(?P<href>.*?)\'(?:.*?)\)$')
    match = pattern.search(href)
    if match:
        href = '../' + match.group('href')

    # win1 second javascript pattern - no forced line start and end
    # this is because when a javascript:win1 and a href are present, the js is
    # usually the correct one
    pattern = re.compile(r'javascript:win1\(\'(?P<href>.*?)\'(?:.*?)\)')
    match = pattern.search(href)
    if match:
        href = match.group('href')

    # showcurve javascript pattern
    pattern = re.compile(r'^javascript:showcurve\(\'(?P<curve>.*?)\'(?:.*?)\)$')
    match = pattern.search(href)
    if match:
        curve = match.group('curve')
        href = '../Curvepics/' + curve + '.gif'

    # if a external url, return it
    if href.startswith('http://') or href.startswith('https://') or href.startswith('ftp://') or href.startswith('//'):
        return href

    # now convert the href to an absolute mactutor link
    href_full = urljoin(base_url, href)

    # and parse it into path and fragment
    parsed = urlparse(href_full)
    path = parsed.path
    fragment = parsed.fragment

    while path.startswith('/history/'):
        path = path[8:]

    html_directories = ('/Astronomy/','/Biographies/','/Curves/','/Extras/','/HistTopics/','/Honours/','/Quotations/','/Societies/','/Strick/','/Tait/','/Wallace/')
    attachment_directories = ('/Bookpages/','/Publications/','/DNB/','/DSB/','/BSHM/')

    # two special cases - need to remove spaces
    path = path.replace('LMS FrolichPrize', 'LMSFrolichPrize')
    path = path.replace('Atiyah_NY Times', 'Atiyah_NYTimes')

    # sometimes we have moved things around, so need to correct this here
    with open('moved_array.json', 'r') as f:
        moved_array = json.load(f)
    for item in moved_array:
        move_from = item['from']
        move_to = item['to']
        if path.startswith(move_from) and path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            path = path.replace(move_from, move_to)
            with open('moved_array.txt', 'a') as f:
                f.write('%s :: %s :: %s\n' % (path, move_from, move_to))
            break

    if path == '/':
        page = '/'

    elif path.startswith(html_directories):
        if path.endswith('.html'):
            page = path[:-5]
        else:
            page = path

    elif path.startswith(attachment_directories):
        if path.endswith('index.html'):
            page = path[:-10]
        else:
            page = path

    elif path.startswith('/Diagrams/'):
        # need to convert a few
        if path.startswith('/Diagrams/braid/'):
            path = path.replace('/Diagrams/braid/', '/Diagrams/')
        if path.startswith('/Diagrams/fairbook/'):
            path = path.replace('/Diagrams/fairbook/', '/Diagrams/')
        if path.startswith('/Diagrams/wf/'):
            path = path.replace('/Diagrams/wf/', '/Diagrams/')

        # see if this matches a diagram
        DIAGRAM_DIR = '/Users/david/Documents/MacTutor/actual-work/dev/mathshistory-site/content/Diagrams/'
        diagram = path[10:]
        if os.path.isfile(os.path.join(DIAGRAM_DIR, diagram)):
            page = path
        else:
            # not a diagram, try and resolve this
            matches = glob.glob('%s%s*' % (DIAGRAM_DIR, diagram))
            if len(matches) != 1:
                with open('diagram-errors.txt', 'a') as f:
                    f.write('%s :: %s :: %s\n' % (original_href, url_context, diagram))
                page = ''
            else:
                page = '/Diagrams/%s' % os.path.basename(matches[0])

    elif path.startswith('/Obits/'):
        page = '/TimesObituaries/' + path[7:]

    elif path.startswith('/Glossary/'):
        if path.endswith('index.html'):
            page = path[:-10]
        elif path.endswith('.html'):
            entry = path[10:-5]
            page = '/Glossary/#%s' % entry
        else:
            page = path

    elif path.startswith('/BigPictures/'):
        pattern = re.compile(r'/BigPictures/(?P<image>(?P<name>.+?)(?:_\d+)?\..*)')
        match = pattern.search(path)
        if match:
            name = match.group('name')
            image = match.group('image')
            page = '/Biographies/%s/%s' % (name, image)
        else:
            page = path

    elif path.startswith('/References/'):
        if path.endswith('.html'):
            name = path[12:-5]
            page = '/Biographies/%s/' % name
        else:
            page = path

    elif path.startswith('/Obits2/'):
        page = '/Obituaries/' + path[8:]
        if page.endswith('.html'):
            page = page[:-5]

    elif path.startswith('/ems/'):
        page = '/EMS/' + path[5:]
        if page.endswith('.html'):
            page = page[:-5]

    elif path.startswith('/Mathematicians/'):
        page = '/Biographies/' + path[16:]
        if page.endswith('.html'):
            page = page[:-5]

    elif path.startswith('/Ledermann/'):
        page = path
        if path.endswith('index.html'):
            page = page[:-10]
        elif page.endswith('.html'):
            page = page[:-5]

    elif path.startswith('/Projects/Daxenberger/'):
        page = path
        if path.endswith('index.html'):
            page = page[:-10]
        elif page.endswith('.html'):
            page = page[:-5]

    elif path.startswith('/Curvepics/'):
        curve = path[11:]
        pattern = re.compile(r'(?<=\D+)(\d)(?=.gif)')
        match = pattern.search(curve)
        if match:
            curve = re.sub(pattern, r'0\1', curve)
        page = '/Curves/%s' % curve

    else:
        page = path
        with open('url-conversion-non.txt', 'a') as f:
            f.write('%s :: %s :: %s\n' % (page, url_context, original_href))

    if fragment.strip() != '':
        page += '#' + fragment

    return page
