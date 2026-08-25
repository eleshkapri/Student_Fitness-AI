"""
StudentFit AI — Main Entry Point
Registers Home & Features, AI Planner Studio, and Student Macro Hub with hidden sidebar navigation.
"""

import streamlit as st

# --- GLOBAL CONFIGURATION ---
st.set_page_config(
    page_title="StudentFit AI — Smart Fitness & Nutrition",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- DEFINE 3 CORE PAGES ---
pages = [
    st.Page("pages/home.py", title="Home & Features", icon="🏠", default=True),
    st.Page("pages/generator.py", title="AI Planner Studio", icon="⚡"),
    st.Page("pages/macros.py", title="Student Macro Hub", icon="📊"),
]

# Run router with hidden sidebar navigation so the custom top navbar is used
pg = st.navigation(pages, position="hidden")
pg.run()