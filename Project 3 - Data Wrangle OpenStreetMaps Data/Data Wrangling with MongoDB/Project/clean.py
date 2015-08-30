# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 16:18:44 2015

@author: Mahlon Barrault (mahlonbarrault@gmail.com)

This file contains the code to clean the Map Zen Calgary Metro Area
OpenStreetMaps data extract. This code will output a cleaned JSON file that can
be imported in to MongoDB for further analysis
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs
import json

OSMFILE = "calgary_canada.osm"

# RegEx for various key validations
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# These values were collectect from audit.py. They are the values that were not
# present in the list of acceptable street types.
ST_TYPE_MAPPING = { "St": "Street",
                   "St.": "Street",
                   'street' : 'Street',
                   "Rd." : 'Road',
                   'Ave' : "Avenue",
                   'Cres' : 'Crescent',
                   'Blvd' : 'Boulevard',
                   'Blvd.' : 'Boulevard'
                   }
# These values were collected from audit.py. They represent all of the
# inconsistancies in the direction suffixes.
DIR_MAPPING = {'East' : 'E',
               'N.E.' : 'NE',
               'N.E' : 'NE',
               'N.W' : 'NW',
               'N.W.' : 'NW',
               'North' : 'N',
               'Northeast' : 'NE',
               'Northwest' : 'NW',
               'S.E' : 'SE',
               'S.E.' : 'SE',
               'S.W' : 'SW',
               'S.W.' : 'SW',
               'South' : 'S',
               'South-west' : 'SW',
               'Southeast' : 'SE',
               'Southwest' : 'SW',
               'West' : 'W'
               }
            
ST_TYPE_EXPECTED = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons", 'Terrace',
            'Way', 'Rise', 'Point', 'Plaza', 'Park', 'Landing', 'Hollow',
            'Highway', 'Gate', 'Crescent', 'Close', 'Bay', 'Manor', 'Circle']
            
DIR_EXPECTED = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']

#CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

# Clean Street Names

# split on comma, take 0th item
# check for direction suffix
#   clean suffix
#   save cleaned suffix to var
#   check for street type in street name with suffix removed
#   clean street type
# append suffix to cleaned street name


def shape_base(element):
    
    node = defaultdict()    
    
    created_keys = ["version", "changeset", "timestamp", "user", "uid"]
    root_keys = ['id', 'visible']    
    
    node['type'] = element.tag
    node['created'] = defaultdict()
    
    # Probably could use the .get() method on element here
    if 'lat' in element.attrib and 'lon' in element.attrib:
        node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]       

    # http://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops-in-python    
    for k, v in (element.attrib).iteritems():
        if k in created_keys:
            node['created'][k] = v
        elif k in root_keys:
            node[k] = v
            
    return shape_node(node, element)
    

def regex_key(k):
    l = lower.search(k)
    lc = lower_colon.search(k)
    pc = problemchars.search(k)

    return l, lc, pc


def shape_node(node, element):
    
    node_refs = []
    address = defaultdict()    
    
    for t in element:
        k = t.attrib.get('k')
        v = t.attrib.get('v')
        r = t.attrib.get('ref')
        
        if k:
            l, lc, pc = regex_key(k)       
            if pc == None:
                if k.startswith('addr'):
                    if lc:
                        # FIXME The v in this line need to be run through data 
                        # cleaning for street types
                        address[k.split(':')[1]] = v
                    else:
                        continue
                else:
                    node[k] = v
        if r:
            node_refs.append(r)
            
        if len(address) > 0:
            node['address'] = address
        if len(node_refs) > 0:
            node['node_refs'] = node_refs
    return node


def shape_element(element):
    node = {}
    
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node = shape_base(element)
        
        return dict(node)
    else:
        return None


# http://stackoverflow.com/questions/3543559/python-regex-match-and-replace
def process_match(m):
    if ST_TYPE_MAPPING.get(m.group()) != None:
        return ST_TYPE_MAPPING.get(m.group())
    else:
        return m.group()
    return 


def update_name(name): 
    return street_type_re.sub(process_match, name)
    
# Instructor Code
def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data