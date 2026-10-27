# frontend/pages/0_Login.py - User Authentication
import streamlit as st
import sys
import os

# Add parent directory to path to import database module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.auth import auth_manager
import time

# Page config
st.set_page_config(
    page_title="Login - Student Feedback Analyzer",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from theme import apply_theme
apply_theme()

# Custom styling
st.markdown("""
    <style>
    .login-container {
        max-width: 420px;
        margin: 60px auto;
        padding: 40px;
        background: rgba(255,255,255,0.9);
        border-radius: 18px;
        border: 1px solid #e4dcff;
        box-shadow: 0 18px 42px rgba(124,58,237,.14);
    }
    .demo-credentials {
        background: #ede9fe;
        border-left: 4px solid #7c3aed;
        padding: 12px 14px;
        border-radius: 10px;
        margin-top: 20px;
        font-size: 13px;
        color: #3f3d56;
    }
    </style>
""", unsafe_allow_html=True)

# Check if already logged in
if "user_id" in st.session_state and st.session_state.user_id:
    st.switch_page("pages/1_Upload_Feedback.py")

st.markdown("<h1 style='text-align: center; margin-bottom: 40px;'>🔐 Login</h1>", unsafe_allow_html=True)

# Login form
with st.form("login_form"):
    username = st.text_input("Username", placeholder="admin or viewer")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    
    submit_btn = st.form_submit_button("🔓 Login", use_container_width=True)

if submit_btn:
    if not username or not password:
        st.error("❌ Please enter both username and password")
    else:
        user = auth_manager.verify_user(username, password)
        
        if user:
            # Store in session
            st.session_state.user_id = user["user_id"]
            st.session_state.username = user["username"]
            st.session_state.role = user["role"]
            
            st.success(f"✅ Welcome, {user['username']}! (Role: {user['role']})")
            time.sleep(1)
            st.switch_page("pages/1_Upload_Feedback.py")
        else:
            st.error("❌ Invalid credentials. Try again.")

# Demo credentials info
st.markdown("""
    <div class="demo-credentials">
    <strong>📌 Demo Credentials</strong><br>
    👤 <code>admin</code> / <code>admin123</code> → Full access<br>
    👁️ <code>viewer</code> / <code>viewer123</code> → Read-only<br>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("🛡️ Multi-Agent Student Feedback Intelligence Platform | v1.0")
