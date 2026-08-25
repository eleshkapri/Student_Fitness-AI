"""
StudentFit AI — Story Page
"""

import streamlit as st
from theme import apply_theme

def show_story_page():
    apply_theme()

    st.markdown('<div class="eyebrow">the student perspective</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size: 2.8rem; margin-bottom: 14px;">Why We Built StudentFit AI</h1>
    <p style="font-size: 1.15rem; color: var(--text-soft); max-width: 760px; margin-bottom: 35px; line-height: 1.6;">
        Mainstream fitness media is built for people with cars, gourmet kitchens, $150 gym memberships, and hours of daily free time. We built StudentFit AI for reality.
    </p>
    """, unsafe_allow_html=True)

    c_left, c_right = st.columns([1.5, 1])

    with c_left:
        st.markdown("""
        <div class="card-dark" style="margin-bottom: 24px;">
            <h3 style="color: var(--highlighter); font-size: 1.35rem; margin-bottom: 8px;">Built for Campus Life, Not Gym Culture</h3>
            <p style="color: var(--paper); font-size: 0.95rem; line-height: 1.6;">
                When you're balancing semester exams, 8:00 AM lectures, and part-time jobs, spending 2 hours in a commercial gym or cooking elaborate 4-course macros is impossible.
            </p>
            <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.6; margin-top: 10px;">
                StudentFit AI treats your tight budget, small dorm floor, single microwave, and exam weeks as primary constraints, generating high-yield 7-day routines that actually fit your student schedule.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        st.markdown("""
        <div class="card-paper" style="margin-bottom: 24px;">
            <div class="mono-stat" style="color: var(--coral);">WHO IT'S FOR</div>
            <ul style="list-style: none; padding-left: 0; margin-top: 12px; font-size: 0.92rem; line-height: 1.8; color: #334155;">
                <li>🏠 <strong>Dorm & Hostel Dwellers:</strong> Exercising with limited space.</li>
                <li>💰 <strong>Budget-Conscious Students:</strong> Realistic weekly grocery spending.</li>
                <li>🧠 <strong>Exam-Week Survivors:</strong> Active recovery & mental stamina.</li>
                <li>🍳 <strong>First-Time Cooks:</strong> Simple stove & microwave formulas.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⚡ Build Your Student Plan", key="story_cta_btn"):
        st.switch_page("pages/generator.py")

if __name__ == "__main__":
    show_story_page()
