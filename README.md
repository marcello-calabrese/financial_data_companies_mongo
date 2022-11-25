# Financial Companies Data Dashboard with Python and MongoDB Charts

**As a stocks investor I am always looking for new ways to improve my trading strategies. One of the most important things is to have a good understanding of the financials of the companies I am investing.**

_So how to get key financial metrics of my shares and visualize them in a dashboard?_

## Introduction

One of the greatest things about Python is that it has a lot of libraries that can help you to get the data you need. Luckily for us, there is a library called [yfinance](https://pypi.org/project/yfinance/) that can help us to get the financials of the companies we are trading.\n

Through simple code syntaxt we can get info such as latest share price, market cap, beta, 52-week range, earnings date, dividend yield, P/E ratio, etc. As a practical and lazy person instead of getting the financials of the companies I am trading one by one, I decided to get the financials of all the companies I am trading and store them in a database in the cloud and MongoDB is the perfect choice for this project because it is free and easy to use (free tier is 512 MB). I tried to connect the MongoDB database to Microsfot PowerBI, but because of the free tier of MongoDB I was not able to connect it to PowerBI. So I decided to use MongoDB Charts to visualize the data. MongoDB Charts is also free!!

**Final Result of the Dashboard**
![image](https://user-images.githubusercontent.com/74682725/203966403-242c95d2-4d37-48c1-8be4-8d22f310c446.png)


## Getting the financials of the companies I am trading

Currently the shares I have in my portfolio are the following:

- Microsoft
- McDonalds
- IBM
- Johnson & Johnson
- Zion Bank

The financial data of these companies I decided to store in the database are:

- Symbol or ticker
- Company name
- Company description
- PE ratio (price to earnings ratio), if you don't know what is the PE ratio, you can read more about it [here](https://www.investopedia.com/terms/p/pe.asp)
- Dividend yield
- Cash Flow

Now let's run into the code and see how to get the financials of the companies I am trading and store them in a MongoDB database.


## Create a MongoDB account

First of all, you need to create a MongoDB account. You can create a free account [here](https://www.mongodb.com/cloud/atlas). After you create your account you need to create a cluster. You can find a tutorial on how to create a cluster [here](https://docs.atlas.mongodb.com/tutorial/create-new-cluster/). After you create your cluster you need to create a database and a collection. You can find a tutorial on how to create a database and a collection [here](https://docs.atlas.mongodb.com/tutorial/create-new-database/). After you create your database and collection you need to create a user and get the connection string. You can find a tutorial on how to create a user and get the connection string [here](https://docs.atlas.mongodb.com/tutorial/create-new-user/). After you create your user and get the connection string you need to whitelist your IP address. You can find a tutorial on how to whitelist your IP address [here](https://docs.atlas.mongodb.com/tutorial/whitelist-connection-ip-address/). 

## Importing the libraries

To replicate my project easily I provided a requirements.txt file in my GitHub repository. You can install all the libraries with the following command:

    ```python
    pip install -r requirements.txt
    ```

In your newly created environment create a new folder and create a new file ''.py''. I called (as you can see in my repo) run_mongo.py. In this file you need to import the following libraries:

```python
# import main libraries

import pandas as pd # data manipulation
import numpy as np # data manipulation
import yfinance as yf # get financials of the companies
import pymongo # connect to MongoDB
from pymongo import MongoClient # connect to MongoDB
import json # convert data to json
```

## ETL Pipeline: Extract, Transform, Load

Now we are going to create the ETL pipeline to Extract the data from yahoo finance, transform the data and load the data into MongoDB.

### Extract Company Financials Data from Yahoo Finance

The extract funtion named ''extract_ticker()'' gets the ticker of the companies I have in my portfolio, create a dictionary to store the data mentioned above of each company and store them in a pandas dataframe. The function returns the pandas dataframe.

```python
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
```
### Transform the data

The transform function named ''transform_data()'' applies a small data cleaning to round the values to 2 decimal places and convert the data into json format needed later to load the data into MongoDB.

```python
def transform_data():
    # create a dataframe to store the data
    df_transformed = extract_ticker() # call the extract function
    # round the values of the dataset to 2 decimal places
    df_transformed = df_transformed.round(2)
    
    # convert the dataframe into a json file
    json_file = df_transformed.to_json('Data/yahoo_data.json' ,indent=4, orient='records')
    return json_file
```

### Load the data into MongoDB

The load function named ''load_mongo()'' loads the data into MongoDB. The function takes the connection string, the database name, the collection name and the json file as arguments. The function returns the data loaded into MongoDB.

```python
def load_mongo():
    # load the json file into mongodb
    # create a client object
    client = MongoClient('mongodb+srv://USER:PASSWORD@cluster0.ragcpnf.mongodb.net/?retryWrites=true&w=majority') # insert your connection string and your personal user and password of your MongoDB account
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
```

## Run the ETL Pipeline

The last section of the code is to run the ETL pipeline. The code below calls the functions and prints the result. I used the standard ''def main()'' function as the main part ingesting the 3 ETL functions and the ''if __name__ == '__main__':'' to run the code.

```python
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
```

## The MongoDB Database with the Data of the Companies in my Portfolio stored in a Collection

After we executed the code we can see the data in our MongoDB database. I created a database named ''stockdb'' and a collection named ''stock_data''. The data is stored in the collection. Just as a reminder, in MongoDB collections are similar to tables in relational databases and documents are similar to rows in relational databases.
See below th screenshot of the data in MongoDB.

![image](https://user-images.githubusercontent.com/74682725/203966598-aa4021b4-8b63-44d5-a8e4-de26a6fb6fbe.png)

You can see how the script captured the key metrics of the companies in my portfolio. For who never used MongoDB before, the data appears similar to a list of dictionaries, something completely different from the way we see data in relational databases.

Great! We have the data in MongoDB. And now let's make this data visually meaningful. Now we start the second fun part of the project, the data visualization inside MongoDB with MongoDB Charts 😎!

## MongoDB Charts

Right here we go to the second fun part of the project, now I will show you how easy is to create a dashboard with MongoDB chart with just few clicks and the drag and drop tool to plot the data in the axis. We are going to create a dashboard with the key metrics of the companies in my portfolio. The dashboard will be updated automatically every time the ETL pipeline is executed. Just as a reminder, based on the data we stored in our MongoDB database, the dashboard will show 6 charts with the key metrics and information of the companies in my portfolio.

### Create a Dashboard 

To create a dashboard in MongoDB Charts, we need to create a new dashboard. To do that, we need to click on the ''Create Dashboard'' button. See below the short video demo.

[Watch the video](https://www.youtube.com/embed/Mja2apf0N64)


After we enter browse collections in our cluster, we select our stockdb database and the stock_data collection. After we select Charts on the top menu, we click ''Add Dashboard'' and add a Title to the dashboard. We click Add Chart, select our cluster (in my case is Cluster0), select the database (stockdb)and the collection (stock_data). We are in the main panel now where on the left the data source is sampled and appears as a drag and drop tool to start building the charts. The dashboard will be structured  with 2 rows and 3 charts per row. The visualization consists of 2 tables with company name and description and company name and ticker symbol, the rest of the charts are simple bar chart to show the key metrics of the companies in my portfolio. See below the second part of the video demo to draw the charts.

[Watch the video](https://www.youtube.com/embed/g96FcqN6EJc)

## Export the Dashboard

After we created the dashboard, we can use the iframe tool to export and embed the dashboard on our webpage. See the video demo below.

[Watch the video](https://www.youtube.com/embed/tqJ8JJevki8)

## Basic html page to embed the dashboard

The last step is to create a basic html page to embed the dashboard. You can find the code in the [github repository](https://github.com/marcello-calabrese/financial_data_companies_mongo/tree/main/html_dashboard) and below. I used [Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/) CSS framework to create a simple page.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
    <title>Portfolio' Shares Financial Data Dashboard</title>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <div class="col-md-12">
                <h1>Portfolio's Shares Financial Data Dashboard</h1>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <h2>Embedded MongoDB Dashboard directly from MongoDB Charts just with the iframe tags</h2>
            </div>
        </div>
        <div class="row">
            
                <!-- Add the iframe code generated from MongoDB Charts-->
                <iframe style="background: #F1F5F4;border: none;border-radius: 2px;box-shadow: 0 2px 10px 0 rgba(70, 76, 79, .2); height: 700px;"  src="https://charts.mongodb.com/charts-project-0-mohor/embed/dashboards?id=6379f795-14ab-4c8d-8ceb-051750764578&theme=light&autoRefresh=true&maxDataAge=3600&showTitleAndDesc=false&scalingWidth=fixed&scalingHeight=fixed"></iframe>
        </div>
    </div>
</body>
</html>
```
The page short video demo is below. As you can see is very interactive. Don't forget to change the iframe code with the code generated from MongoDB Charts, I had to manually add the height pixels in the iframe to 700px to make sure the dahsboard is expanded in the full html page:

[Watch the video](https://www.youtube.com/embed/eKe5Dc2AB2k)

## Conclusion

In this post, I showed you how easy is to create a dashboard with MongoDB Charts. I used the ETL pipeline to extract the data from the web, transform the data and load it into MongoDB. Then I created a dashboard with MongoDB Charts and exported the dashboard with the iframe tool to embed it in a basic html page. I hope you enjoyed this post and learned something new. If you have any questions, please let me know in the comments below. Thanks for reading!
