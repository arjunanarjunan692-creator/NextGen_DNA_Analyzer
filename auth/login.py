import streamlit as st
import sys
import os

# Path configuration for database module import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_manager import get_connection
from auth.auth_handler import verify_password

def show_login_page():
    st.title("🧬 NextGen DNA Analyzer")
    st.subheader("Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Login")
        
    if submit_btn:
        if not email or not password:
            st.error("Please enter both email and password.")
            return
            
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Fetch user account by email
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Verify the hashed password
                if verify_password(password, user['password']):
                    # Initialize Streamlit session states upon successful login
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user['id']
                    st.session_state['user_name'] = user['full_name']
                    st.session_state['user_email'] = user['email']
                    
                    st.success(f"Welcome back, {user['full_name']}!")
                    st.rerun()  # Refresh page to redirect to dashboard
                else:
                    st.error("Incorrect password! Please try again.")
            else:
                st.error("Account not found with this email. Please register first.")
                
        except Exception as e:
            st.error(f"Database error during login: {e}")