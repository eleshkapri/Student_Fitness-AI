"""
StudentFit AI — Plan Generator (Two-Stage Profile Setup -> Sidebar Dashboard Flow)
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
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "gender": "Male", "age": 20, "weight": 70, "weight_unit": "kg",
            "height": 170, "height_unit": "cm", "goal": "Build Muscle",
            "equipment": "Full Gym", "cuisine": "Indian", "budget": "Moderate ($$)",
            "currency": "INR (₹)", "cooking_skill": "Basic Stove"
        }
    if "view_mode" not in st.session_state:
        # 'wizard' on first entry, 'dashboard' once generated
        st.session_state.view_mode = "wizard"

    api_key = get_api_key()
    model_option = "openai/gpt-oss-20b"
    use_simulation = False if api_key else True

    # =========================================================================
    # STAGE 1: FIRST-TIME FULL ENTRY WIZARD
    # =========================================================================
    if st.session_state.view_mode == "wizard" or st.session_state.plan_result is None:
        st.markdown('<div class="eyebrow">⚡ Step 1 of 1 — Personalize Your Week</div>', unsafe_allow_html=True)
        st.markdown("""
        <h1 style="font-size: 2.6rem; margin-bottom: 8px;">Student Fit Profile Setup</h1>
        <p style="font-size: 1.05rem; color: var(--text-soft); margin-bottom: 30px;">
            Configure your campus fitness constraints. Your customized 7-day schedule & budget grocery list will generate instantly.
        </p>
        """, unsafe_allow_html=True)

        prof = st.session_state.user_profile

        col_w1, col_w2 = st.columns(2)

        with col_w1:
            st.markdown("""
            <div class="card-dark" style="margin-bottom: 20px;">
                <h3 style="color: var(--neon-cyan); font-size: 1.15rem; margin-bottom: 14px;">🏃‍♂️ Campus Bio-Data</h3>
            </div>
            """, unsafe_allow_html=True)
            
            c_g, c_a = st.columns(2)
            with c_g:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(prof["gender"]))
            with c_a:
                age = st.number_input("Age", 16, 40, int(prof["age"]))

            c_wt, c_wu = st.columns([2, 1.2])
            with c_wt:
                weight = st.number_input("Weight", 30, 300, int(prof["weight"]))
            with c_wu:
                weight_unit = st.selectbox("Unit", ["kg", "lbs"], index=["kg", "lbs"].index(prof["weight_unit"]), key="wz_wu")

            c_ht, c_hu = st.columns([2, 1.2])
            with c_ht:
                height = st.number_input("Height", 100, 250, int(prof["height"]))
            with c_hu:
                height_unit = st.selectbox("Unit", ["cm", "ft/in"], index=["cm", "ft/in"].index(prof["height_unit"]), key="wz_hu")

        with col_w2:
            st.markdown("""
            <div class="card-dark" style="margin-bottom: 20px;">
                <h3 style="color: var(--neon-gold); font-size: 1.15rem; margin-bottom: 14px;">🎯 Goals & Gear</h3>
            </div>
            """, unsafe_allow_html=True)
            
            goal = st.selectbox("Fitness Target", [
                "Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"
            ], index=["Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"].index(prof["goal"]))

            equipment = st.selectbox("Available Gear", [
                "Full Gym", "Dumbbells Only", "No Equipment (Dorm)"
            ], index=["Full Gym", "Dumbbells Only", "No Equipment (Dorm)"].index(prof["equipment"]))

        st.markdown("""
        <div class="card-dark" style="margin-top: 20px; margin-bottom: 24px;">
            <h3 style="color: var(--coral); font-size: 1.15rem; margin-bottom: 14px;">🥑 Kitchen, Cuisine & Local Currency</h3>
        </div>
        """, unsafe_allow_html=True)

        c_cui, c_bud, c_cur = st.columns(3)
        with c_cui:
            cuisine = st.selectbox("Cuisine Preference", [
                "Indian", "Global", "Mediterranean", "Asian", "Vegan"
            ], index=["Indian", "Global", "Mediterranean", "Asian", "Vegan"].index(prof["cuisine"]))
        with c_bud:
            budget = st.selectbox("Budget Tier", [
                "Cheap ($)", "Moderate ($$)", "Premium ($$$)"
            ], index=["Cheap ($)", "Moderate ($$)", "Premium ($$$)"].index(prof["budget"]))
        with c_cur:
            currency = st.selectbox("Preferred Currency", [
                "INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "AED (د.إ)"
            ], index=["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "AED (د.إ)"].index(prof["currency"]))

        cooking_skill = st.select_slider(
            "Cooking Setup / Facility",
            options=["Microwave Only", "Basic Stove", "Full Chef"],
            value=prof["cooking_skill"]
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 GENERATE 7-DAY SCHEDULE & GROCERIES", key="wizard_submit_btn", use_container_width=True):
            # Save profile
            st.session_state.user_profile = {
                "age": age, "weight": weight, "weight_unit": weight_unit,
                "height": height, "height_unit": height_unit, "gender": gender, 
                "goal": goal, "equipment": equipment, "cuisine": cuisine, 
                "diet_type": "Standard", "budget": budget, "currency": currency,
                "cooking_skill": cooking_skill
            }
            st.session_state.view_mode = "dashboard"
            st.rerun()

    # =========================================================================
    # STAGE 2: SIDEBAR DASHBOARD VIEW (AFTER GENERATING)
    # =========================================================================
    else:
        prof = st.session_state.user_profile

        # SIDEBAR WITH ON-THE-GO CONTROLS
        with st.sidebar:
            st.markdown("## ⚡ Studio Controls")
            if st.button("✏️ Edit in Full View", key="switch_to_wizard_btn"):
                st.session_state.view_mode = "wizard"
                st.rerun()

            st.markdown('<div class="mono-stat" style="color: var(--neon-gold); margin-top: 10px;">🏃‍♂️ BIO-DATA</div>', unsafe_allow_html=True)
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(prof["gender"]), key="sb_gender")
            with col_s2:
                age = st.number_input("Age", 16, 40, int(prof["age"]), key="sb_age")

            col_w1, col_w2 = st.columns([2, 1.2])
            with col_w1:
                weight = st.number_input("Weight", 30, 300, int(prof["weight"]), key="sb_weight")
            with col_w2:
                weight_unit = st.selectbox("Unit", ["kg", "lbs"], index=["kg", "lbs"].index(prof["weight_unit"]), key="sb_wu")

            col_h1, col_h2 = st.columns([2, 1.2])
            with col_h1:
                height = st.number_input("Height", 100, 250, int(prof["height"]), key="sb_height")
            with col_h2:
                height_unit = st.selectbox("Unit", ["cm", "ft/in"], index=["cm", "ft/in"].index(prof["height_unit"]), key="sb_hu")

            st.markdown('<div class="mono-stat" style="color: var(--neon-cyan); margin-top: 14px;">🎯 GOALS & GEAR</div>', unsafe_allow_html=True)
            goal = st.selectbox("Fitness Target", [
                "Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"
            ], index=["Build Muscle", "Lose Weight", "Get Shredded", "Exam Stress Relief"].index(prof["goal"]), key="sb_goal")

            equipment = st.selectbox("Available Gear", [
                "Full Gym", "Dumbbells Only", "No Equipment (Dorm)"
            ], index=["Full Gym", "Dumbbells Only", "No Equipment (Dorm)"].index(prof["equipment"]), key="sb_equip")

            st.markdown('<div class="mono-stat" style="color: var(--coral); margin-top: 14px;">🥑 KITCHEN & BUDGET</div>', unsafe_allow_html=True)
            cuisine = st.selectbox("Cuisine", [
                "Indian", "Global", "Mediterranean", "Asian", "Vegan"
            ], index=["Indian", "Global", "Mediterranean", "Asian", "Vegan"].index(prof["cuisine"]), key="sb_cuisine")

            col_b1, col_b2 = st.columns([1.5, 1.5])
            with col_b1:
                budget = st.selectbox("Budget Tier", ["Cheap ($)", "Moderate ($$)", "Premium ($$$)"], index=["Cheap ($)", "Moderate ($$)", "Premium ($$$)"].index(prof["budget"]), key="sb_budget")
            with col_b2:
                currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "AED (د.إ)"], index=["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)", "CAD ($)", "AUD ($)", "AED (د.إ)"].index(prof["currency"]), key="sb_currency")

            cooking_skill = st.select_slider(
                "Cooking Skill",
                options=["Microwave Only", "Basic Stove", "Full Chef"],
                value=prof["cooking_skill"],
                key="sb_cook"
            )

            st.markdown("<br>", unsafe_allow_html=True)
            regenerate_btn = st.button("🔄 RE-GENERATE PLAN", key="sidebar_regen_btn")

        # MAIN STUDIO DASHBOARD
        col_hdr_l, col_hdr_r = st.columns([2.5, 1])
        with col_hdr_l:
            st.title("AI Planner Studio ⚡")
            st.markdown("#### Synchronized Monday–Sunday Workout & Meal Schedules")

        # Handle Generation or Display Cached
        if regenerate_btn or st.session_state.plan_result is None:
            user_profile = {
                "age": age, "weight": weight, "weight_unit": weight_unit,
                "height": height, "height_unit": height_unit, "gender": gender, 
                "goal": goal, "equipment": equipment, "cuisine": cuisine, 
                "diet_type": "Standard", "budget": budget, "currency": currency,
                "cooking_skill": cooking_skill
            }
            st.session_state.user_profile = user_profile
            
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

        # RENDER RESULTS
        if st.session_state.plan_result:
            day_plans = st.session_state.plan_result["days"]
            grocery_text = st.session_state.plan_result["grocery"]
            
            main_col, side_col = st.columns([2.4, 1.2])
            
            with main_col:
                for plan in day_plans:
                    st.markdown(f"""
                    <div class="day-card">
                        <h3 style="color: var(--neon-gold) !important; font-size: 1.3rem; border-bottom: 1px solid rgba(255, 215, 0, 0.3); padding-bottom: 6px; margin-bottom: 14px;">
                            🗓️ {plan['day']}
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown('<div class="col-box"><span class="mono-stat" style="color: var(--neon-cyan); font-weight: bold; display: block; margin-bottom: 8px;">🏋️ WORKOUT ROUTINE</span>' + plan['workout'] + '</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown('<div class="col-box"><span class="mono-stat" style="color: #ff9100; font-weight: bold; display: block; margin-bottom: 8px;">🥗 SYNCHRONIZED MEALS</span>' + plan['meal'] + '</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")

            with side_col:
                # Formatted Grocery Card in Dark Neon Style
                formatted_grocery = re.sub(
                    r'####\s*(.*)',
                    r'<h4 style="color: var(--neon-gold) !important; border-bottom: 1px solid rgba(255, 215, 0, 0.35); padding-bottom: 6px; margin-top: 18px; margin-bottom: 10px; font-size: 1.05rem;">\1</h4>',
                    grocery_text
                )
                formatted_grocery = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #fff;">\1</strong>', formatted_grocery)
                formatted_grocery = re.sub(r'\n\*\s*(.*)', r'<div style="margin-bottom: 10px; line-height: 1.5; color: #e2e8f0; font-size: 0.92rem;">• \1</div>', formatted_grocery)
                formatted_grocery = re.sub(r'^\*\s*(.*)', r'<div style="margin-bottom: 10px; line-height: 1.5; color: #e2e8f0; font-size: 0.92rem;">• \1</div>', formatted_grocery)
                formatted_grocery = formatted_grocery.replace("\n", "")

                st.markdown(f"""
                <div class="grocery-card" style="position: sticky; top: 20px;">
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

if __name__ == "__main__":
    show_generator_page()
