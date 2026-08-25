"""
StudentFit AI — Main Entrypoint
Multi-page Streamlit Website using st.navigation() and st.Page() API.
"""

import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="StudentFit AI — Fitness that syncs to your syllabus",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DEFINE MULTI-PAGE NAVIGATION ---
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
how_it_works_page = st.Page("pages/how_it_works.py", title="How it Works", icon="📖")
features_page = st.Page("pages/features.py", title="Features", icon="⚡")
plans_page = st.Page("pages/plans.py", title="Plans", icon="💳")
story_page = st.Page("pages/story.py", title="Story", icon="🎓")
generator_page = st.Page("pages/generator.py", title="Plan Generator", icon="🚀")

# --- INITIALIZE NAVIGATION ---
nav = st.navigation({
    "StudentFit AI": [
        home_page,
        how_it_works_page,
        features_page,
        plans_page,
        story_page,
        generator_page
    ]
})

# Run the active page
nav.run()