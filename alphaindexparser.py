import re

import symbolreplace
import urls

letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def purge_mlink(s):
    #The below code is modified from the original htmlformat function to ensure compatibility
    rawch   = ['á','à','â','ä','ã','Á','Â','Ä','é','è','ê','ë','É','î','í','ó','ô','ö','ò','õ','Ö','û','ú','ü','ù','Ü','ç','ï','ø','Ø','ñ','ł','Ł','ś','Ś','ț','Ț']
    transch = ['a','a','a','a','a','A','A','A','e','e','e','e','E','i','i','o','o','o','o','o','O','u','u','u','u','U','c','i','o','O','n','l','L','s','S','t','T']
    for idx, raw in enumerate(rawch):
        trans = transch[idx]
        s = s.replace(raw, trans)
    return s

def get_displays(find_name):
    displays = []

    for letter in letters:
        # read the data
        filepath = '../datasheets/AlphaIndex/%s' % letter
        with open(filepath, 'r', encoding='mac_roman') as f:
            lines = f.readlines()

        # parse each line
        for line in lines:
            line = line.strip()
            if line == '':
                continue

            # extract the name out of this line
            pattern = re.compile(r'^(?P<pretext>.*?)<(?:w|m)(?:\s+(?P<name>.+?))?>(?P<text>.*?)\<\/(?:w|m)\>(?P<posttext>.*?)$')
            match = pattern.search(line)
            assert match

            # get text
            pretext = match.group('pretext') or ''
            text = match.group('text')
            posttext = match.group('posttext')
            text = pretext + text + posttext
            text = symbolreplace.tags_to_unicode(text)
            text = symbolreplace.strip_tags(text)
            text = text.strip()

            # get name
            name = match.group('name') or match.group('text')
            name = urls.biography_rename(name)

            # check text begins with this letter
            assert purge_mlink(text[0]).lower() == letter.lower(), 'not match: %s != %s' % (purge_mlink(text[0]).lower(), letter.lower())

            if name == find_name:
                displays.append(text)

    # check for (and remove) duplicates
    if len(displays) != len(set(displays)):
        with open('duplicate-displays.txt', 'a') as f:
            f.write('%s :: %s\n' % (find_name, displays))
        displays = list(set(displays))

    missing_list = ['Moriarty']
    if len(displays) == 0 and find_name not in missing_list:
        print('No displays found for %s' % find_name)
        return False

    displays.sort()
    return displays



if __name__ == '__main__':
    # simple test
    print(get_displays('Zu_Geng'))
    print(get_displays("De_LHopital"))
