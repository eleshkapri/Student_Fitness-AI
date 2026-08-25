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
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col_s2:
            age = st.number_input("Age", 16, 40, 20)

        col_w1, col_w2 = st.columns([2, 1.2])
        with col_w1:
            weight = st.number_input("Weight", 30, 300, 70)
        with col_w2:
            weight_unit = st.selectbox("Unit", ["kg", "lbs"], key="w_unit")

        col_h1, col_h2 = st.columns([2, 1.2])
        with col_h1:
            height = st.number_input("Height", 100, 250, 170)
        with col_h2:
            height_unit = st.selectbox("Unit", ["cm", "ft/in"], key="h_unit")

        st.markdown('<br><span class="mono-label">🎯 GOALS & GEAR</span>', unsafe_allow_html=True)
        goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"])
        equipment = st.selectbox("Available Gear", ["Full Gym", "Dumbbells Only", "No Equipment (Dorm)"])

        st.markdown('<br><span class="mono-label">🥑 KITCHEN & BUDGET</span>', unsafe_allow_html=True)
        cuisine = st.selectbox("Cuisine", ["Indian", "Global", "Mediterranean", "Asian", "Vegan"])
        
        col_b1, col_b2 = st.columns([1.5, 1.5])
        with col_b1:
            budget = st.selectbox("Budget Tier", ["Cheap ($)", "Moderate ($$)", "Premium ($$$)"], index=1)
        with col_b2:
            currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "AED (د.إ)"], index=0)
            
        cooking_skill = st.select_slider("Cooking Skill", options=["Microwave Only", "Basic Stove", "Full Chef"], value="Basic Stove")

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
                <div class="paper-card" style="margin-bottom: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(20,19,43,0.1); padding-bottom: 8px; margin-bottom: 14px;">
                        <h3 style="margin: 0; font-size: 1.4rem; color: #14132B !important;">🗓️ {plan['day'].upper()}</h3>
                        <span class="tag-pill" style="background: rgba(20,19,43,0.08); border-color: rgba(20,19,43,0.2); color: #14132B;">SYNCHRONIZED</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                c_w, c_m = st.columns(2, gap="medium")
                with c_w:
                    st.markdown("""
                    <div style="background: rgba(20, 19, 43, 0.5); border: 1px solid var(--line); border-radius: 14px; padding: 18px; margin-bottom: 20px;">
                        <span class="mono-label" style="color: var(--highlighter);">🏋️ WORKOUT ROUTINE</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(plan['workout'])
                with c_m:
                    st.markdown("""
                    <div style="background: rgba(20, 19, 43, 0.5); border: 1px solid var(--line); border-radius: 14px; padding: 18px; margin-bottom: 20px;">
                        <span class="mono-label" style="color: var(--coral);">🥗 SYNCHRONIZED MEALS</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(plan['meal'])
                
                st.markdown("<hr style='border-color: var(--line); margin: 20px 0;'>", unsafe_allow_html=True)

        with side_col:
            st.markdown('<span class="mono-label">🛒 1-PERSON GROCERY LIST</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            formatted_grocery = re.sub(
                r'####\s*(.*)',
                r'<h4 style="color: var(--coral) !important; border-bottom: 1px solid rgba(20,19,43,0.15); padding-bottom: 6px; margin-top: 18px; margin-bottom: 10px; font-size: 1.05rem;">\1</h4>',
                grocery_text
            )
            formatted_grocery = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #14132B !important;">\1</strong>', formatted_grocery)
            formatted_grocery = re.sub(r'\n\*\s*(.*)', r'<div style="margin-bottom: 8px; line-height: 1.5; color: #2D2A4A;">• \1</div>', formatted_grocery)
            formatted_grocery = re.sub(r'^\*\s*(.*)', r'<div style="margin-bottom: 8px; line-height: 1.5; color: #2D2A4A;">• \1</div>', formatted_grocery)
            formatted_grocery = formatted_grocery.replace("\n", "")

            st.markdown(f"""
            <div class="paper-card" style="position: sticky; top: 30px;">
                {formatted_grocery}
                <hr style="border-color: rgba(20,19,43,0.15); margin: 20px 0 15px 0;">
                <div style="font-size: 0.8rem; font-family: 'Space Mono', monospace; color: #64748B;">
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
