import json
import glob
import os
import shutil

CONTENT_DIR = '/Users/david/Documents/MacTutor/actual-work/dev/mathshistory-site/content/'
SERVER_DIR = '/Users/david/Documents/MacTutor/actual-work/from-server/public_html/'

with open('moved_array.json', 'r') as f:
    moved_array = json.load(f)

miscellaneous_dir = os.path.join(SERVER_DIR, 'Miscellaneous/')
print(miscellaneous_dir)
for filename in glob.iglob(miscellaneous_dir + '**/*', recursive=True):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        path = filename.replace(SERVER_DIR, '/')
        for item in moved_array:
            move_from = item['from']
            move_to = item['to']
            if path.startswith(move_from):
                new_path = path.replace(move_from, move_to)
                if new_path.startswith('/'):
                    new_path = new_path[1:]
                new_filename = os.path.join(CONTENT_DIR + new_path)
                # copy the file
                shutil.copyfile(filename, new_filename)
                #print(new_filename)
