import json
import glob
import os
import shutil
import regex as re
import lektor.metaformat

DATASHEET_DIR = '/Users/david/Documents/MacTutor/actual-work/datasheets/'
CONTENT_DIR = '/Users/david/Documents/MacTutor/actual-work/dev/mathshistory-site/content/'
SERVER_FILES = '/Users/david/Documents/MacTutor/actual-work/from-server/2/history/'

dir = os.path.join(SERVER_FILES, 'Honours','Parismaps/')
for filename in glob.iglob(dir + '*.html'):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', 'index.html', 'xx.html')):
        continue

    with open(filename, 'r') as f:
        data = f.read()

    filename = os.path.basename(filename).replace('.html', '')

    pattern = re.compile(r'google\.maps\.LatLng\((?P<lat>-?\d+\.\d+),(?P<long>-?\d+\.\d+)\)')
    match = pattern.search(data)
    if not match:
        assert False

    lat = match.group('lat')
    long = match.group('long')

    pattern = re.compile(r'<h2>(?P<name>.+?)</h2>')
    match = pattern.search(data)
    if not match:
        print(filename)
        assert False

    name = match.group('name')

    data = {
        '_model': 'parismap',
        'latitude': lat,
        'longitude': long,
        'name': name
    }

    items = list(data.items())
    lektordata = lektor.metaformat.serialize(items)

    dir = os.path.join(CONTENT_DIR, 'Parismaps', filename)
    if not os.path.isdir(dir):
        os.mkdir(dir)

    contents_file = os.path.join(dir, 'contents.lr')
    with open(contents_file, 'wb') as f:
        for chunk in lektor.metaformat.serialize(items, encoding='utf-8'):
            f.write(chunk)
