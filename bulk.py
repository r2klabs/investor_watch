import rrk_finance as rrk
import pandas as pd
from datetime import date
import datetime
import time
import json

ticker='TSLA'
start_day='2023-02-11'
end_day='2024-03-31'
 
cnx = rrk.connect_mysql()
global_cursor = cnx.cursor()

data = rrk.get_company_data(ticker, start_day, end_day)['results']
#print(json.dumps(data, indent=2))

for i in range(0, len(data)):
    rrk.insert_data(ticker, data[i], global_cursor, cnx)
    

print("Insert complete")