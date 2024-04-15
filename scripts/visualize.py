
import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor
import json
import pandas as pd


def get_connection(config_path='snowflake_config.json'):
    """Load configuration from the JSON file and establish connection 
    to Snowflake using the loaded configuration"""
    
    with open(config_path, 'r') as file:
        config = json.load(file)

    conn = snowflake.connector.connect(
        user=config['user'],
        password=config['password'],
        account=config['account'],
        warehouse=config['warehouse'],
        database=config['database'],
        schema=config['schema']
    )
    
    return conn

def close_connection(cursor, conn):
    """CLoses both the shared cursor and connection to Snowflake"""
    cursor.close()
    conn.close()

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
    conn = get_connection()
    
    #Create a cursor object using a dictionary cursor to fetch rows as dictionaries
    cur = conn.cursor(DictCursor)
    
     # Set the title of the app
    st.title('Invester Watch')
    
    summary_tab, query_tab, graph_tab = st.tabs(["Summary", "Query", "Graph"])
    
    with summary_tab:
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
        st.write("You can write your own SQL query to fetch data from the STOCK table.")
        query = st.text_area("Enter your SQL query here:")
        if st.button("Run Query"):
            data = get_data(query, cur)
            st.write(data)
            
    with graph_tab:
        st.write("You can visualize the data from the STOCK table.")
        query = """SELECT
                    TICKER_DATE, CLOSE_PRICE
                FROM
                    STOCK
                WHERE SYMBOL = 'APPL'
                """
        data = get_pandas_data(query, conn)
        st.write(data.head())
        st.line_chart(data.set_index('TICKER_DATE'))

    
    close_connection(cur, conn)

# Run the main function when the script is executed
if __name__ == '__main__':
    main()
