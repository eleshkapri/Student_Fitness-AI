"""
StudentFit AI — Generator Page (Interactive Weekly Plan Studio)
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

def show_generator_page():
    apply_theme()

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
        with col_s2:
            age = st.number_input("Age", 16, 40, 20)

        # Weight with Unit
        col_w1, col_w2 = st.columns([2, 1.2])
        with col_w1:
            weight = st.number_input("Weight", 30, 300, 70)
        with col_w2:
            weight_unit = st.selectbox("Unit", ["kg", "lbs"], key="w_unit_gen")

        # Height with Unit
        col_h1, col_h2 = st.columns([2, 1.2])
        with col_h1:
            height = st.number_input("Height", 100, 250, 170)
        with col_h2:
            height_unit = st.selectbox("Unit", ["cm", "ft/in"], key="h_unit_gen")

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
        generate_btn = st.button("🚀 GENERATE WEEKLY PLAN", key="gen_submit_btn")

    # --- MAIN PAGE HEADER ---
    st.markdown('<div class="eyebrow">interactive planner studio</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size: 2.8rem; margin-bottom: 8px;">Weekly Plan Generator</h1>
    <p style="font-size: 1.05rem; color: var(--text-soft); margin-bottom: 25px;">
        Synchronized Monday–Sunday workouts, macro-dense meals, and localized grocery lists.
    </p>
    """, unsafe_allow_html=True)

    # --- GENERATION HANDLER ---
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
            st.error(f"❌ AI Generation Error: {full_response}")
        else:
            day_plans, grocery_text = parse_ai_response(full_response)
            if not day_plans:
                st.error("⚠️ Output formatting error. Please retry generation.")
            else:
                st.session_state.plan_result = {"days": day_plans, "grocery": grocery_text}
                st.session_state.plan_source = source
                st.session_state.raw_response = full_response

    # --- RENDER RESULTS ---
    if st.session_state.plan_result:
        day_plans = st.session_state.plan_result["days"]
        grocery_text = st.session_state.plan_result["grocery"]
        
        main_col, side_col = st.columns([2.5, 1.2])
        
        with main_col:
            for plan in day_plans:
                st.markdown(f"""
                <div class="card-paper" style="margin-bottom: 22px;">
                    <h3 style="color: #14132B !important; font-size: 1.3rem; border-bottom: 1px solid rgba(0,0,0,0.12); padding-bottom: 6px; margin-bottom: 14px;">
                        🗓️ {plan['day']}
                    </h3>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown('<div class="mono-stat" style="color: var(--coral); margin-bottom: 6px;">🏋️ WORKOUT ROUTINE</div>', unsafe_allow_html=True)
                    st.markdown(plan['workout'])
                with c2:
                    st.markdown('<div class="mono-stat" style="color: var(--highlighter); margin-bottom: 6px;">🥗 SYNCHRONIZED MEALS</div>', unsafe_allow_html=True)
                    st.markdown(plan['meal'])
                
                st.markdown("---")

        with side_col:
            # Formatted Grocery Card in Paper Style
            formatted_grocery = re.sub(
                r'####\s*(.*)',
                r'<h4 style="color: #14132B !important; border-bottom: 1px solid rgba(0,0,0,0.15); padding-bottom: 6px; margin-top: 18px; margin-bottom: 10px; font-size: 1.05rem;">\1</h4>',
                grocery_text
            )
            formatted_grocery = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_grocery)
            formatted_grocery = re.sub(r'\n\*\s*(.*)', r'<div style="margin-bottom: 10px; line-height: 1.5; color: #334155; font-size: 0.92rem;">• \1</div>', formatted_grocery)
            formatted_grocery = re.sub(r'^\*\s*(.*)', r'<div style="margin-bottom: 10px; line-height: 1.5; color: #334155; font-size: 0.92rem;">• \1</div>', formatted_grocery)
            formatted_grocery = formatted_grocery.replace("\n", "")

            st.markdown(f"""
            <div class="card-paper" style="position: sticky; top: 20px;">
                {formatted_grocery}
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
                st.download_button(
                    label="📥 Save Plan (.md)",
                    data=st.session_state.raw_response or "",
                    file_name="StudentFit_Weekly_Schedule.md",
                    mime="text/markdown",
                    use_container_width=True
                )

        st.success(f"✅ Generated successfully using {st.session_state.plan_source}")
    else:
        st.markdown("""
        <div class="card-dark" style="text-align: center; padding: 50px 30px; margin-top: 20px;">
            <div style="font-size: 2.2rem; margin-bottom: 12px;">👈</div>
            <h3 style="font-size: 1.3rem; margin-bottom: 8px;">Configure in the Sidebar</h3>
            <p style="color: var(--text-soft); font-size: 0.95rem; max-width: 500px; margin: 0 auto;">
                Set your student bio-data, fitness goal, available gear, and cuisine in the left sidebar, then click <strong>"GENERATE WEEKLY PLAN"</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_generator_page()
