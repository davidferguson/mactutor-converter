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

    if href.endswith(' "'):
        href = href[:-2]

    # generate the current context url
    base_url = urljoin('https://www-history.mcs.st-andrews.ac.uk/', url_context)

    href = href.strip()
    href = href.replace('" target=_blank', '')
    href = href.replace('target=_blank', '')
    href = href.replace('target=blank_', '')
    href = href.replace('" target="_blank', '')
    href = href.replace('target="_blank', '')
    href = href.replace('height=800', '')
    href = href.replace('" class="tippyPic', '')
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

    # win javascript pattern
    pattern = re.compile(r'^javascript:win\(\'(?P<href>.*?)\'(?:.*?)\)$')
    match = pattern.search(href)
    if match:
        href = '/Obits/%s.html' % match.group('href')

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

    html_directories = ('/Astronomy/','/Biographies/','/Curves/','/Extras/','/HistTopics/','/Honours/','/Quotations/','/Strick/','/Tait/','/Wallace/','/Gaz/','/Ledermann/','/Projects/Daxenberger/','/ICM/')
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

    if path == '/Honours/FRSE.html' or path == '/Societies/FRSE.html':
        path = '/Societies/RSE/FRSE/'
    elif path == '/Honours/FRSEchron.html' or path == '/Societies/FRSEchron.html':
        path = '/Societies/RSE/FRSE/chronological/'

    if path == '/' or path == '/index.html':
        page = '/'

    elif path == '/Astronomy/astronomers.html':
        page = '/Biographies/@categoryindex/astronomy'

    elif path.startswith(html_directories):
        if path.endswith('index.html'):
            page = path[:-10]
        elif path.endswith('.html'):
            page = path[:-5]
        else:
            page = path

    elif path.startswith('escherpic('):
        pattern = re.compile(r'escherpic\(\'(?P<name>.+?)\',(?P<width>\d+?),(?P<height>\d+?)\)')
        match = pattern.search(path)
        if match:
            name = match.group('name')
            width = match.group('width')
            height = match.group('height')
            page = '/Diagrams/Escher_%s.jpeg' % name
        else:
            page = path

    elif path.startswith('/Darcy/'):
        found = False
        still_there = ['cordmath','Darling','marshall','neville','Peddie','plateau','tait','transformation','whitehead']
        for name in still_there:
            name = '/Darcy/%s.html' % name
            if path.startswith(name):
                page = path[:-5]
                found = True
                break
        if not found:

            if path == '/Darcy/index.html':
                page = '/Darcy/'

            # the ms pages have moved to extras, so they appear as popups
            elif path.startswith('/Darcy/ms') and path.endswith('.html'):
                page = '/Extras/%s/' % path[7:-5]

            elif path == '/Darcy/Overview.html':
                page = '/Projects/DickinsonCernokova/chapter-1/'
            elif path == '/Darcy/Heilmann_Shufeldt.html':
                page = '/Projects/DickinsonCernokova/chatper-2/'
            elif path == '/Darcy/Correspondence_I.html':
                page = '/Projects/DickinsonCernokova/chatper-3/'
            elif path == '/Darcy/Correspondence_II.html':
                page = '/Projects/DickinsonCernokova/chatper-4/'
            elif path == '/Darcy/Correspondence_II.html':
                page = '/Projects/DickinsonCernokova/chatper-5/'
            elif path == '/Darcy/Correspondence_VI.html':
                page = '/Projects/DickinsonCernokova/chatper-6/'
            elif path == '/Darcy/Correspondence_V.html':
                page = '/Projects/DickinsonCernokova/chatper-7/'
            elif path == '/Darcy/Correspondence_VI.html':
                page = '/Projects/DickinsonCernokova/chatper-8/'

            elif path == '/Darcy/dwtandmaths.html':
                page = '/Projects/GowenlockTuminauskaite/chatper-1/'
            elif path == '/Darcy/coordinates.html':
                page = '/Projects/GowenlockTuminauskaite/chatper-2/'
            elif path == '/Darcy/log.html':
                page = '/Projects/GowenlockTuminauskaite/chatper-3/'
            elif path == '/Darcy/cells.html':
                page = '/Projects/GowenlockTuminauskaite/chatper-4/'
            elif path == '/Darcy/fidler.html':
                page = '/Projects/GowenlockTuminauskaite/chatper-5/'

            elif path.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                page = '/Diagrams/darcy-%s' % path[7:]
            else:
                print('DARCY URL ERROR: %s' % path)
                page = path

    elif path.startswith('/Societies/'):
        if path.endswith('index.html'):
            page = path[:-10]
        elif path.endswith('.html'):
            page = path[:-5]
        else:
            page = path

        if page == '/Societies/alph_list':
            page = '/Societies/'
        elif page == '/Societies/societies_list/':
            page = '/Miscellaneous/other_indexes/'

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

        # special case for escher HTML pages
        if path.startswith('/Diagrams/Escher_') and path.endswith('.html'):
            page = '/Extras/%s' % path[10:-5]
        else:

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
                    #page = ''
                    page = '/Diagrams/%s' % diagram
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

    elif path.startswith('/Education/'):
        page = path
        if page.endswith('.html'):
            page = page[:-5]
        # fix some links, that are now subdirs
        if page == '/Education/Edinburgh_m_exams':
            page = '/Education/Edinburgh_maths/Edinburgh_m_exams'
        elif page == '/Education/Edinburgh_p_exams':
            page = '/Education/Edinburgh_maths/Edinburgh_p_exams'
        elif page == '/Education/Glasgow_exams':
            page = '/Education/Glasgow_maths/Glasgow_exams'
        elif page == '/Education/St_Andrews_m_exams':
            page = '/Education/St_Andrews_maths/St_Andrews_m_exams'
        elif page == '/Education/St_Andrews_p_exams':
            page = '/Education/St_Andrews_maths/St_Andrews_p_exams'

    elif path.startswith('/Curvepics/'):
        curve = path[11:]
        pattern = re.compile(r'(?<=\D+)(\d)(?=.gif)')
        match = pattern.search(curve)
        if match:
            curve = re.sub(pattern, r'0\1', curve)
        page = '/Curves/%s' % curve

    elif path.startswith('/Search/'):
        page = '/Search/'

    elif path.startswith('/Davis/'):
        # leave it alone for now
        page = path

    elif path == '/Indexes/African_men_alph.html':
        page = '/Biographies/@categoryindex/african-men-alph'
    elif path == '/Indexes/African_women_alph.html':
        page = '/Biographies/@categoryindex/african-women'
    elif path == '/~john/':
        page = 'http://www-groups.mcs.st-and.ac.uk/~john/'
    elif path == '/~edmund/':
        page = 'http://www-groups.mcs.st-and.ac.uk/~edmund/'

    elif path == '/PictDisplay/Somerville.html':
        page = '/Biographies/Somerville/pictdisplay/'
    elif path == 'gdezso@math.ubbcluj.ro':
        page = 'mailto:gdezso@math.ubbcluj.ro'
    elif path == '/Index/Changes.html':
        page = '/Miscellaneous/recent_changes'
    elif path == '/Miscellaneous/About_us.html':
        page = '/Miscellaneous/about_us'
    elif path == '/Java/Sources/Wholecode.html':
        page = '/Miscellaneous/java_code'
    elif path == '/Miscellaneous/FAQ.html':
        page = '/Miscellaneous/faq'
    elif path == '/Miscellaneous/Copyright.html':
        page = '/Miscellaneous/copyright'
    elif path == '/Miscellaneous/Copyright0.html':
        page = '/Miscellaneous/copyright'
    elif path == '/Miscellaneous/Popular.html':
        page = '/Miscellaneous/Popular'
    elif path == '/Miscellaneous/Popular_2009.html':
        page = '/Miscellaneous/Popular_2009'
    elif path == '/Miscellaneous/DArcy_Thompson.html':
        page = '/Darcy/DArcy_Thompson'
    elif path == '/Miscellaneous/darcy.html':
        page = '/Darcy/darcy'
    elif path == '/Comments/makecomment0.html':
        page = '/Miscellaneous/contact_us'

    else:
        page = path
        with open('url-conversion-non.txt', 'a') as f:
            f.write('%s :: %s :: %s\n' % (page, url_context, original_href))
        with open('invalid-urls.txt', 'a') as f:
            f.write('%s\n' % page)

    if fragment.strip() != '':
        page += '#' + fragment

    return page
