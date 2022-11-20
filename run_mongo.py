# Script to run the ETL process

''' 
The script is used for extracting, transforming, and loading data into a json file of selected tickers and load into a 
mongodb database.

'''

# import main libraries

import pandas as pd
import numpy as np
import yfinance as yf
import pymongo
from pymongo import MongoClient
import json

### Application Layer ###

############################# extraction function ##############################################################

def extract_ticker():
    # extract the ticker data
    
    msft = yf.Ticker('MSFT')
    zion = yf.Ticker('ZION')
    ibm = yf.Ticker('IBM')
    jnj = yf.Ticker('JNJ')
    mcd = yf.Ticker('MCD')
    # create a dictionary to store the data
    dct2 = {'Company_name': [msft.info['longName'], zion.info['longName'], ibm.info['longName'], jnj.info['longName'], mcd.info['longName']],
                    'Company_ticker': [msft.info['symbol'], zion.info['symbol'], ibm.info['symbol'], jnj.info['symbol'], mcd.info['symbol']],
                    'Closed_price': [msft.info['previousClose'], zion.info['previousClose'], ibm.info['previousClose'], jnj.info['previousClose'], mcd.info['previousClose']],
                    'Company_info': [msft.info['longBusinessSummary'], zion.info['longBusinessSummary'], ibm.info['longBusinessSummary'], jnj.info['longBusinessSummary'], mcd.info['longBusinessSummary']],
                    'Company_PE': [msft.info['trailingPE'], zion.info['trailingPE'], ibm.info['trailingPE'], jnj.info['trailingPE'], mcd.info['trailingPE']],
                    'Company_cash_flow': [msft.info['operatingCashflow'], zion.info['operatingCashflow'], ibm.info['operatingCashflow'], jnj.info['operatingCashflow'], mcd.info['freeCashflow']],
                    'Company_dividend': [msft.info['dividendRate'], zion.info['dividendRate'], ibm.info['dividendRate'], jnj.info['dividendRate'], mcd.info['dividendRate']]}
        
    # create a dataframe to store the data
    df = pd.DataFrame(dct2)
    # return the dataframe
    return df

############################# transformation function #######################################################################

def transform_data():
    # create a dataframe to store the data
    df_transformed = extract_ticker()
    # round the values of the dataset to 2 decimal places
    df_transformed = df_transformed.round(2)
    
    # convert the dataframe into a json file
    json_file = df_transformed.to_json('Data/yahoo_data.json' ,indent=4, orient='records')
    return json_file

############################# loading function #######################################################################

def load_mongo():
    # load the json file into mongodb
    # create a client object
    client = MongoClient('mongodb+srv://USER:PASSWORD@cluster0.ragcpnf.mongodb.net/?retryWrites=true&w=majority')
    # get a database named "stockdb"
    db1 = client.stockdb
    # get a collection named "yahoo_data_test_json"
    collection_main = db1.stock_data
    # load a json file into mongodb
    with open('Data/yahoo_data.json') as file:
        file_data = json.load(file)
    # insert_many is used else insert_one is used
    if isinstance(file_data, list):
        # empty the collection
        collection_main.delete_many({})
        # insert the data into the collection
        collection_main.insert_many(file_data)
    else:
        collection_main.insert_one(file_data)
    return True


############################# main function #######################################################################

def main():
    # call the extract function
    #extract_ticker()
    # call the transform function
    transform_data()
    # call the load function
    load_mongo()
    return True

### Run Layer ###

if __name__ == '__main__':
    main()
    print('Data has been extracted, transformed, saved in a json file and loaded into mongodb')
    
    
    
