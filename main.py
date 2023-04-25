from pathlib import Path
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from database import (
    connect
)
from products import product_page


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
    
    ### User login
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
                        st.success('New password sent securely')
                        # Random password to be transferred to user securely
                        
                        # print the new password on my terminal, or you can use alternative way to send to you
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
       
    # Login successfully
    if authentication_status:
        
        # If login successfully, user should not see forgot password. register...
        with placeholder:
            st.text("") 
            
        st.sidebar.title(f'Welcome *{name}*')
        
        
        with st.sidebar:
            
            # line break before logout button ...    
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            st.markdown("""<br>""", unsafe_allow_html=True)
            
            
            # Add line before logout button ...
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
        product_page(conn)
        
    elif authentication_status is False:
        st.error('Username/password is incorrect')
        
    elif authentication_status is None:
        st.warning('Please enter your username and password')
        
        
if __name__ == '__main__':
    main()