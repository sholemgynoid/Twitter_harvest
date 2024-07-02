#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Passi di: Matthew A. Russell. “Mining the Social Web”. iBooks. 

import json
import pymongo
from Harvest_User_Timeline import save_json
from Harvest_User_Timeline import read_json

def save_to_mongo (data, mongo_db, mongo_db_coll, **mongo_conn_kw):

    client = pymongo.MongoClient (**mongo_conn_kw)

    db = client [mongo_db]

    coll = db [mongo_db_coll]

    return coll.insert (data)

def load_from_mongo (mongo_db, mongo_db_coll, return_cursor = False, criteria = None, projection = None, **mongo_conn_kw):

    # Optionally, use criteria and projection to limit the data that is
    # returned as documented in
    # http://docs.mongodb.org/manual/reference/method/db.collection.find/
    
    # Consider leveraging MongoDB's aggregations framework for more
    # sophisticated queries.
    
    client = pymongo.MongoClient (**mongo_conn_kw)
    
    db = client [mongo_db]
    
    coll = db [mongo_db_coll]
    
    if criteria is None:
        criteria = {}

    if projection is None:
        cursor = coll.find (criteria)
    else:
        cursor = coll.find (criteria, projection)

    # Returning a cursor is recommended for large amounts of data
    
    if return_cursor:
        return cursor
    else:
        return [item for item in cursor]

file = raw_input ("Nome file da importare: ")

result = read_json (file)

print (result)

save_to_mongo (result, 'tweet_2013', 'direttori_gaia')
