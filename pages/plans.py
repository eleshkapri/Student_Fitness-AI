"""
Plans Page for StudentFit AI.
Displays 3 conceptual tiers named after the app's budget language: Cheap, Moderate, and Premium.
"""

import streamlit as st
from theme import apply_theme

def render():
    apply_theme("Plans")

    st.markdown('<div class="eyebrow-caveat">transparent tiers ~</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.8rem; margin-bottom: 12px;">Student Plans & Tiers</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: var(--text-soft); font-size: 1.1rem; max-width: 800px; line-height: 1.6; margin-bottom: 35px;">
        Named after our budget philosophy. (Note: Pricing below is illustrative and conceptual — the core AI generator is 100% free for all students).
    </p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown("""
        <div class="panel-card tilt">
            <span class="mono-label" style="color: var(--text-soft);">TIER 1</span>
            <h3 style="font-size: 1.5rem; margin: 8px 0 4px 0;">Cheap Tier</h3>
            <div style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 14px;">$0 <span style="font-size: 0.9rem; color: var(--text-soft); font-weight: normal;">/ forever</span></div>
            <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 20px; line-height: 1.5;">
                Essential 7-day synchronization for individual students on tight hostel budgets.
            </p>
            <hr style="border-color: var(--line); margin-bottom: 18px;">
            <ul style="list-style-type: none; padding-left: 0; color: var(--text-soft); font-size: 0.9rem; line-height: 1.7;">
                <li>✅ 7-Day Mon–Sun Plan Generation</li>
                <li>✅ Dorm & Bodyweight Exercises</li>
                <li>✅ 1-Person Weekly Grocery Checklist</li>
                <li>✅ Local Currency Conversions</li>
                <li>✅ PDF Export</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="panel-card tilt" style="border: 2px solid var(--highlighter); background: var(--ink3);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="mono-label" style="color: var(--highlighter);">TIER 2 • MOST POPULAR</span>
            </div>
            <h3 style="font-size: 1.5rem; margin: 8px 0 4px 0; color: var(--highlighter);">Moderate Tier</h3>
            <div style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 14px;">$3 <span style="font-size: 0.9rem; color: var(--text-soft); font-weight: normal;">/ semester (concept)</span></div>
            <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 20px; line-height: 1.5;">
                Advanced exam block optimization with multiple cuisine swaps and bulk prep guides.
            </p>
            <hr style="border-color: var(--line); margin-bottom: 18px;">
            <ul style="list-style-type: none; padding-left: 0; color: #fff; font-size: 0.9rem; line-height: 1.7;">
                <li>✅ Everything in Cheap Tier</li>
                <li>✅ Exam Stress Relief Auto-Tuning</li>
                <li>✅ Multi-Cuisine Meal Swaps</li>
                <li>✅ High-Protein Grocery Bulk Cheatsheets</li>
                <li>✅ Unlimited Re-generations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="panel-card tilt">
            <span class="mono-label" style="color: var(--coral);">TIER 3</span>
            <h3 style="font-size: 1.5rem; margin: 8px 0 4px 0;">Premium Tier</h3>
            <div style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 14px;">$8 <span style="font-size: 0.9rem; color: var(--text-soft); font-weight: normal;">/ room (concept)</span></div>
            <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 20px; line-height: 1.5;">
                Designed for dorm flatmates and student housemates pooling shared groceries and recipes.
            </p>
            <hr style="border-color: var(--line); margin-bottom: 18px;">
            <ul style="list-style-type: none; padding-left: 0; color: var(--text-soft); font-size: 0.9rem; line-height: 1.7;">
                <li>✅ Everything in Moderate Tier</li>
                <li>✅ Shared Flat Grocery Pooling List</li>
                <li>✅ Roommate Synchronized Meal Prep</li>
                <li>✅ Priority Neural Fallback Cascade</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 1.4, 1])
    with col_b2:
        if st.button("⚡ Use Full Free AI Generator", use_container_width=True):
            st.switch_page("pages/generator.py")

if __name__ == "__main__":
    render()
