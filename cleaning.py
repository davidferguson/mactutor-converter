import regex as re

SPECIAL_RULES = {
    'Al-Battani': [
        ['Tetrabiblos.\n<a href=http://www.britannica.com/biography/al-Battani>','</Q>'],
        ['<a href=http://www.britannica.com/biography/al-Battani>','']
    ],
    'Ambartsumian': [
        ['Stages of life and scientific concepts</i> (Russian) (Moscow, 2011).','<i>Stages of life and scientific concepts</i> (Russian) (Moscow, 2011).']
    ]
}


def clean(bio, name):
    # special case for the common issue
    if bio == "Papers in the Proceedings of the EMS</i>":
        return "Papers in the Proceedings of the EMS"
    if bio == "Papers in the Proceedings and Notes of the EMS</i>":
        return "Papers in the Proceedings and Notes of the EMS"

    # run all the special rules
    if name in SPECIAL_RULES:
        rules = SPECIAL_RULES[name]
        for rule in rules:
            bio = bio.replace(rule[0], rule[1])

    # remove these as they have no BBCode equivalent
    bio = bio.replace('<br clear=right>', '')
    bio = bio.replace('<p align=justify>', '')
    bio = bio.replace('<p align=right>', '')

    # fix line breaks for list items
    bio = bio.replace('\n\n<li', '\n<li')

    return bio
