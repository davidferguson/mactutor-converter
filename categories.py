import os
import re
import json

mathematicians_pattern = re.compile(r'\/(?:Mathematicians|Biographies)\/(.+?).html')
histtopics_pattern = re.compile(r'\/HistTopics\/(.+?).html')

CATEGORY_DIR = '../datasheets/Indexes/'
CATEGORY_DIR = '/Users/david/Documents/MacTutor/actual-work/from-server/2/history/Indexes/'
FILES = [(f, os.path.join(CATEGORY_DIR, f)) for f in os.listdir(CATEGORY_DIR)]
FILES.append(('astronomy','/Users/david/Documents/MacTutor/actual-work/from-server/2/history/Astronomy/astronomers.html'))

def categories():
    global categories_cache
    if categories_cache == None:
        generate_categories()
    return categories_cache

categories_cache = None
def generate_categories():
    global categories_cache
    categories = []
    names = []

    #for name in os.listdir(CATEGORY_DIR):
    #    path = os.path.join(CATEGORY_DIR, name)
    for name, path in FILES:
        if not os.path.isfile(path):
            continue

        parsedname = name.replace('.html', '').replace('_','-').lower()
        if parsedname == 'greek-index':
            parsedname = 'greeks'

        new = False
        if parsedname in names:
            i = names.index(parsedname)
            category = categories[i]
        else:
            category = {
                'name': name.replace('.html', '').replace('_','-').lower(),
                'entries': []
            }
            new = True

        if category['name'] in ('african-all-alph','african-men-alph','african-women','-500-ad', 'african-by-countries','african-women-alph','american','changes','changes-old','eminger','fname','full-alph','full-chron','hist-topics-alph','historytopics','ij','ma','others','pq','test','uv','xyz'):
            continue
        if category['name'].replace('-','').isdigit():
            continue
        if len(category['name']) == 1:
            continue
        if category['name'].endswith('-pics'):
            continue
        if category['name'] == 'greek-index':
            category['name'] = 'greeks'

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

        if len(category['entries']) > 0 and new:
            categories.append(category)
            names.append(parsedname)

    #print(json.dumps(categories, indent=2))
    categories_cache = categories


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


categories()
#alphabetical()
