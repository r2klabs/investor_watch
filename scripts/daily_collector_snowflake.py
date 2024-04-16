import mysql.connector
import requests
import json
from datetime import date
import datetime
import time
import snowflake.connector
from snowflake.connector import DictCursor
import utilities as util

companies = ['META','AAPL','AMZN','NFLX','GOOG','MSFT', 'TSLA']  #company symbols to retrieve.
stock_date = '2024-04-01'

#Establish connection to Snowflake
connection = util.get_snowflake_connection()
    
#Create a cursor object using a dictionary cursor to fetch rows as dictionaries
global_cursor = connection.cursor(DictCursor)


#You need to set up your connection with your credentials
'''
connection = mysql.connector.connect(user='stock_user', password='letmein',
                              host='127.0.0.1',
                              database='stock_data')
global_cursor = connection.cursor()'''

def get_company_data(ticker, timestamp, cnx, local_cursor):
    request_string = 'https://api.polygon.io/v1/open-close/'+ticker+'/'+timestamp+'?adjusted=true&apiKey=46ipIrH5BrzkTqZj7OUvik7XAFOpu8GJ'
    api_response = requests.get(request_string)
    data = api_response.text
    parse_json = json.loads(data)
    db_row=[(v) for k, v in parse_json.items()]
    
    #for item in db_row:
        #print(item)
    
    if(db_row[0] != 'NOT_FOUND'):
    
        symbol = db_row[2]
        ticker_date = db_row[1]
        open_price = db_row[3]
        high_price = db_row[4]
        low_price = db_row[5]
        close_price = db_row[6]
        volume = db_row[7]

        sql = "INSERT INTO stock (symbol, ticker_date, open_price, high_price, low_price, close_price, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (symbol, ticker_date, open_price, high_price, low_price, close_price, volume)
        
        local_cursor.execute(sql, val)
        cnx.commit()

        print(local_cursor.rowcount, "record inserted.")
        time.sleep(15)
        
for company in companies:
    get_company_data(company, stock_date ,connection, global_cursor)
    
global_cursor.close()
connection.close()