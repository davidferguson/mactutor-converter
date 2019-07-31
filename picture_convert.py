import os
import glob
import re
from bs4 import BeautifulSoup
import sys
import shutil

import datasheetparser

DATASHEET_FILES = '/Users/david/Documents/MacTutor/actual-work/datasheets/'
SERVER_FILES = '/Users/david/Documents/MacTutor/actual-work/from-server/public_html/history/'
CONTENT_DIR = '/Users/david/Documents/MacTutor/actual-work/lektor-davidferguson/mactutor/content/'

IGNORE_BIGPICS = [
    'Bartlett.jpg',
    'Bonsall.jpg',
    'Boyle_Margaret.jpg',
    'Bukreev.jpg',
    'Darmois.jpg',
    'Davis.jpg',
    'De_Witt.jpg',
    'Diaconis.jpg',
    'Fiedler_Wilhelm.jpg',
    'Kendall_Maurice.jpg',
    'Konig_Samuel.jpg',
    'Nash-Williams.59.jpeg',
    'Plemelj.jpg',
    'Sluze.jpg',
    'Whitehead.jpg'
]


NODE_SKIPTEXT = (
    'JOC/EFR',
    'The URL of this page',
    'Copyright information',
    '/PictDisplay/'
)


def parse_pictdisplay(name):
    pictdisplays_path = os.path.join(DATASHEET_FILES, 'PictDisplay')
    pictdisplay_path = os.path.join(pictdisplays_path, name)

    if not os.path.isfile(pictdisplay_path):
        return False

    # parse the page
    datasheet = datasheetparser.parse_file(pictdisplay_path)
    html = '<table>' + datasheet['CONTENT']
    soup = BeautifulSoup(html, 'html5lib')

    # simplistic way, won't work on Maclaurin, etc.
    images = soup.find_all('img')
    for image in images:
        parent = image.parent
        if parent.name == 'td':
            child_imgs = parent.find_all('img')
            if len(child_imgs) == 1:
                continue
        print('yikes', name, parent.name)


def save_image(dst, src, description, main):
    shutil.copyfile(src, dst)
    content = '''_model: biographyimage
---
description: %s
---
main: %s''' % (description, main)
    with open('%s.lr' % dst, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    biographies_path = os.path.join(DATASHEET_FILES, 'Biographies')
    thumbnails_path = os.path.join(SERVER_FILES, 'Thumbnails')
    bigpictures_path = os.path.join(SERVER_FILES, 'BigPictures')

    biographies_files = os.listdir(biographies_path)
    for name in biographies_files:
        # check if there is a thumbnail file
        thumbnail_path = os.path.join(thumbnails_path, '%s.*' % name)
        thumbnail = glob.glob(thumbnail_path)
        if len(thumbnail) == 0:
            # no thumbnail, so nothing to do
            continue

        # find the big pictures
        bigpictures_paths = os.path.join(bigpictures_path, '%s*' % name)
        bigpictures = glob.glob(bigpictures_paths)
        assert len(bigpictures) > 0

        # one of these is a main picture, find it
        main_pic = None
        actual_bigpictures = []

        for pic in bigpictures:
            pic_name = os.path.basename(pic)
            if pic_name in IGNORE_BIGPICS: continue

            # check this is an actual match
            pattern = re.compile('%s(_?\\d+)?(\\..+)' % re.escape(name))
            match = pattern.search(pic_name)
            if not match:
                continue

            pic_extra = pic_name[len(name):]
            if pic_extra.startswith('.'):
                assert main_pic == None
                main_pic = pic
            else:
                actual_bigpictures.append(pic)

        # for now, ignore all captions
        # this can be solved later, hopefully.

        if main_pic == None:
            if name == 'Etherington':
                main_pic = actual_bigpictures[1]

        # first do the main image
        dst = os.path.join(CONTENT_DIR, 'Biographies/', name, os.path.basename(main_pic))
        save_image(dst, main_pic, '', 'yes')

        # and then the others
        for pic in actual_bigpictures:
            dst = os.path.join(CONTENT_DIR, 'Biographies/', name, os.path.basename(pic))
            save_image(dst, pic, '', 'no')

        print('processed', name)
