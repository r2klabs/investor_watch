import mysql.connector
import requests
import json
import datetime
import time
import snowflake.connector
from snowflake.connector import DictCursor
import utilities as util

companies = ['AAPL','AMZN','GOOG','META','MSFT','NFLX', 'TSLA']  #company symbols to retrieve.
stock_date = '2024-04-03'

#Establish connection to Snowflake
connection = util.get_snowflake_connection()
    
#Create a cursor object using a dictionary cursor to fetch rows as dictionaries
global_cursor = connection.cursor(DictCursor)

for company in companies:
    util.get_polygon_data(company, stock_date ,connection, global_cursor)
    
global_cursor.close()
connection.close()