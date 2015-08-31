# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 13:28:58 2015

@author: Mahlon Barrault (mahlonbarrault@gmail.com)

This file contains code to validate cleaning done to the Zen Map Calgary Metro
Extract OpenStreetMaps data.
"""


# Instructor Code
def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('DBAAdmin:27017')
    db = client[db_name]
    return db


def make_pipeline():
    pipeline = [
                {'$project': 
                    {'street' : '$address.street'}}           
                ]
    return pipeline

def get_all_docs(db):
    return db.calgary_canada_osm.find({'address.street' : {'$exists' : 1}})

# Instructor Code
def aggregate(db, pipeline):
    result = db.calgary_canada_osm.aggregate(pipeline)
    return result


db = get_db('osm')
#pipeline = make_pipeline()
#result = aggregate(db, pipeline)