# -*- coding: utf-8 -*-

# main converter file, converts datasheet to Lektor format

import glob
import os
import json

import lektor.metaformat

import datasheetparser
import biographyparser
import referenceparser

FILEPATH = '../Datasheets'


def convert(datasheet):
    data = {}

    # main part. parse biography
    bio = biographyparser.parse(datasheet['BIOGRAPHY'])
    data['biography'] = bio

    # parse references
    references = referenceparser.parse_references(datasheet['REFERENCES'])
    data['references'] = references

    # parse cross references
    xrefs = referenceparser.parse_cross_references(datasheet['XREFS'])
    data['xrefs'] = xrefs

    # parse additional links
    additional = referenceparser.parse_cross_references(datasheet['ADDITIONAL'])
    data['additional'] = additional

    # parse honours links
    honours = referenceparser.parse_cross_references(datasheet['ADDITIONAL'])
    data['honours'] = honours

    return data


def save(data, fs_path):
    # transorm data from key-values to list of tuples
    items = list(data.items())
    lektordata = lektor.metaformat.serialize(items)

    for chunk in lektor.metaformat.serialize(items, encoding='utf-8'):
        print(chunk)

    #with open(fs_path, 'wb') as f:
    #        for chunk in lektor.metaformat.serialize(items, encoding='utf-8'):
    #            f.write(chunk)



if __name__ == '__main__':
    # get all the files that need to be processed
    path = os.path.join(FILEPATH, '*')
    files = glob.glob(path)

    # process all the files
    for file in files:
        # parse sections from datasheet
        datasheet = datasheetparser.parse_file(file)

        # convert the datasheet to dictionary
        data = convert(datasheet)

        # save the dictionary in lektor
        save(data, filepath)
