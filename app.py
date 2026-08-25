import streamlit as st
import requests
import re
from streamlit_lottie import st_lottie
from core import (
    get_api_key,
    parse_ai_response,
    generate_plan_mock,
    generate_plan_real,
    CANDIDATE_MODELS
)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="StudentFit AI ⚡",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD ASSETS WITH CACHING ---
@st.cache_data(show_spinner=False, ttl=3600)
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

lottie_fitness = load_lottieurl("https://lottie.host/5a8e0108-0118-4981-b54c-1296c0542368/jY8yHnN2Fm.json")

# --- CUSTOM CSS (GLASSMORPHISM NEON DARK THEME) ---
st.markdown("""
<style>
    /* Global App Styling */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    [data-testid="stSidebar"] {
        background-color: #121212 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* GLASSMORPHISM CARDS */
    .day-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .day-card:hover {
        border-color: rgba(0, 229, 255, 0.6);
        transform: translateY(-2px);
    }
    
    .grocery-card {
        background: rgba(0, 0, 0, 0.35);
        border: 1px solid #FFD700;
        border-radius: 16px;
        padding: 22px;
        height: 100%;
        text-align: left;
    }

    /* Day Headers */
    .day-card h3 {
        color: #FFD700 !important;
        font-size: 1.4rem !important;
        margin-top: 0 !important;
        margin-bottom: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.3);
        padding-bottom: 6px;
    }

    /* Column Headers */
    .col-header {
        color: #00e5ff;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 8px;
        display: block;
        letter-spacing: 0.3px;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        border: none;
        padding: 14px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 17px;
        margin-top: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 22px rgba(255, 75, 43, 0.7);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "plan_result" not in st.session_state:
    st.session_state.plan_result = None
if "plan_source" not in st.session_state:
    st.session_state.plan_source = None
if "raw_response" not in st.session_state:
    st.session_state.raw_response = None

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("## ⚡ StudentFit Setup")
    
    api_key = get_api_key()
    model_option = "openai/gpt-oss-20b"
    use_simulation = False if api_key else True
    
    st.markdown("### 🏃‍♂️ Bio-Data")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", 40, 150, 70)
    with col_s2:
        age = st.number_input("Age", 16, 40, 20)
        height = st.number_input("Height (cm)", 140, 220, 170)

    st.markdown("### 🎯 Goals & Gear")
    goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"])
    equipment = st.selectbox("Available Gear", ["Full Gym", "Dumbbells Only", "No Equipment (Dorm)"])
    
    st.markdown("### 🥑 Kitchen & Budget")
    cuisine = st.selectbox("Cuisine", ["Indian", "Global", "Mediterranean", "Asian", "Vegan"])
    budget = st.select_slider("Budget Tier", options=["Cheap ($)", "Moderate ($$)", "Premium ($$$)"], value="Moderate ($$)")
    cooking_skill = st.select_slider("Cooking Skill", options=["Microwave Only", "Basic Stove", "Full Chef"], value="Basic Stove")
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 GENERATE WEEKLY PLAN")

# --- MAIN PAGE HEADER ---
col_header, col_anim = st.columns([2.5, 1])

with col_header:
    st.title("StudentFit AI ⚡")
    st.markdown("#### Your Hyper-Personalized 7-Day Aligned Schedule")
    if not st.session_state.plan_result and not generate_btn:
        st.info("👈 Fill out your profile in the sidebar to generate a synchronized Workout & Meal schedule.")

with col_anim:
    if lottie_fitness:
        st_lottie(lottie_fitness, height=140, key="anim_top")

st.markdown("---")

# --- GENERATION HANDLER ---
if generate_btn:
    user_profile = {
        "age": age, "weight": weight, "height": height, "gender": gender, 
        "goal": goal, "equipment": equipment, "cuisine": cuisine, 
        "diet_type": "Standard", "budget": budget, "cooking_skill": cooking_skill
    }
    
    with st.spinner('🗓️ Synchronizing your 7-day schedule with AI...'):
        if use_simulation or not api_key:
            full_response = generate_plan_mock(user_profile)
            source = "Simulation (Demo Mode)"
        else:
            full_response, used_model = generate_plan_real(user_profile, api_key, model_option)
            source = f"Groq ({used_model})" if used_model else "Groq"

    if full_response.startswith("Error:"):
        st.error(f"❌ AI Generation Error: {full_response}")
    else:
        day_plans, grocery_text = parse_ai_response(full_response)
        if not day_plans:
            st.error("⚠️ Output formatting error. Please retry generation.")
            with st.expander("🔍 View Raw Output"):
                st.code(full_response)
        else:
            st.session_state.plan_result = {"days": day_plans, "grocery": grocery_text}
            st.session_state.plan_source = source
            st.session_state.raw_response = full_response

# --- RENDER RESULTS FROM SESSION STATE ---
if st.session_state.plan_result:
    day_plans = st.session_state.plan_result["days"]
    grocery_text = st.session_state.plan_result["grocery"]
    
    main_col, side_col = st.columns([2.5, 1])
    
    with main_col:
        for plan in day_plans:
            st.markdown(f"""
            <div class="day-card">
                <h3>🗓️ {plan['day']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<span class="col-header">🏋️ WORKOUT ROUTINE</span>', unsafe_allow_html=True)
                st.markdown(plan['workout'])
            with c2:
                st.markdown('<span class="col-header">🥗 SYNCHRONIZED MEALS</span>', unsafe_allow_html=True)
                st.markdown(plan['meal'])
            
            st.markdown("---")

    with side_col:
        # Formatted Grocery Card
        formatted_grocery = re.sub(
            r'####\s*(.*)',
            r'<h4 style="color: #FFD700; border-bottom: 1px solid #FFD700; padding-bottom: 5px; margin-top: 15px;">\1</h4>',
            grocery_text
        )
        formatted_grocery = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: white;">\1</strong>', formatted_grocery)
        formatted_grocery = re.sub(r'\n\*\s*(.*)', r'<div style="margin-bottom: 5px; color: #e0e0e0;">• \1</div>', formatted_grocery)
        formatted_grocery = re.sub(r'^\*\s*(.*)', r'<div style="margin-bottom: 5px; color: #e0e0e0;">• \1</div>', formatted_grocery)
        formatted_grocery = formatted_grocery.replace("\n", "")

        st.markdown(f"""
        <div class="grocery-card">
            {formatted_grocery}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        # Download Schedule Button
        st.download_button(
            label="📥 Save Schedule (Markdown)",
            data=st.session_state.raw_response or "",
            file_name="StudentFit_7Day_Schedule.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.success(f"✅ Generated successfully using {st.session_state.plan_source}")