'''This script is used to collect data for a specific company from the Polygon API
and insert it into MySQL database.  This was part of the first iteration of this project
using local database storage.  This script is no longer used, but is kept for reference and testing.'''


import utilities as util
import pandas as pd
from datetime import date
import datetime
import time
import json

ticker='NVO'
start_day='2023-02-11'
end_day='2024-03-31'
 
cnx = util.connect_mysql()
global_cursor = cnx.cursor()

data = util.get_company_data(ticker, start_day, end_day)['results']
#print(json.dumps(data, indent=2))

for i in range(0, len(data)):
    util.insert_data(ticker, data[i], global_cursor, cnx)
    
print("Insert complete")