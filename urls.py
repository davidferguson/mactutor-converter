import regex as re

def convert(href):
    href = href.replace('" target=_blank', '')
    href = href.replace('target=_blank', '')
    href = href.replace('" target="_blank', '')
    href = href.strip()

    # if a external url, keep it the same
    if href.startswith('http://') or href.startswith('https://') or href.startswith('ftp://') or href.startswith('//'):
        return href

    # if an absolute url, bail out
    if href.startswith('/'):
        assert False

    # try and match the common pattern
    pattern = re.compile(r'^(?:javascript:win1\(\')?\.\./(?P<subdir>.+?)/(?P<file>.+?)(?:\',\d+,\d+\))?$')
    match = pattern.search(href)
    if match:
        subdir = match.group('subdir').strip()
        file = match.group('file').strip()

        now_in_directories = ['Biographies','Extras','HistTopics']
        if subdir in now_in_directories:
            pattern = re.compile(r'^(?P<name>.+)\.html(?:#(?P<anchor>.+))?$')
            match = pattern.search(file)
            if not match:
                print('NO MATCH')
                print(href)
                print(subdir)
                print(file)
            assert match
            name = match.group('name')
            anchor = match.group('anchor')
            file = '%s/' % name
            if anchor:
                file += '#' + anchor

        return '/%s/%s' % (subdir, file)

    print('processing url', href)
    return href
