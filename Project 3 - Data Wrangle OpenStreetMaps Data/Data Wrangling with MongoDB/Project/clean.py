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

OSMFILE = "calgary_canada.osm"
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


# Clean Street Names

# split on comma, take 0th item
# check for direction suffix
#   clean suffix
#   save cleaned suffix to var
#   check for street type in street name with suffix removed
#   clean street type
# append suffix to cleaned street name