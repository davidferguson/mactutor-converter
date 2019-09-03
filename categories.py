import os
import re
import json

mathematicians_pattern = re.compile(r'\/(?:Mathematicians|Biographies)\/(.+?).html')
histtopics_pattern = re.compile(r'\/HistTopics\/(.+?).html')

CATEGORY_DIR = '../datasheets/Indexes/'

def categories():
    categories = []

    for name in os.listdir(CATEGORY_DIR):
        path = os.path.join(CATEGORY_DIR, name)
        if not os.path.isfile(path):
            continue
        category = {
            'name': name.replace('.html', '').replace('_','-').lower(),
            'entries': []
        }
        with open(path, 'r', encoding='mac_roman') as f:
            data = f.read()

        for match in re.finditer(mathematicians_pattern, data):
            name = match.group(1)
            name = '/Biographies/%s' % name
            if name != 'index' and name not in category['entries']:
                category['entries'].append(name)

        for match in re.finditer(histtopics_pattern, data):
            name = match.group(1)
            name = '/HistTopics/%s' % name
            if name != 'index' and name not in category['entries']:
                category['entries'].append(name)

        if len(category['entries']) > 0:
            categories.append(category)

    print(json.dumps(categories, indent=2))


def alphabetical():
    dir = os.path.join(CATEGORY_DIR, 'alphabet')
    categories = []

    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if not os.path.isfile(path):
            continue
        category = {
            'name': name.replace('.html', '').replace('_','-').lower(),
            'entries': []
        }
        with open(path, 'r', encoding='mac_roman') as f:
            data = f.read()

        for match in re.finditer(mathematicians_pattern, data):
            name = match.group(1)
            name = '/Biographies/%s' % name
            if name != 'index' and name not in category['entries']:
                category['entries'].append(name)

        if len(category['entries']) > 0:
            categories.append(category)

    print(json.dumps(categories, indent=2))


#categories()
alphabetical()
