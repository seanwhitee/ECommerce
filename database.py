import mysql.connector
import pandas as pd
import streamlit as st
import random
  
def add_new_user(conn:mysql.connector.connect, username, password, name, email):
    cur = conn.cursor()
    query = f"""
        INSERT INTO users
        values ('{username}', '{password}', '{email}');
        """
    cur.execute(query)
    conn.commit()
    
def view_cart_items(conn:mysql.connector.connect, username):
    cur = conn.cursor()
    query = f"""
    SELECT * FROM buy where username='{username}';
    """
    cur.execute(query)
    data = cur.fetchall()
    buy_df = pd.DataFrame(data, columns=['buy_id', 'username', 'product_id'])
    return buy_df
  
def delete_item_from_cart(conn:mysql.connector.connect, buy_id):
    cur = conn.cursor()
    query = f"""
    DELETE FROM buy
    WHERE buy_id='{buy_id}';
    """
    cur.execute(query)
    conn.commit()
    
def is_no_duplicate(conn:mysql.connector.connect, username, product_id):
    cur = conn.cursor()
    query = f"""
    SELECT * FROM buy where username='{username}';
    """
    cur.execute(query)
    data = cur.fetchall()
    buy_df = pd.DataFrame(data, columns=['buy_id', 'username', 'product_id'])
    all_product_ids = list(buy_df.get('product_id'))
    if not product_id in all_product_ids:
        return True
    
    return False
    
    
def add_to_cart(conn:mysql.connector.connect, username, product_id):
    if is_no_duplicate(conn, username, product_id):
        cur = conn.cursor()
        query = """
        SELECT * FROM buy;
        """
        cur.execute(query)
        data = cur.fetchall()
        buy_df = pd.DataFrame(data, columns=['buy_id', 'username', 'product_id'])
        all_ids = list(buy_df.get('buy_id'))
        
        num = random.randint(0, 10000)
        while num in all_ids:
            num = random.randint(0, 10000)
        
        query = f"""
        INSERT INTO buy
        values ('{num}', '{username}', '{product_id}');
        """
        
        cur.execute(query)
        conn.commit()

def fetch_all_products(conn:mysql.connector.connect):
    cur = conn.cursor()
    
    query = """
    SELECT * FROM products;
    """
    cur.execute(query)
    data = cur.fetchall()
    product_df = pd.DataFrame(data, columns=['product_id', 'product_name', 'price', 'seller', 'description'])
    return product_df

def get_product(conn:mysql.connector.connect, product_id):
    cur = conn.cursor()
    
    query = f"""
    SELECT * FROM products WHERE product_id='{product_id}';
    """
    cur.execute(query)
    data = cur.fetchall()
    product_df = pd.DataFrame(data, columns=['product_id', 'product_name', 'price', 'seller', 'description'])
    return product_df

# Connect to database and return the database connection object.
def connect():
    
    
    try:
        # Connect to server
        # MySQL database configuration setup in .streamlit/secrets.toml file.
        connect_db = mysql.connector.connect(**st.secrets["mysql"])
        print("Connect success!")
        
    except Exception as ex:
        print(ex)
        
        
    
    return connect_db
    
# test session
if __name__ == '__main__':
    pass
    
    
    