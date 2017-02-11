import xml.etree.cElementTree as ET
from collections import defaultdict
import string
import re
import pprint

OSMFILE = "philadelphia_pennsylvania.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
direction_re = re.compile(r'\b[NESW]\b\.*', re.IGNORECASE)
postcode_re = re.compile(r'[08|18|19]\S{4}')
state_nat_re = re.compile(r'Nj|Us\sHighway|Us')


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Way", "Pike", "Extension", "Circle"]

mapping = {
            "AVE": "Avenue",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "Blvd": "Boulevard",
            "Blvd.": "Boulevard",
            "Cir": "Circle",
            "Cir.": "Circle",
            "Ct": "Court",
            "Ct.": "Court",
            "Dr": "Drive",
            "E": "East",
            "E.": "East",
            "Ext.": "Extension",
            "Hwy": "Highway",
            "Ln": "Lane",
            "N.": "North",
            "N": "North",
            "ROAD": "Road",
            "Rd": "Road",
            "Rd.": "Road",
            "ST": "Street",
            "Sstreet": "Street",
            "Sreet": "Street",
            "St": "Street",
            "St.": "Street",
            "Steet": "Street",
            "Streetphiladelphia": "Street",
            "Sts.": "Streets",
            "Ter": "Terrace",
            "W": "West",
            "W.": "West",
            "S": "South",
            "S.": "South",
            }

state_national_mapping = {
                            "Us": "U.S. Route",
                            "Us Highway": "U.S. Route",
                            "Nj": "New Jersey",
                        }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(key):
    return (key == 'addr:street')


def is_zip_code(key):
    return (key == 'addr:postcode')


def is_phone_number(key):
    return (key == "phone" or key == 'contact:phone')

def capitalize_name(name):
    name = string.capwords(name)
    m = state_nat_re.search(name)
    if m:
        name = re.sub(state_nat_re, state_national_mapping[m.group()], name)
    return name

def standardize_phone_num(phone_number):
    phone_number = phone_number.translate(None, '()- .')
    if not phone_number.startswith('+'):
        phone_number = "+1" + phone_number
    return phone_number

def standardize_postcode(postcode):
    if len(postcode) != 5:
        m = postcode_re.search(postcode)
        if m:
            postcode = m.group()
    return postcode

postcodes = []
phone_numbers = []

def audit(osmfile):
    osm_file = open(osmfile, 'r')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(OSMFILE, events=('start',)):
        if elem.tag == 'way' or elem.tag == 'node':
            for tag in elem.iter('tag'):
                if is_street_name(tag.attrib['k']):
                    audit_street_type(street_types, tag.attrib['v'])
                if is_zip_code(tag.attrib['k']):
                    if len(tag.attrib['v']) != 5:
                        postcodes.append(tag.attrib['v'])
                if is_phone_number(tag.attrib['k']):
                        phone_numbers.append(tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name):
    name = capitalize_name(name)

    st = street_type_re.search(name)
    st_key = st.group()
    d = direction_re.match(name)
    if st_key in mapping.keys():
        name = re.sub(street_type_re, mapping[st_key], name)

    if d:
        name = re.sub(direction_re, mapping[d.group()], name)

    return name

def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name)
            print name, "=>", better_name

    for postcode in postcodes:
        updated_postcode = standardize_postcode(postcode)
        print postcode, "=>", updated_postcode

    for phone_number in phone_numbers:
        updated_phone_number = standardize_phone_num(phone_number)
        print phone_number, "=>", updated_phone_number






if __name__ == '__main__':
    test()
