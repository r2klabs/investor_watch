
import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor
import json

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
     # Always close cursor and connection
        cursor.close()
        conn.close()
        
def get_data(query, cursor):
    
    try:
        # Execute SQL query
        cursor.execute(query)
        data = cursor.fetchall()  # Fetch all data
    finally:
        pass
    
    return data

# Main function to run the Streamlit app
def main():
    # Establish connection to Snowflake
    conn = get_connection()
    
     # Create a cursor object using a dictionary cursor to fetch rows as dictionaries
    cur = conn.cursor(DictCursor)
    
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

    # Set the title of the app
    st.title('Invester Watch')

    # Display the data as a table in Streamlit
    st.write("Here are the average, minimum, and maximum close prices for each stock in your portfolio:")
    st.table(data)
    
    close_connection(cur, conn)

# Run the main function when the script is executed
if __name__ == '__main__':
    main()
