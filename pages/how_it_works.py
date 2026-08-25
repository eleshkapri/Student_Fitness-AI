"""
StudentFit AI — How It Works Page
"""

import streamlit as st
from theme import apply_theme

def show_how_it_works_page():
    apply_theme()

    st.markdown('<div class="eyebrow">simple, transparent, structured</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size: 2.8rem; margin-bottom: 14px;">How StudentFit AI Works</h1>
    <p style="font-size: 1.1rem; color: var(--text-soft); max-width: 720px; margin-bottom: 35px; line-height: 1.6;">
        Every weekly schedule is dynamically generated across three student lifestyle dimensions, ensuring full alignment between your dorm equipment, budget, and culinary heritage.
    </p>
    """, unsafe_allow_html=True)

    # --- STEP 1: BIO DATA ---
    st.markdown("""
    <div class="card-dark" style="margin-bottom: 24px;">
        <div style="display: flex; gap: 16px; align-items: flex-start;">
            <div style="background: var(--coral); color: white; font-family: 'Space Mono'; font-weight: 700; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">01</div>
            <div>
                <h3 style="font-size: 1.3rem; margin-bottom: 6px;">Campus Bio-Data Configuration</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.5; margin-bottom: 14px;">
                    Calculates metabolic energy baselines (BMR) and recommended hydration tailored to campus walking and active student lifestyles.
                </p>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Gender: Male / Female / Other</span>
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Age (16–40)</span>
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Weight (kg / lbs)</span>
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Height (cm / ft/in)</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- STEP 2: GOALS & GEAR ---
    st.markdown("""
    <div class="card-dark" style="margin-bottom: 24px;">
        <div style="display: flex; gap: 16px; align-items: flex-start;">
            <div style="background: var(--coral); color: white; font-family: 'Space Mono'; font-weight: 700; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">02</div>
            <div>
                <h3 style="font-size: 1.3rem; margin-bottom: 6px;">Goals & Equipment Adaptability</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.5; margin-bottom: 14px;">
                    Translates available gear into high-efficiency compound movements, supersets, and progressive overload schemes without requiring commercial gym machinery.
                </p>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Goals: Build Muscle / Lose Weight / Get Shredded / Exam Stress Relief</span>
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Gear: Full Gym / Dumbbells Only / No Equipment (Dorm)</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- STEP 3: KITCHEN & BUDGET ---
    st.markdown("""
    <div class="card-dark" style="margin-bottom: 24px;">
        <div style="display: flex; gap: 16px; align-items: flex-start;">
            <div style="background: var(--coral); color: white; font-family: 'Space Mono'; font-weight: 700; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">03</div>
            <div>
                <h3 style="font-size: 1.3rem; margin-bottom: 6px;">Kitchen Setup, Cuisine & Local Currency</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.5; margin-bottom: 14px;">
                    Aligns calorie and protein goals with realistic college cooking facilities, bulk staples, and student budgets in your preferred currency.
                </p>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Cuisine: Indian / Global / Mediterranean / Asian / Vegan</span>
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Budget: Cheap ($) / Moderate ($$) / Premium ($$$)</span>
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Facility: Microwave Only / Basic Stove / Full Chef</span>
                    <span class="mono-stat" style="background: rgba(246, 241, 227, 0.08); padding: 4px 10px; border-radius: 6px;">Currencies: INR (₹) / USD ($) / EUR (€) / GBP (£) / CAD / AUD / AED</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- STEP 4: MOCKED LOADING SYNC STATE ---
    st.markdown("""
    <div style="margin: 35px 0 20px 0;">
        <h3 style="font-size: 1.4rem; margin-bottom: 12px;">⚡ The Real-Time Synchronization Engine</h3>
        <p style="color: var(--text-soft); font-size: 0.95rem; margin-bottom: 20px;">
            Here is how the neural engine aligns Monday through Sunday workouts directly with your synchronized meals:
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: var(--ink3); border: 1px solid var(--line); border-radius: var(--radius); padding: 28px; text-align: center;">
        <div style="font-size: 2rem; margin-bottom: 10px;">🗓️</div>
        <h4 style="color: var(--highlighter); font-size: 1.15rem; margin-bottom: 6px;">Synchronizing your 7-day schedule with AI...</h4>
        <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 16px;">Tailoring exercises, student meals, and localized grocery budgets...</p>
        <div style="background: rgba(246, 241, 227, 0.1); border-radius: 10px; height: 8px; max-width: 450px; margin: 0 auto; overflow: hidden;">
            <div style="background: linear-gradient(90deg, var(--coral), var(--highlighter)); width: 75%; height: 100%; border-radius: 10px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Try the Generator Now", key="how_cta_btn"):
        st.switch_page("pages/generator.py")

if __name__ == "__main__":
    show_how_it_works_page()
