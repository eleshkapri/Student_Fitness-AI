"""
Student Macro Hub Page for StudentFit AI.
Interactive BMR, TDEE, Daily Protein/Carbs/Fats Calculator and Student Budget Meal Prep Tips.
"""

import streamlit as st
from theme import apply_theme
from core import calculate_macros

def render():
    apply_theme("Student Macro Hub")

    st.markdown('<div class="eyebrow-caveat">student metabolism math ~</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.8rem; margin-bottom: 10px;">Student BMR & Macro Calculator 📊</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: var(--text-soft); font-size: 1.05rem; max-width: 800px; line-height: 1.6; margin-bottom: 30px;">
        Calculate daily maintenance calories, protein requirements, and target macronutrient splits tailored to university study schedules and training.
    </p>
    """, unsafe_allow_html=True)

    col_form, col_res = st.columns([1.1, 1.4], gap="large")

    with col_form:
        st.markdown('<div class="panel-card" style="padding: 24px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="font-size: 1.3rem; margin-top: 0; color: var(--highlighter);">Personal Metrics</h3>', unsafe_allow_html=True)
        
        col_g, col_a = st.columns(2)
        with col_g:
            m_gender = st.selectbox("Gender", ["Male", "Female"], key="m_g")
        with col_a:
            m_age = st.number_input("Age", 16, 40, 20, key="m_a")

        col_w, col_wu = st.columns([2, 1.2])
        with col_w:
            m_weight = st.number_input("Weight", 30, 300, 70, key="m_w")
        with col_wu:
            m_weight_unit = st.selectbox("Unit", ["kg", "lbs"], key="m_wu")

        col_h, col_hu = st.columns([2, 1.2])
        with col_h:
            m_height = st.number_input("Height", 100, 250, 170, key="m_h")
        with col_hu:
            m_height_unit = st.selectbox("Unit", ["cm", "ft/in"], key="m_hu")

        m_goal = st.selectbox(
            "Target Goal",
            ["Build Muscle (Surplus +350 kcal)", "Lose Weight (Deficit -400 kcal)", "Exam Stress Relief & Maintain"],
            key="m_goal"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_res:
        goal_clean = "Build Muscle" if "Muscle" in m_goal else ("Lose Weight" if "Lose" in m_goal else "Exam Stress Relief")
        res = calculate_macros(m_age, m_gender, m_weight, m_weight_unit, m_height, m_height_unit, goal_clean)

        st.markdown(f"""
        <div class="panel-card" style="border: 1px solid var(--neon-cyan, #00e5ff); padding: 28px;">
            <span class="mono-label" style="color: #00e5ff;">DAILY NUTRITION TARGET</span>
            <div style="font-size: 3rem; font-weight: 800; color: #00e5ff; margin: 8px 0 4px 0;">
                {res['target_calories']:,} <span style="font-size: 1.2rem; color: #fff; font-weight: normal;">kcal / day</span>
            </div>
            <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 22px;">
                Basal Metabolic Rate (BMR): <strong>{res['bmr']} kcal</strong> | Total Daily Energy (TDEE): <strong>{res['tdee']} kcal</strong>
            </p>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 22px;">
                <div style="background: rgba(20, 19, 43, 0.7); border: 1px solid var(--line); border-radius: 12px; padding: 16px; text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 800; color: var(--coral);">{res['protein_g']}g</div>
                    <div class="mono-label" style="font-size: 0.75rem; margin-top: 4px;">PROTEIN</div>
                </div>
                <div style="background: rgba(20, 19, 43, 0.7); border: 1px solid var(--line); border-radius: 12px; padding: 16px; text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 800; color: var(--highlighter);">{res['carbs_g']}g</div>
                    <div class="mono-label" style="font-size: 0.75rem; margin-top: 4px;">CARBS</div>
                </div>
                <div style="background: rgba(20, 19, 43, 0.7); border: 1px solid var(--line); border-radius: 12px; padding: 16px; text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 800; color: #00e5ff;">{res['fats_g']}g</div>
                    <div class="mono-label" style="font-size: 0.75rem; margin-top: 4px;">FATS</div>
                </div>
            </div>

            <div style="background: rgba(20, 19, 43, 0.7); border: 1px solid var(--line); border-radius: 12px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.95rem; color: #fff;">💧 Daily Hydration Target:</span>
                <strong style="color: #00e5ff; font-size: 1.1rem;">{res['water_liters']} Liters / day</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- STUDENT BUDGET MEAL PREP TIPS ---
    st.markdown("### 🥑 Student Budget Nutrition Blueprint")
    
    t1, t2, t3, t4 = st.columns(4, gap="medium")
    with t1:
        st.markdown("""
        <div class="panel-card tilt" style="padding: 20px;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🥚</div>
            <h4 style="font-size: 1.05rem; margin-bottom: 6px; color: var(--coral);">Eggs & Soya Chunks</h4>
            <p style="color: var(--text-soft); font-size: 0.88rem; line-height: 1.5;">
                Over 25g of bioavailable protein for under $0.50 / ₹30 per serving.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="panel-card tilt" style="padding: 20px;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🍲</div>
            <h4 style="font-size: 1.05rem; margin-bottom: 6px; color: var(--highlighter);">Sunday Batch Cook</h4>
            <p style="color: var(--text-soft); font-size: 0.88rem; line-height: 1.5;">
                Boil 500g lentils and brown rice in one pot to save 45 min daily.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="panel-card tilt" style="padding: 20px;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🧠</div>
            <h4 style="font-size: 1.05rem; margin-bottom: 6px; color: #00e5ff;">Exam Week Hydration</h4>
            <p style="color: var(--text-soft); font-size: 0.88rem; line-height: 1.5;">
                Dehydration drops memory retention by 15%. Aim for 3 bottle refills.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with t4:
        st.markdown("""
        <div class="panel-card tilt" style="padding: 20px;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🥜</div>
            <h4 style="font-size: 1.05rem; margin-bottom: 6px; color: var(--coral);">Peanut Butter & Oats</h4>
            <p style="color: var(--text-soft); font-size: 0.88rem; line-height: 1.5;">
                Slow-release carbohydrates and fats for sustained energy in 3-hour lectures.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_c1, col_c2, col_c3 = st.columns([1, 1.4, 1])
    with col_c2:
        if st.button("🚀 Generate Full 7-Day Plan", use_container_width=True):
            st.switch_page("pages/generator.py")

if __name__ == "__main__":
    render()
