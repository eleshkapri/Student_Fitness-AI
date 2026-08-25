"""
How It Works Page for StudentFit AI.
Walks through each real configuration axis with live option breakdowns and simulated AI synchronization.
"""

import streamlit as st
import time
from theme import apply_theme

def render():
    apply_theme()

    st.markdown('<div class="eyebrow-caveat">step by step logic ~</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.8rem; margin-bottom: 12px;">How StudentFit AI Works</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: var(--text-soft); font-size: 1.1rem; max-width: 800px; line-height: 1.6; margin-bottom: 35px;">
        Unlike generic fitness apps that give one-size-fits-all routines, StudentFit AI calculates exercises, meals, and weekly grocery quantities based on your simultaneous constraints.
    </p>
    """, unsafe_allow_html=True)

    # --- STEP 1: BIO-DATA ---
    st.markdown("""
    <div class="panel-card" style="margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;">
            <span class="tag-pill">STEP 1</span>
            <h3 style="margin: 0; font-size: 1.4rem;">Campus Bio-Data</h3>
        </div>
        <p style="color: var(--text-soft); font-size: 0.95rem; margin-bottom: 16px;">
            Sets the foundational calorie expenditure and metabolic baseline for student campus walking and study sessions.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 14px;">
            <div style="background: rgba(20, 19, 43, 0.6); padding: 14px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">GENDER</span>
                <div style="font-weight: 600; margin-top: 4px; color: #fff;">Male / Female / Other</div>
            </div>
            <div style="background: rgba(20, 19, 43, 0.6); padding: 14px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">AGE</span>
                <div style="font-weight: 600; margin-top: 4px; color: #fff;">16 – 40 Years</div>
            </div>
            <div style="background: rgba(20, 19, 43, 0.6); padding: 14px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">WEIGHT</span>
                <div style="font-weight: 600; margin-top: 4px; color: #fff;">30 – 300 (kg or lbs)</div>
            </div>
            <div style="background: rgba(20, 19, 43, 0.6); padding: 14px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">HEIGHT</span>
                <div style="font-weight: 600; margin-top: 4px; color: #fff;">100 – 250 (cm or ft/in)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- STEP 2: GOALS & GEAR ---
    st.markdown("""
    <div class="panel-card" style="margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;">
            <span class="tag-pill" style="background: rgba(255, 107, 84, 0.15); border-color: var(--coral); color: var(--coral);">STEP 2</span>
            <h3 style="margin: 0; font-size: 1.4rem;">Goals & Available Gear</h3>
        </div>
        <p style="color: var(--text-soft); font-size: 0.95rem; margin-bottom: 16px;">
            Adapts daily progressive overload and tempo to your physical training space.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <div style="background: rgba(20, 19, 43, 0.6); padding: 16px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">4 FITNESS GOALS</span>
                <ul style="margin-top: 8px; padding-left: 18px; color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                    <li><strong>Build Muscle:</strong> Hypertrophy volume + calorie surplus</li>
                    <li><strong>Lose Weight:</strong> High-density protein + moderate calorie deficit</li>
                    <li><strong>Get Shredded:</strong> Compound conditioning + athletic power</li>
                    <li><strong>Exam Stress Relief:</strong> Nervous system recovery + mobility & brain focus</li>
                </ul>
            </div>
            <div style="background: rgba(20, 19, 43, 0.6); padding: 16px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">3 GEAR TIERS</span>
                <ul style="margin-top: 8px; padding-left: 18px; color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                    <li><strong>Full Gym:</strong> Barbell racks, cables, leg press, dumbbells</li>
                    <li><strong>Dumbbells Only:</strong> Unilateral variations & timed TUT sets</li>
                    <li><strong>No Equipment (Dorm):</strong> Calisthenics, isometric holds, floor cardio</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- STEP 3: KITCHEN & BUDGET ---
    st.markdown("""
    <div class="panel-card" style="margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;">
            <span class="tag-pill" style="background: rgba(156, 140, 255, 0.15); border-color: var(--lilac); color: var(--lilac);">STEP 3</span>
            <h3 style="margin: 0; font-size: 1.4rem;">Kitchen Setup, Cuisine & Local Currency</h3>
        </div>
        <p style="color: var(--text-soft); font-size: 0.95rem; margin-bottom: 16px;">
            Guarantees meal plans you can actually afford and cook within your student housing rules.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px;">
            <div style="background: rgba(20, 19, 43, 0.6); padding: 16px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">5 CUISINES</span>
                <p style="color: #fff; margin-top: 6px; font-size: 0.9rem;">Indian, Global, Mediterranean, Asian, Vegan</p>
            </div>
            <div style="background: rgba(20, 19, 43, 0.6); padding: 16px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">3 BUDGET TIERS</span>
                <p style="color: #fff; margin-top: 6px; font-size: 0.9rem;">Cheap ($), Moderate ($$), Premium ($$$)</p>
            </div>
            <div style="background: rgba(20, 19, 43, 0.6); padding: 16px; border-radius: 12px; border: 1px solid var(--line);">
                <span class="mono-label">3 COOKING SKILLS</span>
                <p style="color: #fff; margin-top: 6px; font-size: 0.9rem;">Microwave Only, Basic Stove, Full Chef</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- STEP 4: MOCKED LOADING STATE SHOWCASE ---
    st.markdown("""
    <div style="background: var(--ink3); border: 1px dashed var(--line); border-radius: 22px; padding: 30px; margin: 30px 0;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
            <span class="tag-pill">STEP 4</span>
            <h3 style="margin: 0; font-size: 1.3rem;">AI Synchronization Preview</h3>
        </div>
        <p style="color: var(--text-soft); font-size: 0.92rem; margin-bottom: 20px;">
            Here is a simulation of the live neural alignment state generated when you trigger your weekly schedule:
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div style="background: rgba(20, 19, 43, 0.85); border: 1px solid var(--coral); border-radius: 16px; padding: 24px; text-align: center;">
            <h3 style="color: var(--highlighter); font-size: 1.25rem; margin-bottom: 6px;">🗓️ Synchronizing your 7-day schedule with AI...</h3>
            <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 16px;">
                Tailoring exercises, student meals, and localized grocery budgets...
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(85)

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1.4, 1])
    with col_btn2:
        if st.button("🚀 Try Generator With Your Profile", use_container_width=True):
            st.switch_page("pages/generator.py")

if __name__ == "__main__":
    render()
