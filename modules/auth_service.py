import hashlib
import streamlit as st
import re
from modules import auth_db

# Initialize DB on first load
auth_db.init_db()

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_hash, password):
    """Verify a password against its hash."""
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    """Check if email format is valid using regex."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def login(email, password):
    """Attempt to log in a user."""
    user = auth_db.get_user_by_email(email)
    
    if user and verify_password(user['password_hash'], password):
        st.session_state['logged_in'] = True
        st.session_state['user_info'] = {
            "name": user['name'],
            "email": user['email'],
            "role": user['role']
        }
        return True
    return False

def register(email, password, name):
    """Register a new user."""
    if not email or not password or not name:
        return False, "Semua field harus diisi."
    
    if not is_valid_email(email):
        return False, "Format email tidak valid."

    if len(password) < 6:
        return False, "Password minimal 6 karakter."
        
    pwd_hash = hash_password(password)
    success = auth_db.create_user(email, pwd_hash, name)
    
    if success:
        return True, "Registrasi berhasil! Silakan login."
    else:
        return False, "Email sudah terdaftar."

def logout():
    """Log out the current user."""
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = {}
