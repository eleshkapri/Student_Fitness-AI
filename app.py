import streamlit as st
import requests
import re
from streamlit_lottie import st_lottie
from core import (
    get_api_key,
    calculate_macros,
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

# --- CUSTOM CSS (GLASSMORPHISM 3D NEON DARK THEME) ---
st.markdown("""
<style>
    /* Global App Styling */
    .stApp {
        background: linear-gradient(135deg, #09071c 0%, #17133d 50%, #15112e 100%);
        color: #ffffff;
    }

    /* ULTRA-THIN & TRANSPARENT SCROLLBAR */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.18); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0, 229, 255, 0.6); }
    
    [data-testid="stSidebar"] {
        background-color: #0d0a20 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 3D GLASSMORPHISM CARDS */
    .card-3d-home {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .card-3d-home:hover {
        border-color: rgba(0, 229, 255, 0.6);
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 229, 255, 0.2);
    }

    .day-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 22px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .day-card:hover {
        border-color: rgba(0, 229, 255, 0.6);
        transform: translateY(-2px);
    }
    
    .grocery-card {
        background: rgba(0, 0, 0, 0.38);
        border: 1px solid #FFD700;
        border-radius: 16px;
        padding: 24px 22px;
        height: 100%;
        text-align: left;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }

    /* Day Headers */
    .day-card h3 {
        color: #FFD700 !important;
        font-size: 1.35rem !important;
        margin-top: 0 !important;
        margin-bottom: 14px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid rgba(255, 215, 0, 0.3);
        padding-bottom: 8px;
    }

    /* Column Headers */
    .col-header {
        color: #00e5ff;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 10px;
        display: block;
        letter-spacing: 0.5px;
        border-bottom: 1px dashed rgba(0, 229, 255, 0.2);
        padding-bottom: 6px;
    }

    /* List Items */
    ul { list-style-type: none; padding-left: 0; }
    li { margin-bottom: 10px; font-size: 0.95rem; color: #e2e8f0; line-height: 1.6; }
    strong { color: #fff; font-weight: 600; }

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

# --- SESSION STATE ---
if "plan_result" not in st.session_state:
    st.session_state.plan_result = None
if "plan_source" not in st.session_state:
    st.session_state.plan_source = None
if "raw_response" not in st.session_state:
    st.session_state.raw_response = None

# --- SIDEBAR (EDITABLE ON THE GO) ---
with st.sidebar:
    st.markdown("## ⚡ StudentFit Setup")
    
    api_key = get_api_key()
    model_option = "openai/gpt-oss-20b"
    use_simulation = False if api_key else True
    
    st.markdown("### 🏃‍♂️ Bio-Data")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with col_s2:
        age = st.number_input("Age", 16, 40, 20)

    # Weight with Unit
    col_w1, col_w2 = st.columns([2, 1.2])
    with col_w1:
        weight = st.number_input("Weight", 30, 300, 70)
    with col_w2:
        weight_unit = st.selectbox("Unit", ["kg", "lbs"], key="w_unit")

    # Height with Unit
    col_h1, col_h2 = st.columns([2, 1.2])
    with col_h1:
        height = st.number_input("Height", 100, 250, 170)
    with col_h2:
        height_unit = st.selectbox("Unit", ["cm", "ft/in"], key="h_unit")

    st.markdown("### 🎯 Goals & Gear")
    goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"])
    equipment = st.selectbox("Available Gear", ["Full Gym", "Dumbbells Only", "No Equipment (Dorm)"])
    
    st.markdown("### 🥑 Kitchen & Budget")
    cuisine = st.selectbox("Cuisine", ["Indian", "Global", "Mediterranean", "Asian", "Vegan"])
    
    col_b1, col_b2 = st.columns([1.5, 1.5])
    with col_b1:
        budget = st.selectbox("Budget Tier", ["Cheap ($)", "Moderate ($$)", "Premium ($$$)"], index=1)
    with col_b2:
        currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "AED (د.إ)"], index=0)
        
    cooking_skill = st.select_slider("Cooking Skill", options=["Microwave Only", "Basic Stove", "Full Chef"], value="Basic Stove")
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 UPDATE & GENERATE PLAN")

# --- MULTI-PAGE TABS ---
tab_home, tab_studio, tab_macros = st.tabs([
    "🏠 Overview & Features",
    "⚡ AI Planner Studio",
    "📊 Student Macro Calculator"
])

# ==========================================
# TAB 1: 3D OVERVIEW & GUIDE
# ==========================================
with tab_home:
    col_h_text, col_h_anim = st.columns([2.5, 1])
    with col_h_text:
        st.markdown("""
        <div style="background: rgba(0, 229, 255, 0.12); border: 1px solid rgba(0, 229, 255, 0.4); color: #00e5ff; display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; margin-bottom: 12px;">
            🎓 BUILT EXCLUSIVELY FOR COLLEGE & UNIVERSITY STUDENTS
        </div>
        """, unsafe_allow_html=True)
        st.title("Smart Fitness & Nutrition on Campus")
        st.markdown("##### Hyper-personalized workouts and budget meals tailored to dorm spaces, student schedules, and local currencies.")
    with col_h_anim:
        if lottie_fitness:
            st_lottie(lottie_fitness, height=150, key="home_anim")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card-3d-home">
            <h3 style="color: #00e5ff;">🏋️ Dorm & Gym Adaptive</h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">Tailors exercises whether you have a dorm floor, dumbbells, or full university gym.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card-3d-home">
            <h3 style="color: #FFD700;">🥗 Cultural & Budget Meals</h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">Respects Indian, Mediterranean, Asian, Vegan, and Global cuisines within student budgets.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card-3d-home">
            <h3 style="color: #ff416c;">🛒 Localized Grocery List</h3>
            <p style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5;">Exact 1-person quantities with weekly price estimations in your chosen currency.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🚀 How It Works in 3 Steps")
    st.markdown("""
    1. **Fill Bio-Data in Sidebar:** Set your weight, height, goal, cooking setup, and currency.
    2. **Generate 7-Day Plan:** AI synchronizes Monday–Sunday workouts directly with synchronized high-protein student meals.
    3. **Shop & Prep:** Download your markdown grocery list and meal-prep on Sunday to save study time!
    """)

# ==========================================
# TAB 2: AI PLANNER STUDIO
# ==========================================
with tab_studio:
    if generate_btn:
        user_profile = {
            "age": age, "weight": weight, "weight_unit": weight_unit,
            "height": height, "height_unit": height_unit, "gender": gender, 
            "goal": goal, "equipment": equipment, "cuisine": cuisine, 
            "diet_type": "Standard", "budget": budget, "currency": currency,
            "cooking_skill": cooking_skill
        }
        
        with st.spinner('🗓️ AI Neural Engine is Synchronizing Your 7-Day Plan...'):
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
            else:
                st.session_state.plan_result = {"days": day_plans, "grocery": grocery_text}
                st.session_state.plan_source = source
                st.session_state.raw_response = full_response

    if st.session_state.plan_result:
        day_plans = st.session_state.plan_result["days"]
        grocery_text = st.session_state.plan_result["grocery"]
        
        main_col, side_col = st.columns([2.5, 1.2])
        
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
            formatted_grocery = re.sub(
                r'####\s*(.*)',
                r'<h4 style="color: #FFD700; border-bottom: 1px solid rgba(255, 215, 0, 0.35); padding-bottom: 8px; margin-top: 22px; margin-bottom: 14px; font-size: 1.1rem; font-weight: 700;">\1</h4>',
                grocery_text
            )
            formatted_grocery = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: white;">\1</strong>', formatted_grocery)
            formatted_grocery = re.sub(r'\n\*\s*(.*)', r'<div style="margin-bottom: 12px; line-height: 1.65; color: #e2e8f0; font-size: 0.93rem;">• \1</div>', formatted_grocery)
            formatted_grocery = re.sub(r'^\*\s*(.*)', r'<div style="margin-bottom: 12px; line-height: 1.65; color: #e2e8f0; font-size: 0.93rem;">• \1</div>', formatted_grocery)
            formatted_grocery = formatted_grocery.replace("\n", "")

            st.markdown(f"""
            <div class="grocery-card">
                {formatted_grocery}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Save Schedule (Markdown)",
                data=st.session_state.raw_response or "",
                file_name="StudentFit_Weekly_Schedule.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.success(f"✅ Generated successfully using {st.session_state.plan_source}")
    else:
        st.info("👈 Customize your profile in the sidebar and click **'UPDATE & GENERATE PLAN'** to view your schedule.")

# ==========================================
# TAB 3: STUDENT MACRO CALCULATOR
# ==========================================
with tab_macros:
    st.markdown("### 📊 Student Daily Macro & Calorie Calculator")
    st.markdown("Calculate maintenance calories and macro goals specifically tailored to campus student activity.")
    
    col_m1, col_m2 = st.columns([1, 1.2])
    with col_m1:
        st.markdown("#### Input Metrics")
        m_gender = st.selectbox("Gender", ["Male", "Female"], key="m_g")
        m_age = st.number_input("Age", 16, 40, 20, key="m_a")
        
        m_w_col, m_wu_col = st.columns([2, 1.2])
        with m_w_col:
            m_weight = st.number_input("Weight", 30, 300, 70, key="m_w")
        with m_wu_col:
            m_wunit = st.selectbox("Unit", ["kg", "lbs"], key="m_wu")
            
        m_h_col, m_hu_col = st.columns([2, 1.2])
        with m_h_col:
            m_height = st.number_input("Height", 100, 250, 170, key="m_h")
        with m_hu_col:
            m_hunit = st.selectbox("Unit", ["cm", "ft/in"], key="m_hu")
            
        m_goal = st.selectbox("Target Goal", ["Build Muscle", "Lose Weight", "Exam Stress Relief"], key="m_go")
        
    with col_m2:
        macros = calculate_macros(m_age, m_gender, m_weight, m_wunit, m_height, m_hunit, m_goal)
        st.markdown("#### Daily Nutrition Target")
        st.markdown(f"""
        <div style="background: rgba(0, 0, 0, 0.35); border: 1px solid #00e5ff; border-radius: 16px; padding: 24px;">
            <div style="font-size: 2.5rem; font-weight: 800; color: #00e5ff;">{macros['target_calories']:,} <span style="font-size: 1.1rem; color: #fff;">kcal/day</span></div>
            <p style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 18px;">BMR: {macros['bmr']} kcal | TDEE: {macros['tdee']} kcal</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; text-align: center;">
                <div style="background: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 10px;">
                    <div style="font-size: 1.4rem; font-weight: 800; color: #ff416c;">{macros['protein_g']}g</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">PROTEIN</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 10px;">
                    <div style="font-size: 1.4rem; font-weight: 800; color: #FFD700;">{macros['carbs_g']}g</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">CARBS</div>
                </div>
                <div style="background: rgba(255, 255, 255, 0.05); padding: 12px; border-radius: 10px;">
                    <div style="font-size: 1.4rem; font-weight: 800; color: #00e5ff;">{macros['fats_g']}g</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">FATS</div>
                </div>
            </div>
            <p style="margin-top: 18px; font-size: 0.9rem; color: #cbd5e1;">💧 <strong>Recommended Water:</strong> {macros['water_liters']} Liters / day</p>
        </div>
        """, unsafe_allow_html=True)