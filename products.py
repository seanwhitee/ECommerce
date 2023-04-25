from pathlib import Path

import streamlit as st  # pip install streamlit
from PIL import Image  # pip install pillow

from database import get_product

def product_page(conn):
    
    # --- PATH SETTINGS ---
    THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    ASSETS_DIR = THIS_DIR / "assets"
    
    product_list = {
        "1": ["Excel Add-In: MyToolBelt", "https://buy.stripe.com/test_14kaF75nPg2xe52288"]
    }
    
    # First product 
    with st.container():
        product_df = get_product(conn, 1)
        st.header(f"{product_df.get('product_name')[0]}")
        left_col, right_col = st.columns(2)
        with left_col:
            st.text("")
            description = product_df.get('description')[0].splitlines(True)
        
            for sentence in description:
                st.markdown(sentence)
            st.markdown(
                f"""<a href={product_list[product_df.get('product_id')[0]][1]} class="button">👉 Buy</a>""",
                unsafe_allow_html=True,
            )
        with right_col:
            product_image = Image.open(ASSETS_DIR / "product.png")
            st.image(product_image, width=450)