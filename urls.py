import regex as re
from urllib.parse import urljoin, urlparse

def convert(href, url_context):
    original_href = href

    # generate the current context url
    base_url = urljoin('https://www-history.mcs.st-andrews.ac.uk/', url_context)

    href = href.replace('" target=_blank', '')
    href = href.replace('target=_blank', '')
    href = href.replace('" target="_blank', '')
    href = href.strip()

    pattern = re.compile(r'^https?://www-history.mcs.st-and(?:rews)?.ac.uk(?P<page>.*)$')
    match = pattern.search(href)
    if match:
        # this is an external link that goes to us! convert to absolute
        href = match.group('page')

    # if a external url, return it
    if href.startswith('http://') or href.startswith('https://') or href.startswith('ftp://') or href.startswith('//'):
        return href

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

    # win1 javascript pattern
    pattern = re.compile(r'^javascript:win1\(\'(?P<href>.*?)\'(?:.*?)\)$')
    match = pattern.search(href)
    if match:
        href = match.group('href')

    # now convert the href to an absolute mactutor link
    href_full = urljoin(base_url, href)

    # and parse it into path and fragment
    parsed = urlparse(href_full)
    path = parsed.path
    fragment = parsed.fragment

    html_directories = ('/Biographies/','/Extras/','/HistTopics/', '/Honours/', '/Societies/', '/Quotations/')
    if path.startswith(html_directories):
        if path.endswith('.html'):
            page = path[:-5]
        else:
            page = path
    elif path.startswith('/Obits2/'):
        page = '/Obituaries/' + path[8:]
        if page.endswith('.html'):
            page = page[:-5]
    else:
        page = path

    if fragment.strip() != '':
        page += '#' + fragment

    with open('url-conversion.txt', 'a') as f:
        f.write('%s , %s:: %s\n' % (original_href, url_context, page))

    return page
