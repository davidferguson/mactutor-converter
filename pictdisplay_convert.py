import os
import re
import shutil

# this file is safe to run multiple times
# once the new biographies are added, just run this again
# .... and we'll also need to do the thumbnails for them, which is picture_convert.py

import datasheetparser
import htmlparser

import lektor.metaformat

DATASHEET_DIR = '/Users/david/Documents/MacTutor/actual-work/datasheets/'
CONTENT_DIR = '/Users/david/Documents/MacTutor/actual-work/dev/mathshistory-site/content/'
SERVER_FILES = '/Users/david/Documents/MacTutor/actual-work/from-server/2/history/'

def strip_br(source):
    while source.startswith('<br>'):
        source = source[4:]
        source = source.strip()
    while source.endswith('<br>'):
        source = source[:4]
        source = source.strip()
    return source

if __name__ == '__main__':
    pictures_datasheets = os.path.join(DATASHEET_DIR, 'PictDisplayCaptions')

    pictures_datasheets_files = os.listdir(pictures_datasheets)
    for name in pictures_datasheets_files:
        order = 1
        print('processing %s' % name)
        path = os.path.join(pictures_datasheets, name)
        datasheet = datasheetparser.parse_file(path)

        content = datasheet['CONTENT']
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            pattern = re.compile(r'^(?P<position>[SCLR]),(?P<path>.+?),(?P<height>.+?)(?:,(?P<description>.*))?$')
            match = pattern.search(line)
            if not match:
                print('not a match! (%s), (%s)' % (name, line))
                assert False
            position = match.group('position')
            path = match.group('path')
            height = match.group('height')
            description = match.group('description') or ''

            description = strip_br(description)

            # parse the description
            description = htmlparser.parse(description,
                                        'PictDisplay/%s' % name,
                                        paragraphs=False,
                                        url_context='PictDisplay/%s' % name)

            description = strip_br(description)

            # check this person exists
            biography_dir = os.path.join(CONTENT_DIR, 'Biographies/', name)
            if not os.path.isdir(biography_dir):
                with open('not-exists.txt', 'a') as f:
                    f.write('%s\n' % name)
                    continue

            # copy that image in
            img_dst = os.path.join(biography_dir, os.path.basename(path))
            img_src = os.path.join(SERVER_FILES, path)

            if not os.path.isfile(img_src):
                continue

            # copy the image to the mathematician's directory
            shutil.copyfile(img_src, img_dst)

            # make the lektor content file
            data = {
                '_model': 'biographyimage',
                'main': 'no',
                'description': description,
                'position': position,
                'height': height,
                'order': str(order)
            }

            items = list(data.items())
            lektordata = lektor.metaformat.serialize(items)

            contents_file = '%s.lr' % img_dst
            with open(contents_file, 'wb') as f:
                    for chunk in lektor.metaformat.serialize(items, encoding='utf-8'):
                        f.write(chunk)

            # increment order
            order += 1
