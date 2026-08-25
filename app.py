"""
StudentFit AI — Main Entry Point
Configures st.navigation() across all 6 cohesive pages using Streamlit's modern multi-page API.
"""

import streamlit as st

# --- GLOBAL CONFIGURATION ---
st.set_page_config(
    page_title="StudentFit AI — Fitness that Syncs to Your Syllabus",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DEFINE MULTI-PAGE NAVIGATION ---
pages = [
    st.Page("pages/home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/how_it_works.py", title="How it Works", icon="📖"),
    st.Page("pages/features.py", title="Features", icon="✨"),
    st.Page("pages/plans.py", title="Plans & Tiers", icon="🏷️"),
    st.Page("pages/story.py", title="Our Story", icon="💡"),
    st.Page("pages/generator.py", title="AI Generator", icon="⚡"),
]

# Run router
pg = st.navigation(pages)
pg.run()