#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it, clean it, 
come up with a data model, insert it into a MongoDB and then run some queries against your database.
The set contains data about Arachnid class.
Your task in this exercise is to parse the file, process only the fields that are listed in the
FIELDS dictionary as keys, and return a dictionary of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label' field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the cleanup is up to you,
  eg removing "*" prefixes etc
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:
{ 'label': 'Argiope',
  'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
  'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
  'name': 'Argiope',
  'synonym': ["One", "Two"],
  'classification': {
                    'family': 'Orb-weaver spider',
                    'class': 'Arachnid',
                    'phylum': 'Arthropod',
                    'order': 'Spider',
                    'kingdom': 'Animal',
                    'genus': None
                    }
}
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}

def remove_duplicates(entry):
    # This function trims out redundant description in parenthesis from like "(spider)"
    startp = 0
    endp = 0
    new_entry = entry
    if (startp != -1):
        startp = entry.find('(', startp)
        endp = entry.find(')', endp)
        # Subtract 1 from startp to remove space and add 1 to endp to remove last ')'
        new_entry = new_entry.replace(new_entry[startp-1:endp+1],'')
    return new_entry

def change_to_list(entry):
    # If there is a value in 'synonym', it should be converted to a list
    contents = entry.strip('{}').split('|')
    # Remove leading/trailing * and spaces
    for i in range(0,len(contents)):
        contents[i] = contents[i].strip('* ')
    return contents

def process_file(filename, fields):

    process_fields = fields.keys()
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            entry = {}
            entry['classification'] = {}
            for key in line.keys():
                # Keys of the dictionary changed according to the mapping in FIELDS dictionary
                if key in FIELDS:
                    #strip leading and ending whitespace from all fields, if there is any
                    info = line[key].strip()
                    # If a value of a field is "NULL", convert it to None
                    if (line[key] == 'NULL'):
                        info = None
                    if FIELDS[key] in ['family','class', 'phylum','order', 'kingdom', 'genus']:
                        entry['classification'][FIELDS[key]] = info
                    else:
                        entry[FIELDS[key]] = info
            # Remove info in ()
            entry['label'] = remove_duplicates(entry['label'])
            # If 'name' is "NULL" or contains non-alphanumeric characters, set it to the same value as 'label'.
            if (entry['name'] == None) or (not entry['name'].isalnum()):
                entry['name'] = entry['label']
            # If there is a value in 'synonym', it should be converted to a list
            if (entry['synonym'] != None):
                entry['synonym'] = change_to_list(entry['synonym'])
            data.append(entry)
    return data


def parse_array(v):
    if (v[0] == "{") and (v[-1] == "}"):
        v = v.lstrip("{")
        v = v.rstrip("}")
        v_array = v.split("|")
        v_array = [i.strip() for i in v_array]
        return v_array
    return [v]


def test():
    data = process_file(DATAFILE, FIELDS)
    # pprint.pprint(data[0])
    assert data[0] == {
                        "synonym": None,
                        "name": "Argiope",
                        "classification": {
                            "kingdom": "Animal",
                            "family": "Orb-weaver spider",
                            "order": "Spider",
                            "phylum": "Arthropod",
                            "genus": None,
                            "class": "Arachnid"
                        },
                        "uri": "http://dbpedia.org/resource/Argiope_(spider)",
                        "label": "Argiope",
                        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
                    }


if __name__ == "__main__":
    test()