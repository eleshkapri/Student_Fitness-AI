"""
Story Page for StudentFit AI.
Narrative on why StudentFit AI was created and who it is built for.
"""

import streamlit as st
from theme import apply_theme

def render():
    apply_theme()

    st.markdown('<div class="eyebrow-caveat">our mission & philosophy ~</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.8rem; margin-bottom: 12px;">Built for Students, Not Gym Culture</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="panel-card" style="margin: 25px 0 35px 0; border-left: 4px solid var(--highlighter);">
        <p style="font-size: 1.15rem; line-height: 1.7; color: #fff; margin-bottom: 16px;">
            The fitness industry is designed for working adults with fully equipped kitchens, cars for weekly supermarket runs, disposable income for specialty supplements, and predictable 9-to-5 schedules.
        </p>
        <p style="font-size: 1.05rem; line-height: 1.7; color: var(--text-soft); margin-bottom: 0;">
            When students try to follow these plans, they hit walls immediately: dorm floors with zero equipment, tight budgets that can't afford fresh salmon and avocados, single-induction or microwave cooking limits, and exam weeks where high-intensity training leads straight to burnout.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Who StudentFit AI Is Built For")

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        st.markdown("""
        <div class="panel-card tilt" style="margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 8px;">🏠</div>
            <h3 style="font-size: 1.3rem; margin-bottom: 6px;">1. Dorm & Hostel Dwellers</h3>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                Students living in residence halls with limited floor area. Workouts adapt to bodyweight, bands, or university gyms without requiring commute time.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="panel-card tilt">
            <div style="font-size: 2rem; margin-bottom: 8px;">💵</div>
            <h3 style="font-size: 1.3rem; margin-bottom: 6px;">2. Budget-Conscious Students</h3>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                Anyone working with strict weekly grocery spending. Every recipe prioritizes high-protein staple foods like eggs, lentils, oats, tofu, and peanut butter.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="panel-card tilt" style="margin-bottom: 20px;">
            <div style="font-size: 2rem; margin-bottom: 8px;">🧠</div>
            <h3 style="font-size: 1.3rem; margin-bottom: 6px;">3. Exam-Week Survivors</h3>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                During midterms and finals, the priority is cognitive focus and stress relief. Training volume dials down to active recovery and brain-supporting nutrition.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="panel-card tilt">
            <div style="font-size: 2rem; margin-bottom: 8px;">🍳</div>
            <h3 style="font-size: 1.3rem; margin-bottom: 6px;">4. First-Time Cooks</h3>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.6;">
                Students cooking for themselves for the first time with basic appliances. Simple batch prep instructions that take under 20 minutes.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 1.4, 1])
    with col_b2:
        if st.button("⚡ Build Your Student Plan Now", use_container_width=True):
            st.switch_page("pages/generator.py")

if __name__ == "__main__":
    render()
