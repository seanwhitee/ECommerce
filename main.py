from pathlib import Path
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from database import *
from streamlit_option_menu import option_menu
from products import *


def load_css_file(css_file_path):
        with open(css_file_path) as f:
            return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
def main():
    ### --- PAGE CONFIG ---
    st.set_page_config(
        page_title='abc',
        page_icon=":star:",
        layout="centered",
        
    )
    
    ### Connect to database
    conn = connect() 
    
    # --- User login ---
    with open('./config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    
    name: str
    authentication_status: bool
    username: str
    placeholder = st.empty()
    with placeholder:
        with st.container():
            
            ## Login session
            with st.expander('Login'):
                name, authentication_status, username = authenticator.login('Login', 'main')
                
            ## Registration session
            with st.expander('Registration'):
                try:
                    if authenticator.register_user('Register user', preauthorization=False):
                        st.success('User registered successfully')
                        
                        # Update config.yaml file
                        with open('./config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                            
                except Exception as e:
                    st.error(e)

            ## Forgot password
            with st.expander('Forgot password'):
                try:
                    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
                    if username_forgot_pw:
                        
                        # Random password to be transferred to user securely
                        st.success('New password sent securely')
                        
                        # print the new password on my terminal, or you can use alternative way to send to you
                        # Maybe implement some feature like sending password to user email or sth.
                        print(random_password)
                        
                        # Update config.yaml file
                        with open('./config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                    else:
                        st.error('Username not found')
                        
                except Exception as e:
                    st.error(e)
                
            ## Forgot username
            with st.expander('Forgot username'):
                try:
                    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
                    if username_forgot_username:
                        st.success('Username sent securely')
                        # Username to be transferred to user securely
                        
                        print(username_forgot_username)
                        print(email_forgot_username)
                        
                    else:
                        st.error('Email not found')
                except Exception as e:
                    st.error(e)
                    
    # --- End of login process ---

    # Login successfully
    if authentication_status:
            
        # If login successfully, user should not see forgot password. register...
        with placeholder:
            st.text("") 
            
        st.sidebar.title(f'Welcome *{name}*')
        
        with st.sidebar:
            
            bar = option_menu(
                menu_title= 'Function Table',
                menu_icon='gear',
                options=['Your Cart', 'Add To Cart'],
                
            )
            
            ### Perform the shopping cart function
            if bar == 'Your Cart':
                
                menu = ['View Cart Products', 'Delete Item']
                choice = st.sidebar.selectbox("Menu", menu)
                
                if choice == 'Delete Item':
                    
                    your_cart_df = view_cart_items(conn, username)
                    all_buy_ids = list(your_cart_df.get('buy_id'))
                    all_cart_products_ids = list(your_cart_df.get('product_id'))
                    
                    with st.form('Delete something... ?'):
                        buy_id = st.text_input('buy_id', placeholder='Buy Id...')
                        deleted_product_id = st.text_input('product_id', placeholder='Product id...')
                        
                        if st.form_submit_button('Delete'):
                    
                            if buy_id in all_buy_ids and deleted_product_id in all_cart_products_ids and all_cart_products_ids[all_buy_ids.index(buy_id)] == deleted_product_id:
                                if st.success(f'Successfully delete product_id {deleted_product_id}'):
                                        
                                        delete_item_from_cart(conn, buy_id)
                            else:
                                st.error(f'The buy_id or product_id may be wrong value.') 
                    
                elif choice == 'View Cart Products':
                    
                    # View product detail
                    your_cart_df = view_cart_items(conn, username)
                    st.dataframe(your_cart_df)
                    
                    # prepare for checkout
                    item_ids = list(your_cart_df.get('product_id'))
                    
                    product_links = get_product_link()
                    
                    with st.expander('Want to checkout ?', ):
                        st.text("")
                        for item_id in item_ids:
                            
                            # show product name and id
                            st.markdown(f'<strong>{item_id}</strong>. <strong>{product_links[item_id][0]}</strong>', unsafe_allow_html=True)
                        
                            # show strip checkout
                            st.markdown(
                                f'<a href={product_links[item_id][1]} class="button">👉 Buy</a>',
                                unsafe_allow_html=True,
                            )
                    
                
            ### Perform the add to cart function function
            elif bar == 'Add To Cart':
                with st.form('Buy something... ?', clear_on_submit=True):
                    product_id = st.text_input('product_id', placeholder='Product Id...')
                    product_name = st.text_input('product_name', placeholder='Product Name...')
                    product_links = get_product_link()
                    if st.form_submit_button('Add it'):
                        
                        if is_no_duplicate(conn, username, product_id) and is_product_exist(conn, product_id, product_name) and product_links[product_id][0] == product_name:
                            if st.success(f'Successfully add product {product_name}'):
                                # if no duplicate product, then add to cart
                                add_to_cart(conn, username, product_id)
                        else:
                            if not is_no_duplicate(conn, username, product_id):
                                st.error(f'The {product_name} already in your cart.')
                            elif not is_product_exist(conn, product_id, product_name):
                                st.error(f'The product_id or product_name may be wrong value.')
                            else:
                                st.error('name and id not match.')
                        
                            
                            
                        
                        
            
            # line break before logout button ...    
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            
            
            
            
            ## Add line before logout button ...
            st.markdown("""<hr class="between-footer-and-content">""", unsafe_allow_html=True)
        
        # logout button
        authenticator.logout('Logout', 'sidebar')
        
        with st.sidebar:
            
            ## Reset password
            with st.expander('Reset password'):
                try:
                    if authenticator.reset_password(username, 'Reset password'):
                        st.success('Password modified successfully')
                        
                        # Update config.yaml file
                        with open('./config.yaml', 'w') as file:
                            yaml.dump(config, file, default_flow_style=False)
                except Exception as e:
                    st.error(e)
                    
            ## Reset user detail
            with st.expander('Reset user detail'):
                try:
                    if authenticator.update_user_details(username, 'Update user details'):
                        st.success('Entries updated successfully')
                        
                    # Update config.yaml file
                    with open('./config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                        
                except Exception as e:
                    st.error(e)
                    
        
            
            
        # --- PATH SETTINGS ---
        THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        STYLES_DIR = THIS_DIR / "styles"
        CSS_FILE = STYLES_DIR / "main.css"
        
        load_css_file(CSS_FILE)
        
        # Enter product page
        product_page(conn, username)
        
    elif authentication_status is False:
        st.error('Username/password is incorrect')
        
    elif authentication_status is None:
        st.warning('Please enter your username and password')
        
        
if __name__ == '__main__':
    main()