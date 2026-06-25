import streamlit as st
import sys
import os

# Append root path to python path to resolve database module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_manager import get_connection
from auth.auth_handler import hash_password, validate_email

def show_register_page():
    st.title("🧬 NextGen DNA Analyzer")
    st.subheader("Create a New Account")
    
    # Secure registration form block
    with st.form("registration_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        # Perfect 8-space indentation inside 'with' block
        submit_btn = st.form_submit_button("Register")
        
    if submit_btn:
        if not full_name or not email or not password or not confirm_password:
            st.error("All fields are required!")
            return
            
        if not validate_email(email):
            st.error("Invalid email format! Please check your input.")
            return
            
        if password != confirm_password:
            st.error("Passwords do not match!")
            return
            
        # Write validated credentials securely into database
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Check for duplicate registration records
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                st.error("Email already registered! Please navigate to Login.")
                conn.close()
                return
                
            # Execute secure password hashing and save user profile
            hashed_pwd = hash_password(password)
            cursor.execute(
                "INSERT INTO users (full_name, email, password) VALUES (?, ?, ?)",
                (full_name, email, hashed_pwd)
            )
            conn.commit()
            conn.close()
            
            st.success("Account created successfully! Kindly redirect to the Login screen.")
            
        except Exception as e:
            st.error(f"Database error during registration execution: {e}")