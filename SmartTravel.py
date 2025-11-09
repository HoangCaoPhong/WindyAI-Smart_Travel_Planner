import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.auth import render_login_page
from src.pages.page_dashboard import render_dashboard
from src.pages.page_discover import render_discover_page
from src.pages.page_home import render_home_page, render_about_page, render_features_page
from src.pages.page_recognize import render_recognition_page
from src.pages.page_profile import render_profile_page
from src.utils.db_utils import init_db
from src.utils.constants import PAGE_TITLE, PAGE_LAYOUT, PRIMARY_COLOR, BACKGROUND_COLOR

# --- Cấu hình Trang & Theme ---
st.set_page_config(
    page_title=PAGE_TITLE,
    layout=PAGE_LAYOUT,
)

# Apply custom CSS
css_path = os.path.join(os.path.dirname(__file__), "static", "css", "style.css")
with open(css_path, encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Additional CSS to force white background and remove black bars
st.markdown("""
    <style>
        /* Force white background everywhere */
        .stApp, .main, body, html {
            background-color: #FFFFFF !important;
        }
        
        /* Remove black decoration bars */
        [data-testid="stDecoration"] {
            display: none !important;
        }
        
        /* Force white for app view container */
        [data-testid="stAppViewContainer"] {
            background-color: #FFFFFF !important;
        }
        
        /* === COMPLETE FIX FOR BLACK BARS === */
        
        /* Root cause: The navigation menu doesn't extend to full viewport width
           The black bars are actually the .stApp background showing through */
        
        /* Step 1: Make the entire app background white - NO BLACK ANYWHERE */
        body, html, .stApp, 
        [data-testid="stAppViewContainer"],
        [data-testid="stDecoration"] {
            background-color: #FFFFFF !important;
        }
        
    /* Step 2: Make the navigation menu TRULY full width by breaking out of container */
    /* Target the element-container that contains the streamlit_option_menu iframe */
    .main .block-container > div:has(iframe[title*="streamlit_option_menu"]) {
        width: 100vw !important;
        position: relative;
        left: 50% !important;
        right: 50% !important;
        margin-left: -50vw !important;
        margin-right: -50vw !important;
        padding: 0 !important;
        background-color: #E8F1FA !important;
    }
    
    /* The vertical block containing the iframe */
    [data-testid="stVerticalBlock"]:has(iframe[title*="streamlit_option_menu"]) {
        width: 100% !important;
        padding: 0 !important;
        background-color: #E8F1FA !important;
    }
    
    /* The element-container with the iframe */
    .element-container:has(iframe[title*="streamlit_option_menu"]) {
        width: 100% !important;
        background-color: #E8F1FA !important;
        padding: 0.5rem 0 !important;
    }
    
    /* The iframe itself should be centered and scaled up 1.5x */
    iframe[title*="streamlit_option_menu"] {
        display: block !important;
        margin: 0 auto !important;
        max-width: 1200px !important;
        transform: scale(1.5) !important;
        transform-origin: center center !important;
        height: 93px !important;
    }
    
    /* Adjust container to accommodate scaled iframe - minimal padding */
    .element-container:has(iframe[title*="streamlit_option_menu"]) {
        padding: 0.5rem 0 !important;
        min-height: auto !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 0 !important;
    }
    
    [data-testid="stVerticalBlock"]:has(iframe[title*="streamlit_option_menu"]) {
        padding: 0 !important;
        margin: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* Remove any border/divider lines near nav */
    .main .block-container > div:has(iframe[title*="streamlit_option_menu"]) + * {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
        /* Step 3: Keep other content centered with proper width */
        .main .block-container {
            max-width: 1200px;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Step 4: Ensure no other element tries to be full width unless intended */
        .element-container {
            background-color: transparent !important;
        }
        
        [data-testid="stVerticalBlock"] {
            background-color: transparent !important;
        }
        
        /* Remove extra spacing after navigation */
        .main .block-container {
            padding-top: 0 !important;
        }
        
        /* Hide any horizontal lines/dividers */
        hr {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Ensure database is initialized on startup
init_db()

# --- Khởi tạo Session State với Flask backend ---
import requests as req

# Try to restore session from Flask backend
if 'session_checked' not in st.session_state:
    try:
        response = req.get('http://localhost:5000/api/session', timeout=1)
        if response.ok:
            data = response.json()
            st.session_state['logged_in'] = data.get('logged_in', False)
            st.session_state['username'] = data.get('username', '')
            st.session_state['user_id'] = data.get('user_id', None)
    except:
        # Flask backend not running, use default values
        pass
    st.session_state['session_checked'] = True

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

# Sync session to Flask backend whenever it changes
def sync_session_to_backend():
    """Sync Streamlit session to Flask backend"""
    try:
        req.post('http://localhost:5000/api/session', 
                json={
                    'logged_in': st.session_state.get('logged_in', False),
                    'username': st.session_state.get('username', ''),
                    'user_id': st.session_state.get('user_id', None)
                },
                timeout=1)
    except:
        pass  # Backend not available

# --- A. LOGIC ĐIỀU HƯỚNG (PHẦN CHÍNH) ---

if not st.session_state['logged_in']:
    # ---- 1. GIAO DIỆN CHƯA ĐĂNG NHẬP (NAV NGANG CÔNG KHAI) ----
    selected = option_menu(
        menu_title=None,
        options=["Home", "About", "Tính năng", "Đăng nhập"],
        icons=["house", "info-circle", "star", "box-arrow-in-right"],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#E8F1FA", "width": "100%"},
            "nav-link": {"color": "#000000", "font-weight": "500"},
            "nav-link-selected": {"background-color": PRIMARY_COLOR, "color": "#FFFFFF"},
        }
    )
    
    if selected == "Home":
        render_home_page()
    elif selected == "About":
        render_about_page()
    elif selected == "Tính năng":
        render_features_page()
    elif selected == "Đăng nhập":
        render_login_page()

else:
    # ---- 2. GIAO DIỆN ĐÃ ĐĂNG NHẬP (NAV NGANG THÀNH VIÊN) ----
    selected = option_menu(
        menu_title=PAGE_TITLE,
        options=["Dashboard", "Khám phá", "Nhận diện", "Hồ sơ", "Đăng xuất"],
        icons=["speedometer2", "search", "image", "person-circle", "box-arrow-left"],
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#E8F1FA", "width": "100%"},
            "nav-link": {"color": "#000000", "font-weight": "500"},
            "nav-link-selected": {"background-color": PRIMARY_COLOR, "color": "#FFFFFF"},
            "menu-title": {"color": "#000000", "font-weight": "600"},
        }
    )

    if selected == "Dashboard":
        render_dashboard(st.session_state.get('username', ''))
    elif selected == "Khám phá":
        render_discover_page()
    elif selected == "Nhận diện":
        render_recognition_page()
    elif selected == "Hồ sơ":
        render_profile_page()
    elif selected == "Đăng xuất":
        # Clear Flask backend session
        try:
            req.delete('http://localhost:5000/api/session', timeout=1)
        except:
            pass
        
        st.session_state.clear()
        st.session_state['logged_in'] = False
        st.rerun()
