from pathlib import Path

import streamlit as st  # pip install streamlit
from PIL import Image  # pip install pillow

from database import *
    
def get_product_link():
    product_links = {
        "1": ["Excel Add-In: MyToolBelt", "https://buy.stripe.com/test_14kaF75nPg2xe52288"],
        "2": ["Hello World", "https://buy.stripe.com/test_5kA00t6rT8A56CA7st"],
        "3": ["System Design", "https://buy.stripe.com/test_28o14xg2t7w1f964gi"]
    }
    return product_links

def is_product_exist(conn:mysql.connector.connect, product_id, product_name):
    
    products_df = fetch_all_products(conn)
    
    all_products_ids = list(products_df.get('product_id'))
    all_products_names = list(products_df.get('product_name'))
    
    if ( product_id in all_products_ids ) and ( product_name in all_products_names ):
        return True
    
    return False

def product_page(conn, username):
    
    # --- PATH SETTINGS ---
    THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    ASSETS_DIR = THIS_DIR / "assets"
    
    # Fetch all products
    products_df = fetch_all_products(conn)
    
    product_ids = products_df.get('product_id')
    product_names = products_df.get('product_name')
    product_prices = products_df.get('price')
    product_sellers = products_df.get('seller')
    product_descriptions = products_df.get('description')
    
    ### List all products
    for i in range(0, len(product_ids)):
        
    
        with st.container():
                
            left_col, right_col = st.columns(2)
            with left_col:
                st.header(f"{product_ids[i]}. {product_names[i]}")
                st.text("")
                description = product_descriptions[i].splitlines(True)
            
                for sentence in description:
                    st.markdown(sentence)
                
            with right_col:
                product_image = Image.open(ASSETS_DIR / f"test_product{i+1}.jpg")
                st.image(product_image, use_column_width=True)
                
            if not i == len(product_ids) - 1:
                # # Add line before logout button ...
                st.markdown("""<hr class="between-footer-and-content">""", unsafe_allow_html=True)
                
if __name__ == '__main__':
    conn = connect()
    product_page(conn, 'test')