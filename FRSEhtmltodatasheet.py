import glob
import os
import regex as re
from bs4 import BeautifulSoup

done = {}

DATASHEET_DIR = '/Users/david/Documents/MacTutor/actual-work/datasheets/FRSE/'
BIOGS_DIR = '/Users/david/Documents/MacTutor/actual-work/datasheets/Biographies/'
HTML_DIR = '/Users/david/Documents/MacTutor/actual-work/from-server/2/history/Honours/FRSE/'
FRSE_PAGE = '/Users/david/Documents/MacTutor/actual-work/from-server/2/history/Honours/FRSE.html'

NAME_PATTERN = re.compile(r'<h2><font color=red>(?P<firstname>.+?) <b>(?P<lastname>.+?)</b></font></h2><p>')
NAME_PATTERN_2 = re.compile(r'<h2><font color=red>(?P<name>.+?)</font></h2><p>')
BIRTH_DEATH_PATTERN = re.compile(r'<b>Birth/death dates: </b>(?P<birth>.*?)(?: - (?P<death>.*?)?)?<p>')
BIRTHPLACE_PATTERN = re.compile(r'<b>Birth place: </b>(?P<place>.+?)<p>')
ELECTED_PATTERN = re.compile(r'<b>Elected: </b>(?P<elected>[\d/\? ]+?)<p>')
PROFESSION_PATTERN = re.compile(r'<b>Profession: </b>(?P<profession>.+?)<p>')
FELLOWSHIP_PATTERN = re.compile(r'<b>Type of fellowship: </b>(?<fellowship>.+?)<p>')

BIOGRAPHY_PATTERN_STRING = 'FRSE/NAME_GOES_HERE\\.html.+?<a href=../Mathematicians/(?P<name>.+?).html.+?MacTutor biography</a>'

with open(FRSE_PAGE, 'r') as f:
    frse_data = f.read()

for name in glob.glob(HTML_DIR + '*.html'):
    with open(name, 'r') as f:
        data = f.read()
    filename = os.path.basename(name)[:-5]

    # name
    match = NAME_PATTERN_2.search(data)
    name = match.group('name')

    if name in done:
        # found a duplicate! but which one was right...
        if os.path.isfile(os.path.join(BIOGS_DIR, filename)):
            # we are correct - delete duplicate and run us
            os.remove(os.path.join(DATASHEET_DIR, done[name]))
            print('correct is US')
        elif os.path.isfile(os.path.join(BIOGS_DIR, done[name])):
            # duplicate is correct
            print('correct is DUPLICATE')
            continue

    done[name] = filename

    # birth, death
    match = BIRTH_DEATH_PATTERN.search(data)
    birth = match.group('birth')
    death = match.group('death')
    if birth == '?' or birth == None:
        birth = ''
    if death == '?' or birth == None:
        death = ''

    # birthplace
    match = BIRTHPLACE_PATTERN.search(data)
    birthplace = ''
    if match:
        birthplace = match.group('place')

    # elected
    match = ELECTED_PATTERN.search(data)
    elected = match.group('elected')
    if elected == '?':
        elected = ''
    elected.replace('  /  /', '')

    # profession
    match = PROFESSION_PATTERN.search(data)
    profession = match.group('profession')

    # fellowship
    match = FELLOWSHIP_PATTERN.search(data)
    fellowship = match.group('fellowship')

    # mactutor link
    biography_pattern = re.compile(BIOGRAPHY_PATTERN_STRING.replace('NAME_GOES_HERE', re.escape(filename)))
    match = biography_pattern.search(frse_data)
    biography = ''
    if match:
        biography = match.group('name')
        print('got a biography: %s' % biography)

    #create the datasheet
    datasheet = '''<FILENAME>
%s
</FILENAME>

<NAME>
%s
</NAME>

<BIRTH>
%s
</BIRTH>

<DEATH>
%s
</DEATH>

<BIRTHPLACE>
%s
</BIRTHPLACE>

<ELECTED>
%s
</ELECTED>

<PROFESSION>
%s
</PROFESSION>

<FELLOWSHIP>
%s
</FELLOWSHIP>

<BIOGRAPHY>
%s
</BIOGRAPHY>
''' % (filename, name, birth, death, birthplace, elected, profession, fellowship, biography)

    with open(os.path.join(DATASHEET_DIR, filename), 'w') as f:
        f.write(datasheet)
