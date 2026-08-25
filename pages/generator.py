"""
Generator Page for StudentFit AI.
The core 7-day AI fitness and nutrition scheduler styled with the top navbar design system.
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
    apply_theme("AI Generator")

    # --- SESSION STATE INITIALIZATION ---
    if "plan_result" not in st.session_state:
        st.session_state.plan_result = None
    if "plan_source" not in st.session_state:
        st.session_state.plan_source = None
    if "raw_response" not in st.session_state:
        st.session_state.raw_response = None

    # --- HEADER ---
    st.markdown('<div class="eyebrow-caveat">7-day synchronized alignment ~</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.8rem; margin-bottom: 8px;">AI Planner Studio ⚡</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: var(--text-soft); font-size: 1rem; margin-bottom: 25px;">
        Synchronizing dorm-adaptive workout routines with budget-friendly student meal plans and grocery lists.
    </p>
    """, unsafe_allow_html=True)

    # --- TWO COLUMN STUDIO WORKSPACE ---
    col_setup, col_results = st.columns([1.1, 2.2], gap="large")

    with col_setup:
        st.markdown('<div class="panel-card" style="padding: 24px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1.3rem; margin-top: 0; color: #fff;">⚙️ Studio Setup</h3>', unsafe_allow_html=True)
        
        api_key = get_api_key()
        model_option = "openai/gpt-oss-20b"
        use_simulation = False if api_key else True

        st.markdown('<span class="mono-label">🏃‍♂️ CAMPUS BIO-DATA</span>', unsafe_allow_html=True)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="gen_g")
        with col_s2:
            age = st.number_input("Age", 16, 40, 20, key="gen_a")

        col_w1, col_w2 = st.columns([2, 1.2])
        with col_w1:
            weight = st.number_input("Weight", 30, 300, 70, key="gen_w")
        with col_w2:
            weight_unit = st.selectbox("Unit", ["kg", "lbs"], key="gen_wu")

        col_h1, col_h2 = st.columns([2, 1.2])
        with col_h1:
            height = st.number_input("Height", 100, 250, 170, key="gen_h")
        with col_h2:
            height_unit = st.selectbox("Unit", ["cm", "ft/in"], key="gen_hu")

        st.markdown('<br><span class="mono-label">🎯 GOALS & GEAR</span>', unsafe_allow_html=True)
        goal = st.selectbox("Fitness Goal", ["Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"], key="gen_goal")
        equipment = st.selectbox("Available Gear", ["Full Gym", "Dumbbells Only", "No Equipment (Dorm)"], key="gen_eq")

        st.markdown('<br><span class="mono-label">🥑 KITCHEN & BUDGET</span>', unsafe_allow_html=True)
        cuisine = st.selectbox("Cuisine", ["Indian", "Global", "Mediterranean", "Asian", "Vegan"], key="gen_cui")
        
        col_b1, col_b2 = st.columns([1.5, 1.5])
        with col_b1:
            budget = st.selectbox("Budget Tier", ["Cheap ($)", "Moderate ($$)", "Premium ($$$)"], index=1, key="gen_bud")
        with col_b2:
            currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "AED (د.إ)"], index=0, key="gen_curr")
            
        cooking_skill = st.select_slider("Cooking Skill", options=["Microwave Only", "Basic Stove", "Full Chef"], value="Basic Stove", key="gen_cook")

        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("🚀 GENERATE 7-DAY PLAN", key="btn_gen_submit", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_results:
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

        # --- RENDER RESULTS ---
        if st.session_state.plan_result:
            day_plans = st.session_state.plan_result["days"]
            grocery_text = st.session_state.plan_result["grocery"]
            
            col_plan_sched, col_plan_groc = st.columns([1.5, 1.1], gap="medium")
            
            with col_plan_sched:
                st.markdown('<span class="mono-label">🗓️ MONDAY – SUNDAY SCHEDULE</span>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                for plan in day_plans:
                    st.markdown(f"""
                    <div class="paper-card" style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid rgba(20,19,43,0.1); padding-bottom: 6px; margin-bottom: 12px;">
                            <h3 style="margin: 0; font-size: 1.3rem; color: #14132B !important;">🗓️ {plan['day'].upper()}</h3>
                            <span class="tag-pill" style="background: rgba(20,19,43,0.08); border-color: rgba(20,19,43,0.2); color: #14132B;">SYNCED</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c_w, c_m = st.columns(2, gap="small")
                    with c_w:
                        st.markdown("""
                        <div style="background: rgba(20, 19, 43, 0.5); border: 1px solid var(--line); border-radius: 12px; padding: 14px; margin-bottom: 16px;">
                            <span class="mono-label" style="color: var(--highlighter);">🏋️ WORKOUT ROUTINE</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(plan['workout'])
                    with c_m:
                        st.markdown("""
                        <div style="background: rgba(20, 19, 43, 0.5); border: 1px solid var(--line); border-radius: 12px; padding: 14px; margin-bottom: 16px;">
                            <span class="mono-label" style="color: var(--coral);">🥗 SYNCHRONIZED MEALS</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(plan['meal'])
                    
                    st.markdown("<hr style='border-color: var(--line); margin: 15px 0;'>", unsafe_allow_html=True)

            with col_plan_groc:
                st.markdown('<span class="mono-label">🛒 1-PERSON GROCERY LIST</span>', unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                
                formatted_grocery = re.sub(
                    r'####\s*(.*)',
                    r'<h4 style="color: var(--coral) !important; border-bottom: 1px solid rgba(20,19,43,0.15); padding-bottom: 6px; margin-top: 16px; margin-bottom: 8px; font-size: 1rem;">\1</h4>',
                    grocery_text
                )
                formatted_grocery = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #14132B !important;">\1</strong>', formatted_grocery)
                formatted_grocery = re.sub(r'\n\*\s*(.*)', r'<div style="margin-bottom: 6px; line-height: 1.5; color: #2D2A4A; font-size: 0.9rem;">• \1</div>', formatted_grocery)
                formatted_grocery = re.sub(r'^\*\s*(.*)', r'<div style="margin-bottom: 6px; line-height: 1.5; color: #2D2A4A; font-size: 0.9rem;">• \1</div>', formatted_grocery)
                formatted_grocery = formatted_grocery.replace("\n", "")

                st.markdown(f"""
                <div class="paper-card" style="position: sticky; top: 20px;">
                    {formatted_grocery}
                    <hr style="border-color: rgba(20,19,43,0.15); margin: 18px 0 12px 0;">
                    <div style="font-size: 0.8rem; font-family: 'Space Mono', monospace; color: #64748B;">
                        Generated via {st.session_state.plan_source}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                pdf_bytes = create_fitness_pdf(st.session_state.raw_response or "")
                if pdf_bytes:
                    st.download_button(
                        label="📥 Save Schedule (PDF)",
                        data=pdf_bytes,
                        file_name="StudentFit_Weekly_Schedule.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        else:
            st.markdown("""
            <div class="panel-card" style="text-align: center; padding: 70px 30px;">
                <div style="font-size: 3.5rem; margin-bottom: 16px;">⚡</div>
                <h3 style="font-size: 1.5rem; margin-bottom: 10px;">Your 7-Day Studio Canvas</h3>
                <p style="color: var(--text-soft); max-width: 520px; margin: 0 auto 20px auto; line-height: 1.6;">
                    Configure your campus bio-data, fitness goal, available gear, and cuisine on the left, then click <strong>"GENERATE 7-DAY PLAN"</strong> to create your schedule.
                </p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
