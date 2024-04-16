
'''This script connects to Snowflake, fetches data from the STOCK table, and displays the data in a Streamlit app.'''

import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor
import json
import pandas as pd
import utilities as util

def get_pandas_data(query, conn):
    df = pd.read_sql(query, conn)
    return df
      
def get_data(query, cursor):
    """Execute the SQL query and fetch the data from Snowflake"""  #was cursor
    try:
        #data=pd.read_sql(query, conn)
        # Execute SQL query
        cursor.execute(query)
        data = cursor.fetchall()  # Fetch all data
    finally:
        pass # Do nothing if an exception occurs
    
    return data


def main():
    """Main function to run the Streamlit app"""
    #Establish connection to Snowflake
    conn = util.get_snowflake_connection()
    
    #Create a cursor object using a dictionary cursor to fetch rows as dictionaries
    cur = conn.cursor(DictCursor)
    connected = True
    
     # Set the title of the app
    st.title('Invester Watch')
    
    with st.sidebar:
        st.subheader("Snowflake Connection")
        if st.button("Connect to Snowflake", type="primary"):
            conn = util.get_snowflake_connection()
            cur = conn.cursor(DictCursor)
            connected = True
        if st.button("Disconnect from Snowflake", type="secondary"):
            util.close_snowflake_connection(cur, conn)
            connected = False
    
    summary_tab, query_tab, graph_tab = st.tabs(["Summary", "Query", "Graph"])
    
    with summary_tab:
        if connected:
            # Display the data as a table in Streamlit
            st.write("Here are the average, minimum, and maximum close prices for each stock in your portfolio:")
        
            #Establish the SQL query to fetch the average, minimum, and maximum close prices for each stock
            query = """SELECT
                        SYMBOL,
                        AVG(CLOSE_PRICE) AS "Average Close Price", 
                        MIN(CLOSE_PRICE) AS "Minimum Close Price",
                        MAX(CLOSE_PRICE) AS "Maximum Close Price" 
                    FROM
                        STOCK
                    GROUP BY SYMBOL
                    ORDER BY SYMBOL;
                    """
            # Fetch data from Snowflake
            data = get_data(query,cur)
            st.table(data)
            
    
    with query_tab:
        if connected:
            st.write("You can write your own SQL query to fetch data from the STOCK table.")
            query = st.text_area("Enter your SQL query here:", "SELECT * FROM STOCK LIMIT 10;")
            if st.button("Run Query"):
                with st.spinner('Fetching data...'):
                    data = get_data(query, cur)
                    st.table(data)
            
    with graph_tab:
        if connected:
            st.write("You can visualize the data from the STOCK table.")
            option = st.selectbox('Select a stock:', ['AMZN', 'APPL', 'GOOG', 'META','MSFT','NFLX','TSLA'])
            query = f"SELECT TICKER_DATE, CLOSE_PRICE FROM STOCK WHERE SYMBOL = '{option}'"
            data = get_pandas_data(query, conn)
            #st.write(data.head())
            st.line_chart(data.set_index('TICKER_DATE'))

    st.write(f'Connected to Snowflake: {connected}')
    
# Run the main function when the script is executed
if __name__ == '__main__':
    main()
