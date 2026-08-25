"""
Student Macro Hub Page for StudentFit AI.
Interactive BMR, TDEE, and optimal macronutrient split calculator with student budget nutrition hacks.
"""

import streamlit as st
from theme import apply_theme
from core import StudentProfile, MacroCalculator


def render():
    apply_theme()

    st.markdown('<div class="eyebrow-caveat">daily metabolic math ~</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.8rem; margin-bottom: 8px;">Student BMR & Macro Calculator</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: var(--text-soft); font-size: 1.05rem; margin-bottom: 30px;">
        Calculate your daily maintenance calories and optimal macronutrient split for study energy and muscle growth.
    </p>
    """, unsafe_allow_html=True)

    col_input, col_results = st.columns([1, 1.2], gap="large")

    with col_input:
        st.markdown("""
        <div class="panel-card" style="padding: 24px; margin-bottom: 20px;">
            <h3 style="color: var(--highlighter); font-size: 1.25rem; margin-bottom: 18px;">Personal Metrics</h3>
        """, unsafe_allow_html=True)

        col_g, col_a = st.columns(2)
        with col_g:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0, key="macro_gender")
        with col_a:
            age = st.number_input("Age", min_value=14, max_value=80, value=20, step=1, key="macro_age")

        col_w, col_wu = st.columns([2, 1])
        with col_w:
            weight = st.number_input("Weight", min_value=30.0, max_value=300.0, value=70.0, step=0.5, key="macro_weight")
        with col_wu:
            weight_unit = st.selectbox("Unit", ["kg", "lbs"], index=0, key="macro_wunit")

        col_h, col_hu = st.columns([2, 1])
        with col_h:
            height = st.number_input("Height", min_value=100.0, max_value=250.0, value=170.0, step=1.0, key="macro_height")
        with col_hu:
            height_unit = st.selectbox("Unit", ["cm", "ft/in"], index=0, key="macro_hunit")

        goal_choice = st.selectbox(
            "Target Goal",
            [
                "Build Muscle (Surplus +350 kcal)",
                "Lose Weight / Cut (Deficit -400 kcal)",
                "Maintenance / Study Focus (TDEE)",
                "Athletic Conditioning (Surplus +150 kcal)"
            ],
            index=0,
            key="macro_goal"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # Compute using OOP domain model and calculator
    profile = StudentProfile(
        gender=gender,
        age=age,
        weight=weight,
        weight_unit=weight_unit,
        height=height,
        height_unit=height_unit,
        goal=goal_choice
    )
    macros = MacroCalculator.calculate(profile)

    # Compute percentage breakdown for segmented ratio bar
    total_cals = macros.target_calories
    protein_cals = macros.protein_g * 4
    carbs_cals = macros.carbs_g * 4
    fats_cals = macros.fats_g * 9
    total_macro_cals = max(protein_cals + carbs_cals + fats_cals, 1)

    p_pct = round((protein_cals / total_macro_cals) * 100)
    c_pct = round((carbs_cals / total_macro_cals) * 100)
    f_pct = 100 - (p_pct + c_pct)

    with col_results:
        st.markdown(f"""
        <div class="panel-card" style="padding: 26px; border: 1px solid var(--coral); background: var(--ink2); box-shadow: 0 16px 40px rgba(0,0,0,0.5);">
            <div style="font-size: 0.85rem; font-family: 'Space Mono', monospace; color: var(--text-soft); text-transform: uppercase;">Daily Target</div>
            <div style="font-size: 3.2rem; font-weight: 800; font-family: 'Space Grotesk', sans-serif; color: #00E5FF; margin: 4px 0 6px 0; line-height: 1;">
                {macros.target_calories:,} <span style="font-size: 1.2rem; color: var(--highlighter); font-weight: 600;">kcal/day</span>
            </div>
            <div style="color: var(--text-soft); font-size: 0.95rem; margin-bottom: 20px; font-family: 'Space Mono', monospace;">
                BMR: <strong style="color: #fff;">{macros.bmr:,} kcal</strong> | TDEE: <strong style="color: #fff;">{macros.tdee:,} kcal</strong>
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 24px;">
                <div style="background: rgba(255, 107, 84, 0.12); border: 1px solid var(--coral); border-radius: 12px; padding: 14px 10px; text-align: center;">
                    <div style="font-size: 1.6rem; font-weight: 800; color: var(--coral); font-family: 'Space Grotesk', sans-serif;">{macros.protein_g}g</div>
                    <div style="font-size: 0.75rem; font-weight: 700; font-family: 'Space Mono', monospace; color: #fff; letter-spacing: 0.5px;">PROTEIN</div>
                </div>
                <div style="background: rgba(228, 255, 91, 0.12); border: 1px solid var(--highlighter); border-radius: 12px; padding: 14px 10px; text-align: center;">
                    <div style="font-size: 1.6rem; font-weight: 800; color: var(--highlighter); font-family: 'Space Grotesk', sans-serif;">{macros.carbs_g}g</div>
                    <div style="font-size: 0.75rem; font-weight: 700; font-family: 'Space Mono', monospace; color: #fff; letter-spacing: 0.5px;">CARBS</div>
                </div>
                <div style="background: rgba(0, 229, 255, 0.12); border: 1px solid #00E5FF; border-radius: 12px; padding: 14px 10px; text-align: center;">
                    <div style="font-size: 1.6rem; font-weight: 800; color: #00E5FF; font-family: 'Space Grotesk', sans-serif;">{macros.fats_g}g</div>
                    <div style="font-size: 0.75rem; font-weight: 700; font-family: 'Space Mono', monospace; color: #fff; letter-spacing: 0.5px;">FATS</div>
                </div>
            </div>

            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-family: 'Space Mono', monospace; margin-bottom: 6px; color: var(--text-soft);">
                    <span>Macro Ratio Split</span>
                    <span>{p_pct}% P / {c_pct}% C / {f_pct}% F</span>
                </div>
                <div style="height: 10px; border-radius: 10px; overflow: hidden; display: flex; background: rgba(246, 241, 227, 0.1);">
                    <div style="width: {p_pct}%; background: var(--coral);" title="Protein"></div>
                    <div style="width: {c_pct}%; background: var(--highlighter);" title="Carbs"></div>
                    <div style="width: {f_pct}%; background: #00E5FF;" title="Fats"></div>
                </div>
            </div>

            <div style="display: flex; align-items: center; gap: 8px; font-size: 0.9rem; color: #00E5FF; font-weight: 600; margin-top: 16px; background: rgba(0, 229, 255, 0.08); padding: 8px 14px; border-radius: 8px;">
                <span>💧</span> Daily Water Target: <strong>{macros.water_liters} Liters/day</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3 Educational Student Cards
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 15px;">
        <div class="panel-card" style="padding: 20px;">
            <h4 style="color: var(--coral); font-size: 1.1rem; margin-bottom: 8px;">🥚 #1 Cheap Protein: Eggs & Soya</h4>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                Eggs, Paneer, Tofu, and Soya chunks provide over 20g of high-bioavailability protein for less than ₹30 / $0.50 per serving.
            </p>
        </div>
        <div class="panel-card" style="padding: 20px;">
            <h4 style="color: var(--highlighter); font-size: 1.1rem; margin-bottom: 8px;">🍚 Batch Cook Starches on Sunday</h4>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                Cook 3 days of brown rice or boil 500g chickpeas in one pot. Store in containers to save 45 minutes of daily study time.
            </p>
        </div>
        <div class="panel-card" style="padding: 20px;">
            <h4 style="color: #00E5FF; font-size: 1.1rem; margin-bottom: 8px;">💧 Study Focus & Hydration</h4>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                Dehydration drops cognitive performance by 15%. Keep a 1L water bottle at your desk and aim for 3 refills during exam weeks.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
