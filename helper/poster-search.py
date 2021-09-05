import re
import glob
import json

INPUT_DIR = '/Users/david/Documents/MacTutor/actual-work/from-server/public_html/Posters/'
pattern = re.compile(r'/Biographies/(?P<name>.*?)\.html')

have_posters = set()

for name in glob.glob(INPUT_DIR + '*.html'):
    with open(name, 'r') as f:
        data = f.read()
    match = pattern.search(data)
    if match:
        name = match.group('name')
        have_posters.add(name)
        print(name)

have_posters_list = list(have_posters)
with open('posters.json', 'w') as f:
    json.dump(have_posters_list, f)
