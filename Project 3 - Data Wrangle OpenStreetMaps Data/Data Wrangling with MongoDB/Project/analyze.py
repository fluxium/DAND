# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 13:28:58 2015

@author: Mahlon Barrault (mahlonbarrault@gmail.com)

This file contains the code to clean the Map Zen Calgary Metro Area
OpenStreetMaps data extract. This code will output a cleaned JSON file that can
be imported in to MongoDB for further analysis
"""

# Instructor Code
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('DBAAdmin:27017')
    db = client[db_name]
    return db


def make_pipeline():
    pipeline = []
    return pipeline
 

# Instructor Code
def aggregate(db, pipeline):
    result = db.calgary_canada_osm.aggregate(pipeline)
    return result


db = get_db('osm')
pipeline = make_pipeline()
result = aggregate(db, pipeline)