#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint



def parse_map(filename):
    '''Returns a dictionary of element tags as keys and a list of element
    attribute keys.

    '''

    tags={}
    for event, elem in ET.iterparse(filename, events = ('start', 'end')):
        if event == 'start':
            tags[elem.tag] = elem.keys()
            print elem.attrib
    return tags

def parse():

    tags = parse_map('philadelphia_pennsylvania_sample_area.osm')
    pprint.pprint(tags)

if __name__ == '__main__':
    parse()
