import mysql.connector
import pandas as pd
import streamlit as st

# def get_credential_info(conn: mysql.connector):
#     cur = conn.cursor()
#     query = f"""
#     SELECT * FROM users;
#     """
     
#     cur.execute(query)
#     data = cur.fetchall()
#     users_credential_df = pd.DataFrame(data, columns=['username', 'password', 'name', 'email'])
#     return users_credential_df
    
def get_product(conn:mysql.connector, product_id):
    cur = conn.cursor()
    
    query = f"""
    SELECT * FROM products WHERE product_id='{product_id}';
    """
    cur.execute(query)
    data = cur.fetchall()
    product_df = pd.DataFrame(data, columns=['product_id', 'product_name', 'price', 'seller', 'description'])
    return product_df

# Connect to database and return the database connection object.
@st.cache_resource
def connect():
    
    
    try:
        # Connect to server
        # MySQL database configuration setup in .streamlit/secrets.toml file.
        connect_db = mysql.connector.connect(**st.secrets["mysql"])
        print("Connect success!")
        
    except Exception as ex:
        print(ex)
        
        
    
    return connect_db
    
    
    
    