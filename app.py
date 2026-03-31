"""
WelloraFit AI - AI-Powered Health & Fitness Tracker
"""
import streamlit as st
import sys
import os
from datetime import datetime

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

from auth.authentication import create_user, authenticate_user, get_user_by_id
from config.settings import settings
from config.database import init_database

# Initialize database
try:
    init_database()
except Exception as e:
    # Don't show encoding errors to user, just log them
    if "codec can't encode" not in str(e):
        st.error(f"Database initialization error: {e}")

# Page configuration
st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00D9A3;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #00D9A3;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00B589;
    }
</style>
""", unsafe_allow_html=True)

def login_page():
    """Display login/signup page"""
    st.markdown('<div class="main-header">🏋️ WelloraFit AI</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.subheader("Welcome Back!")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if username and password:
                    user = authenticate_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
    
    with tab2:
        st.subheader("Create Your Account")
        
        with st.form("signup_form"):
            new_username = st.text_input("Choose a Username")
            new_email = st.text_input("Email Address")
            new_password = st.text_input("Choose a Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            submit = st.form_submit_button("Sign Up", use_container_width=True)
            
            if submit:
                if not all([new_username, new_email, new_password, confirm_password]):
                    st.warning("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    user_id = create_user(new_username, new_email, new_password)
                    if user_id:
                        st.success("Account created successfully! Please log in.")
                    else:
                        st.error("Username or email already exists")

def main_app():
    """Main application after login"""
    user = st.session_state.user
    
    # Refresh user data from database to get latest goals
    refreshed_user = get_user_by_id(user['id'])
    if refreshed_user:
        st.session_state.user = refreshed_user
        user = refreshed_user
    
    # Import UI components
    from ui.dashboard import show_dashboard
    from ui.chat_interface import show_chat_interface
    from ui.water_favorites import show_favorites, show_water_tracker
    from ui.reports import show_reports
    from ui.settings_ui import show_settings
    
    # Sidebar
    with st.sidebar:
        st.title(f"👋 Hello, {user['username']}!")
        st.divider()
        
        page = st.radio(
            "Navigation",
            ["🏠 Dashboard", "💬 Chat & Log", "📅 History", "⭐ Favorites", "💧 Water", "📊 Reports", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Quick stats in sidebar
        from utils.database_utils import get_daily_totals, get_today_water_total
        today = get_daily_totals(user['id'])
        water_today = get_today_water_total(user['id'])
        
        st.metric("Today's Calories", f"{today.get('total_calories', 0):.0f}")
        st.metric("Water Intake", f"{water_today} ml")
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard(user)
    elif page == "💬 Chat & Log":
        show_chat_interface(user)
    elif page == "⭐ Favorites":
        show_favorites(user)
    elif page == "💧 Water":
        show_water_tracker(user)
    elif page == "📊 Reports":
        show_reports(user)
    elif page == "⚙️ Settings":
        show_settings(user)

# Main application flow
if __name__ == "__main__":
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Show appropriate page
    if st.session_state.authenticated:
        main_app()
    else:
        login_page()
