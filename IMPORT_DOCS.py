#!/usr/bin/python
# -*- coding: utf-8 -*-

# Programma per spostare i file json di tweet dentro mongo DB
# Versione 1.0
# Sviluppi futuri:
#		indicare programmaticamente db e collezione, possibilmente scegliendo da una lista fornita dal programma
#		inserire nel documento la data di inserimento e la/e parola/e chiave della ricerca

import sys
import json
import os
import shutil
import pymongo
import config

from datetime import datetime
from pymongo.errors import ConnectionFailure
from pymongo.errors import BulkWriteError
from pymongo.errors import DuplicateKeyError
from IMPORTAZIONE_TWIT_FUNZIONI import UPDATE_DATE_FIELD

def CREATE_INDEX(mydb , field , index_name , unique_value):
    try:
        mydb.create_index(field , name=index_name , unique=unique_value)

    except DuplicateKeyError as e:
        print('Skip indexing for duplicated key error: {}'.format(e))


def IMPORT_DOCS_IN_MONGO(doc , mydb , doc_name):
    #	print type (data)

    updated_doc = UPDATE_DATE_FIELD (doc)

    try:
        mydb.insert_many(updated_doc , ordered=False)
        print('Successfully inserted document: {}'.format(doc_name))

    except BulkWriteError as bwe:
        print("Skipped duplicate keys")


def CONNECT_MONGODB(db , collection):

    try:
        c = pymongo.MongoClient(host="192.168.0.244" , port=27017)
    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)

    config.connessione_mongodb = True

    mydb = c[db][collection]

    return mydb
