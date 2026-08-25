"""
Generator Page for StudentFit AI.
The core 7-day AI fitness and nutrition scheduler styled cohesively with the shared theme.
"""

import streamlit as st
import re
from theme import apply_theme
from planner.llm_client import (
    get_api_key,
    parse_ai_response,
    generate_plan_mock,
    generate_plan_real,
    create_fitness_pdf
)

def render():
    apply_theme()

    # --- SESSION STATE INITIALIZATION ---
    if "plan_result" not in st.session_state:
        st.session_state.plan_result = None
    if "plan_source" not in st.session_state:
        st.session_state.plan_source = None
    if "raw_response" not in st.session_state:
        st.session_state.raw_response = None

    # --- SIDEBAR WIZARD CONTROLS ---
    with st.sidebar:
        st.markdown('<div class="eyebrow-caveat" style="font-size: 1.3rem;">studio setup ~</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="font-size: 1.5rem; margin-top: 0;">⚡ StudentFit Controls</h2>', unsafe_allow_html=True)
        
        api_key = get_api_key()
        model_option = "openai/gpt-oss-20b"
        use_simulation = False if api_key else True

        st.markdown('<span class="mono-label">🏃‍♂️ CAMPUS BIO-DATA</span>', unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=None, placeholder="Select Gender")
        with col_s2:
            age = st.number_input("Age", min_value=16, max_value=40, value=None, placeholder="e.g. 20")

        col_w1, col_w2 = st.columns([2, 1.2])
        with col_w1:
            weight = st.number_input("Weight", min_value=30, max_value=300, value=None, placeholder="e.g. 70")
        with col_w2:
            weight_unit = st.selectbox("Unit", ["kg", "lbs"], index=0, key="w_unit")

        col_h1, col_h2 = st.columns([2, 1.2])
        with col_h1:
            height = st.number_input("Height", min_value=100, max_value=250, value=None, placeholder="e.g. 170")
        with col_h2:
            height_unit = st.selectbox("Unit", ["cm", "ft/in"], index=0, key="h_unit")

        st.markdown('<br><span class="mono-label">🎯 GOALS & GEAR</span>', unsafe_allow_html=True)
        goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"], index=None, placeholder="Select Fitness Goal")
        equipment = st.selectbox("Available Gear", ["Full Gym", "Dumbbells Only", "No Equipment (Dorm)"], index=None, placeholder="Select Available Gear")

        st.markdown('<br><span class="mono-label">🥑 KITCHEN & BUDGET</span>', unsafe_allow_html=True)
        cuisine = st.selectbox("Cuisine", ["Indian", "Global", "Mediterranean", "Asian", "Vegan"], index=None, placeholder="Select Cuisine")
        
        col_b1, col_b2 = st.columns([1.5, 1.5])
        with col_b1:
            budget = st.selectbox("Budget Tier", ["Cheap ($)", "Moderate ($$)", "Premium ($$$)"], index=None, placeholder="Select Budget Tier")
        with col_b2:
            currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "AED (د.إ)"], index=None, placeholder="Select Currency")
            
        cooking_skill = st.selectbox("Cooking Skill", ["Microwave Only", "Basic Stove", "Full Chef"], index=None, placeholder="Select Cooking Setup")

        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🚀 GENERATE WEEKLY PLAN", use_container_width=True)

    # --- MAIN STUDIO CANVAS ---
    st.markdown('<div class="eyebrow-caveat">7-day synchronized alignment ~</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.8rem; margin-bottom: 8px;">AI Planner Studio ⚡</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: var(--text-soft); font-size: 1rem; margin-bottom: 25px;">
        Synchronizing dorm-adaptive workout routines with budget-friendly student meal plans.
    </p>
    """, unsafe_allow_html=True)

    if generate_btn:
        if not all([gender, age, weight, height, goal, equipment, cuisine, budget, currency, cooking_skill]):
            st.warning("⚠️ Please fill in all information fields (Age, Weight, Height, Goal, Equipment, Cuisine, etc.) to generate your personalized plan!")
        else:
            user_profile = {
                "age": age, "weight": weight, "weight_unit": weight_unit,
                "height": height, "height_unit": height_unit, "gender": gender, 
                "goal": goal, "equipment": equipment, "cuisine": cuisine, 
                "diet_type": "Standard", "budget": budget, "currency": currency,
                "cooking_skill": cooking_skill
            }
            
            with st.spinner('🗓️ Synchronizing your 7-day schedule with AI... Tailoring exercises, student meals, and localized grocery budgets...'):
                if use_simulation or not api_key:
                    full_response = generate_plan_mock(user_profile)
                    source = "Simulation (Demo Mode)"
                else:
                    full_response, used_model = generate_plan_real(user_profile, api_key, model_option)
                    source = f"Groq ({used_model})" if used_model else "Groq"

        if full_response.startswith("Error:"):
            st.error(f"❌ Generation Error: {full_response}")
        else:
            day_plans, grocery_text = parse_ai_response(full_response)
            if not day_plans:
                st.error("⚠️ Output formatting error. Please retry generation.")
            else:
                st.session_state.plan_result = {"days": day_plans, "grocery": grocery_text}
                st.session_state.plan_source = source
                st.session_state.raw_response = full_response

    # --- RENDER RESULTS IN PAPER CARDS ---
    if st.session_state.plan_result:
        day_plans = st.session_state.plan_result["days"]
        grocery_text = st.session_state.plan_result["grocery"]
        
        main_col, side_col = st.columns([2.2, 1.3], gap="large")
        
        with main_col:
            st.markdown('<span class="mono-label">🗓️ MONDAY – SUNDAY SCHEDULE</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            for plan in day_plans:
                st.markdown(f"""
                <div class="panel-card" style="margin-bottom: 24px; padding: 22px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--line); padding-bottom: 8px; margin-bottom: 14px;">
                        <h3 style="margin: 0; font-size: 1.35rem; color: var(--highlighter) !important;">🗓️ {plan['day'].upper()}</h3>
                        <span class="tag-pill">SYNCHRONIZED</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div style="background: rgba(20, 19, 43, 0.7); border: 1px solid rgba(255, 107, 84, 0.3); border-radius: 14px; padding: 16px;">
                            <strong style="color: var(--coral) !important; display: block; margin-bottom: 8px; font-size: 0.95rem; letter-spacing: 0.5px;">🏋️ WORKOUT ROUTINE</strong>
                            <div style="color: #FFFFFF; font-size: 0.92rem; line-height: 1.6;">{plan['workout']}</div>
                        </div>
                        <div style="background: rgba(20, 19, 43, 0.7); border: 1px solid rgba(228, 255, 91, 0.3); border-radius: 14px; padding: 16px;">
                            <strong style="color: var(--highlighter) !important; display: block; margin-bottom: 8px; font-size: 0.95rem; letter-spacing: 0.5px;">🥗 SYNCHRONIZED MEALS</strong>
                            <div style="color: #FFFFFF; font-size: 0.92rem; line-height: 1.6;">{plan['meal']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with side_col:
            st.markdown('<span class="mono-label">🛒 1-PERSON GROCERY LIST</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            formatted_grocery = re.sub(
                r'####\s*(.*)',
                r'<h4 style="color: var(--highlighter) !important; border-bottom: 1px solid var(--line); padding-bottom: 6px; margin-top: 18px; margin-bottom: 10px; font-size: 1.1rem; font-weight: 700;">\1</h4>',
                grocery_text
            )
            formatted_grocery = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: var(--coral) !important;">\1</strong>', formatted_grocery)
            formatted_grocery = re.sub(r'\n\*\s*(.*)', r'<div style="margin-bottom: 10px; line-height: 1.6; color: #FFFFFF; font-size: 0.93rem;">• \1</div>', formatted_grocery)
            formatted_grocery = re.sub(r'^\*\s*(.*)', r'<div style="margin-bottom: 10px; line-height: 1.6; color: #FFFFFF; font-size: 0.93rem;">• \1</div>', formatted_grocery)
            formatted_grocery = formatted_grocery.replace("\n", "")

            st.markdown(f"""
            <div class="panel-card" style="position: sticky; top: 30px; border: 1px solid var(--coral); padding: 24px;">
                {formatted_grocery}
                <hr style="border-color: var(--line); margin: 20px 0 15px 0;">
                <div style="font-size: 0.8rem; font-family: 'Space Mono', monospace; color: var(--text-soft);">
                    Generated via {st.session_state.plan_source}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            pdf_bytes = create_fitness_pdf(st.session_state.raw_response or "")
            if pdf_bytes:
                st.download_button(
                    label="📥 Save Plan (PDF)",
                    data=pdf_bytes,
                    file_name="StudentFit_Weekly_Schedule.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
    else:
        st.markdown("""
        <div class="panel-card" style="text-align: center; padding: 60px 30px;">
            <div style="font-size: 3rem; margin-bottom: 14px;">👈</div>
            <h3 style="font-size: 1.4rem; margin-bottom: 8px;">Configure your profile in the sidebar</h3>
            <p style="color: var(--text-soft); max-width: 500px; margin: 0 auto 20px auto;">
                Set your bio-data, fitness goal, available gear, and budget tier in the left sidebar, then click <strong>"GENERATE WEEKLY PLAN"</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
