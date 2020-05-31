# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json
import re

import htmlparser
import referenceparser
import symbolreplace
import flow

SPEAKERS_PATH = '/Users/david/Documents/MacTutor/actual-work/datasheets/BMC/speakers/'
speakers_data_raw = {}
for t in ['dates', 'mlinks', 'names', 'talks', 'types']:
    with open(os.path.join(SPEAKERS_PATH, t), 'r',  encoding='mac_roman') as f:
        speakers_data_raw[t] = f.read().split('\n')
# check validity
assert len(speakers_data_raw['dates']) == len(speakers_data_raw['mlinks'])
assert len(speakers_data_raw['dates']) == len(speakers_data_raw['names'])
assert len(speakers_data_raw['dates']) == len(speakers_data_raw['talks'])
assert len(speakers_data_raw['dates']) == len(speakers_data_raw['types'])
# transform it
speakers_data = {}
for i in range(0, len(speakers_data_raw['dates'])):
    date = speakers_data_raw['dates'][i].strip()
    mlink = speakers_data_raw['mlinks'][i].strip()
    name = speakers_data_raw['names'][i].strip()
    talk = speakers_data_raw['talks'][i].strip()
    type = speakers_data_raw['types'][i].strip()
    if date == '':
        break
    if date not in speakers_data:
        speakers_data[date] = []
    speakers_data[date].append({
        'date': date,
        'mlink': mlink,
        'name': name,
        'talk': talk,
        'type': type
    })


def get_speakers(type, year):
    speakers = []
    if not year in speakers_data:
        return flow.to_flow_block('bmcspeaker', [])
    all_speakers = speakers_data[year]
    for speaker in all_speakers:
        if speaker['type'] == type:
            speakers.append({
                'mlink': speaker['mlink'],
                'talk': speaker['talk'],
                'name': speaker['name']
            })
    d = flow.to_flow_block('bmcspeaker', speakers)
    return d


def convert(datasheet, url_context):
    data = {}

    # metadata, the template and model
    data['_model'] = 'bmc'
    data['_template'] = 'bmc.html'

    # easily translatable info
    data['place'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['PLACE']))
    data['date'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['PLACE']))
    data['year'] = datasheet['YEAR']
    data['size'] = datasheet['SIZE']
    data['organisers'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['ORGANISERS']))
    data['chair'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['CHAIR']))
    data['secretary'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['SECRETARY']))
    data['partner'] = symbolreplace.strip_tags(symbolreplace.tags_to_unicode(datasheet['PARTNER']))

    if data['chair'] == data['organisers']:
        data['organisers'] == ''

    # now the speakers
    speakers = []

    # do plenary speakers
    pspeakers = {
        'speakers': get_speakers('p', data['year']),
        'title': 'The plenary speakers were:',
        'type': 'Ap'
    }
    if pspeakers['speakers'] != '':
        speakers.append(pspeakers)

    # do morning speakers
    mspeakers = {
        'speakers': get_speakers('m', data['year']),
        'title': 'The morning speakers were:',
        'type': 'Bm'
    }
    if mspeakers['speakers'] != '':
        speakers.append(mspeakers)

    # do special speakers
    for i in range(0, 9):
        title = datasheet['SPECIALTITLE%s' % i]
        if title == '':
            continue
        sspeakers = {
            'speakers': get_speakers('s%s' % i, data['year']),
            'title': title,
            'type': 'Cs'
        }
        speakers.append(sspeakers)

    # need to parse the individual equations out, and convert to flow
    data['speakertypes'] = flow.to_flow_block('bmcspeakertype', speakers)

    # add in links to minutes of meetings
    links = []
    if data['year'] == '1976':
        links.append({
            'text': 'G',
            'page': 'Gminutes%s' % data['year']
        })
        links.append({
            'text': 'C<sub>1</sub>',
            'page': 'Sminutes%s' % data['year']
        })
        links.append({
            'text': 'C<sub>2</sub>',
            'page': 'Cminutes%s' % data['year']
        })
    elif int(data['year']) < 1994:
        links.append({
            'text': 'G',
            'page': 'Gminutes%s' % data['year']
        })
        links.append({
            'text': 'C',
            'page': 'Cminutes%s' % data['year']
        })
    elif data['year'] == '1994':
        links.append({
            'text': 'G',
            'page': 'Gminutes%s' % data['year']
        })
        links.append({
            'text': 'SubC',
            'page': 'SubCminutes%s' % data['year']
        })
        links.append({
            'text': 'SC',
            'page': 'SCminutes%s' % data['year']
        })
    elif int(data['year']) < 2002 and data['year'] != '1999':
        links.append({
            'text': 'G',
            'page': 'Gminutes%s' % data['year']
        })
        links.append({
            'text': 'SC',
            'page': 'SCminutes%s' % data['year']
        })
    elif data['year'] == '1999' or int(data['year']) < 2019:
        links.append({
            'text': 'G',
            'page': 'Gminutes%s' % data['year']
        })
        links.append({
            'text': 'SC<sub>1</sub>',
            'page': 'SCminutes%sa' % data['year']
        })
        links.append({
            'text': 'SC<sub>2</sub>',
            'page': 'SCminutes%sb' % data['year']
        })

    # check they all go to valid pages
    with open('bmcarray.json', 'r') as f:
        bmcdata = json.load(f)
    pages = []
    for year,page in bmcdata:
        if year == data['year']:
            pages.append(page)
    for link in links:
        if link['page'] not in pages:
            print('ERROR: %s not in %s' % (link['page'], pages))
    data['indexlinks'] = flow.to_flow_block('bmcindexlink', links)

    return data
