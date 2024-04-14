import mysql.connector
import pandas as pd
import requests
import json
from datetime import date
import datetime
import time

def get_company_data(ticker, start_day, end_day):
    '''Uses the Polygon API to get stock data for a given ticker symbol and date range.'''
    request_string='https://api.polygon.io/v2/aggs/ticker/'+ticker+'/range/1/day/'+start_day+'/'+end_day+'?adjusted=true&sort=asc&apiKey=46ipIrH5BrzkTqZj7OUvik7XAFOpu8GJ'

    api_response = requests.get(request_string)
    data = api_response.text
    time.sleep(15) #Slows down the requests to avoid being blocked by the API.
    return json.loads(data)
    
def insert_data(ticker, row, local_cursor, cnx):
    '''Inserts stock data into a MySQL database.'''
    symbol = ticker
    local_date = str(row['t'])[0:-3]
    ticker_date = datetime.datetime.fromtimestamp(int(local_date)).date()
    open_price = row['o']
    high_price = row['h']
    low_price = row['l']
    close_price = row['c']
    volume = row['v']

    #print(symbol, ticker_date, open_price, high_price, low_price, close_price, volume)
                     
    sql = "INSERT INTO stock (symbol, ticker_date, open_price, high_price, low_price, close_price, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (symbol, ticker_date, open_price, high_price, low_price, close_price, volume)
    local_cursor.execute(sql, val)
    cnx.commit()


def connect_mysql():
    '''Connects to a MySQL database.'''
    connection = mysql.connector.connect(user='stock_user', password='letmein',
                                host='127.0.0.1',
                                database='stock_data')
    return connection