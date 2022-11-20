import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine


# print the version of pandas
# print(pd.__version__)
# print (np.__version__)
# print (sqlalchemy.__version__)

# load the json file into a dataframe
df = pd.read_json('yahoo_data.json')

#print(df)

# create a database engine

db_engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="Lorenzo_22",
                               db="yahoo_tickers"))

# write the dataframe to the database

df.to_sql('ticker_selection', db_engine, if_exists='replace')
