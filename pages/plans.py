"""
StudentFit AI — Plans Page
"""

import streamlit as st
from theme import apply_theme

def show_plans_page():
    apply_theme()

    st.markdown('<div class="eyebrow">transparent concept tiers</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size: 2.8rem; margin-bottom: 14px;">Budget-Tiered Student Plans</h1>
    <p style="font-size: 1.1rem; color: var(--text-soft); max-width: 720px; margin-bottom: 35px; line-height: 1.6;">
        Named directly after the app's own budget tiers. Designed for individual dorm rooms up to campus fitness squads.
    </p>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card-dark tilt" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="mono-stat" style="color: var(--text-soft);">TIER 01 · FREE FOREVER</div>
                <h2 style="font-size: 1.8rem; margin: 10px 0 4px 0;">Cheap ($)</h2>
                <div style="font-size: 2rem; font-weight: 700; color: var(--highlighter); margin-bottom: 16px;">$0 <span style="font-size: 0.9rem; color: var(--text-soft);">/ semester</span></div>
                <ul style="list-style: none; padding-left: 0; font-size: 0.92rem; color: var(--text-soft); line-height: 1.8;">
                    <li>✓ 7-Day AI Schedule Generation</li>
                    <li>✓ Dorm Floor & Dumbbell Modes</li>
                    <li>✓ Indian & Global Cuisines</li>
                    <li>✓ Basic Grocery Checklist</li>
                    <li>✓ PDF Schedule Export</li>
                </ul>
            </div>
            <div style="margin-top: 20px; font-size: 0.78rem; color: var(--text-faint);">Concept Tier · 100% Free Live Access</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card-paper tilt" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between; border: 2px solid var(--coral);">
            <div>
                <div class="mono-stat" style="color: var(--coral);">TIER 02 · MOST POPULAR</div>
                <h2 style="font-size: 1.8rem; margin: 10px 0 4px 0; color: #14132B !important;">Moderate ($$)</h2>
                <div style="font-size: 2rem; font-weight: 700; color: var(--coral); margin-bottom: 16px;">$5 <span style="font-size: 0.9rem; color: #475569;">/ semester</span></div>
                <ul style="list-style: none; padding-left: 0; font-size: 0.92rem; color: #334155; line-height: 1.8;">
                    <li>✓ Everything in Cheap ($)</li>
                    <li>✓ Exam Stress Relief Adaptive Splits</li>
                    <li>✓ 5 Cuisines & Macro-Calculators</li>
                    <li>✓ Multi-Currency Budget Breakdown</li>
                    <li>✓ Sunday Batch-Prep Blueprints</li>
                </ul>
            </div>
            <div style="margin-top: 20px; font-size: 0.78rem; color: #64748b;">Concept Tier · Illustrative Roadmap</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card-dark tilt" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="mono-stat" style="color: var(--text-soft);">TIER 03 · CAMPUS SQUAD</div>
                <h2 style="font-size: 1.8rem; margin: 10px 0 4px 0;">Premium ($$$)</h2>
                <div style="font-size: 2rem; font-weight: 700; color: var(--lilac); margin-bottom: 16px;">$12 <span style="font-size: 0.9rem; color: var(--text-soft);">/ flat of 4</span></div>
                <ul style="list-style: none; padding-left: 0; font-size: 0.92rem; color: var(--text-soft); line-height: 1.8;">
                    <li>✓ Shared Flat Grocery Consolidation</li>
                    <li>✓ Bulk Meal Prep Sync for Roommates</li>
                    <li>✓ University Gym Progression Logs</li>
                    <li>✓ High-Speed Priority AI Neural Queue</li>
                </ul>
            </div>
            <div style="margin-top: 20px; font-size: 0.78rem; color: var(--text-faint);">Concept Tier · Illustrative Roadmap</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 Start Free on the Generator", key="plans_cta_btn"):
        st.switch_page("pages/generator.py")

if __name__ == "__main__":
    show_plans_page()
