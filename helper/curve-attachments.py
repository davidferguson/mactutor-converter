import os
import regex as re
from shutil import copyfile

INPUT_DIR = '/Users/david/Documents/MacTutor/actual-work/from-server/public_html/Curvepics/'
OUTPUT_DIR = '/Users/david/Documents/MacTutor/actual-work/mathshistory-lektor/mathshistory/content/Curves'

def get_description(name):
    if name.endswith('12.gif'):
        return 'Caustic curve wrt another point'
    if name.endswith('11.gif'):
        return 'Caustic wrt horizontal rays'
    if name.endswith('10.gif'):
        return 'Negative pedal wrt another point'
    if name.endswith('9.gif'):
        return 'Negative pedal curve wrt origin'
    if name.endswith('8.gif'):
        return 'Pedal wrt another point'
    if name.endswith('7.gif'):
        return 'Pedal curve wrt origin'
    if name.endswith('6.gif'):
        return 'Inverse wrt another circle'
    if name.endswith('5.gif'):
        return 'Inverse curve wrt origin'
    if name.endswith('4.gif'):
        return 'Involute 2'
    if name.endswith('3.gif'):
        return 'Involute 1'
    if name.endswith('2.gif'):
        return 'Evolute'
    if name.endswith('1.gif'):
        return 'Main'

def process_curve_dir(dir):
    path = os.path.join(INPUT_DIR, dir)

    if not os.path.isdir(path):
        return
    for image in os.listdir(path):
        description = get_description(image)
        is_main = 'no'
        if description == 'Main':
            is_main = 'yes'

        dst = os.path.join(OUTPUT_DIR, dir, image)
        src = os.path.join(INPUT_DIR, dir, image)
        #copyfile(src, dst)

        content = '''_model: curveimage
---
description: %s
---
main: %s''' % (description, is_main)
        with open('%s.lr' % dst, 'w') as f:
            f.write(content)
        #print('writing to', '%s.lr' % out)

#for filename in os.listdir(INPUT_DIR):
#    process_curve_dir(filename)


pattern = re.compile(r'(?<=\D+)(\d)(?=.gif(.lr)?)')
for subdir, dirs, files in os.walk(OUTPUT_DIR):
    for file in files:
        if '.gif' in file:
            match = pattern.search(file)
            if match:
                newname = re.sub(pattern, r'0\1', file)
                os.rename(os.path.join(subdir, file), os.path.join(subdir, newname))
