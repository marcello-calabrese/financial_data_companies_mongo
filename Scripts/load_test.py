import pymongo
from pymongo import MongoClient
import pandas as pd
import json

client = MongoClient('mongodb+srv://Marce82:Lorenzo_22@cluster0.ragcpnf.mongodb.net/?retryWrites=true&w=majority')

# Get an existing database named "yahoo_testdb"
db1 = client.yahoo_testdb

# Get a collection named "Seattle_listing"
collection_main = db1.yahoo_data_test_json

# load a json file into mongodb

with open('Data/test_json1.json') as file:
    file_data = json.load(file)
    
# insert_many is used else insert_one is used

    if isinstance(file_data, list):
        collection_main.insert_many(file_data)
    else:
        collection_main.insert_one(file_data)