"""
Home Page for StudentFit AI.
Features hero section, 3D fanned deck, real-count ticker, dorm-room benefits, and student testimonials.
"""

import streamlit as st
from theme import apply_theme

def render():
    apply_theme()

    # --- HERO SECTION ---
    col_hero, col_deck = st.columns([1.2, 1], gap="large")

    with col_hero:
        st.markdown('<div class="eyebrow-caveat">built between lectures & leftovers ~</div>', unsafe_allow_html=True)
        st.markdown('<h1 style="font-size: 3.2rem; line-height: 1.15; margin-bottom: 18px;">Fitness that syncs to your <span style="color: var(--highlighter);">syllabus.</span></h1>', unsafe_allow_html=True)
        st.markdown("""
        <p style="font-size: 1.1rem; color: var(--text-soft); line-height: 1.6; margin-bottom: 28px;">
            Most fitness apps assume a full kitchen, a car, and endless free time. <strong>StudentFit AI</strong> plans around what students actually have: dorm-room gear, a real grocery budget, cooking skill, and an exam schedule that can't be ignored.
        </p>
        """, unsafe_allow_html=True)

        c_cta1, c_cta2 = st.columns([1.2, 1])
        with c_cta1:
            if st.button("⚡ Generate My Week", key="btn_hero_gen", use_container_width=True):
                st.switch_page("pages/generator.py")
        with c_cta2:
            if st.button("📖 How it Works", key="btn_hero_how", use_container_width=True):
                st.switch_page("pages/how_it_works.py")

    with col_deck:
        st.markdown("""
        <div class="hero-deck">
            <div class="deck-card deck-card-1">
                <span class="mono-label">MON</span>
                <div style="font-size: 2.2rem;">🏋️</div>
                <strong style="font-size: 0.85rem;">Push Day</strong>
            </div>
            <div class="deck-card deck-card-2">
                <span class="mono-label">TUE</span>
                <div style="font-size: 2.2rem;">⚡</div>
                <strong style="font-size: 0.85rem;">Pull Power</strong>
            </div>
            <div class="deck-card deck-card-3">
                <span class="mono-label">WED</span>
                <div style="font-size: 2.2rem;">🦵</div>
                <strong style="font-size: 0.85rem;">Legs & Core</strong>
            </div>
            <div class="deck-card deck-card-4" style="border: 2px solid var(--coral);">
                <span class="mono-label" style="color: var(--coral);">THU</span>
                <div style="font-size: 2.2rem;">🥑</div>
                <strong style="font-size: 0.85rem;">Meal Prep</strong>
            </div>
            <div class="deck-card deck-card-5">
                <span class="mono-label">FRI</span>
                <div style="font-size: 2.2rem;">💥</div>
                <strong style="font-size: 0.85rem;">Upper Body</strong>
            </div>
            <div class="deck-card deck-card-6">
                <span class="mono-label">SAT</span>
                <div style="font-size: 2.2rem;">🏃</div>
                <strong style="font-size: 0.85rem;">Full Body</strong>
            </div>
            <div class="deck-card deck-card-7">
                <span class="mono-label">SUN</span>
                <div style="font-size: 2.2rem;">🧘</div>
                <strong style="font-size: 0.85rem;">Recovery</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- REAL STAT TICKER ---
    st.markdown("""
    <div class="marquee-container">
        <div class="marquee-content">
            ⚡ 4 FITNESS GOALS &nbsp;•&nbsp; 3 GEAR TIERS &nbsp;•&nbsp; 5 CUISINES &nbsp;•&nbsp; 3 BUDGET TIERS &nbsp;•&nbsp; 3 COOKING SKILL LEVELS &nbsp;•&nbsp; 7 DAYS FULLY SYNCHRONIZED &nbsp;•&nbsp; 100% STUDENT-FOCUSED &nbsp;•&nbsp; 4 FITNESS GOALS &nbsp;•&nbsp; 3 GEAR TIERS &nbsp;•&nbsp; 5 CUISINES &nbsp;•&nbsp; 3 BUDGET TIERS &nbsp;•&nbsp; 3 COOKING SKILL LEVELS &nbsp;•&nbsp; 7 DAYS FULLY SYNCHRONIZED
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- "BUILT FOR DORM ROOMS, NOT GYM FLOORS" BAND ---
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <span class="tag-pill">STUDENT REALITY CHECK</span>
        <h2 style="font-size: 2.3rem; margin-top: 10px;">Built for dorm rooms, not gym floors.</h2>
        <p style="color: var(--text-soft); max-width: 680px; margin: 0 auto;">Everything engineered around college constraints so you stay consistent through midterms and finals.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown("""
        <div class="panel-card tilt">
            <div style="font-size: 2.4rem; margin-bottom: 12px;">🏠</div>
            <h3 style="font-size: 1.25rem; margin-bottom: 8px;">No Gym Required</h3>
            <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.6;">
                Only have 2m² of carpet next to your desk? Get bodyweight and dumbbell routines with calculated tempo and intensity.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="panel-card tilt">
            <div style="font-size: 2.4rem; margin-bottom: 12px;">💰</div>
            <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Budget Respected</h3>
            <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.6;">
                Get weekly grocery shopping lists with quantities and localized prices (₹, $, €, £) mapped to high-protein staples.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="panel-card tilt">
            <div style="font-size: 2.4rem; margin-bottom: 12px;">📚</div>
            <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Exam-Week Aware</h3>
            <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.6;">
                "Exam Stress Relief" is a first-class fitness goal that balances nervous system fatigue with brain-power nutrition.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- 3-STEP PROCESS BAND ---
    st.markdown("""
    <div style="background: var(--ink3); border: 1px solid var(--line); border-radius: 22px; padding: 40px 30px; margin: 30px 0;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="font-size: 2rem;">How Your Week Comes Together</h2>
            <p style="color: var(--text-soft);">Three quick steps to complete weekly alignment.</p>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 24px;">
            <div style="background: rgba(20, 19, 43, 0.6); padding: 22px; border-radius: 16px; border: 1px solid var(--line);">
                <div style="background: var(--coral); color: #fff; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-bottom: 12px;">1</div>
                <h4 style="color: #fff; margin-bottom: 6px;">Configure Profile</h4>
                <p style="color: var(--text-soft); font-size: 0.9rem; line-height: 1.5;">Pick your goal, available gear, cooking skill, and cuisine preference in the generator.</p>
            </div>
            <div style="background: rgba(20, 19, 43, 0.6); padding: 22px; border-radius: 16px; border: 1px solid var(--line);">
                <div style="background: var(--highlighter); color: #14132B; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-bottom: 12px;">2</div>
                <h4 style="color: #fff; margin-bottom: 6px;">AI Synchronizes Mon–Sun</h4>
                <p style="color: var(--text-soft); font-size: 0.9rem; line-height: 1.5;">Neural models align workout recovery demands directly with your budget meals.</p>
            </div>
            <div style="background: rgba(20, 19, 43, 0.6); padding: 22px; border-radius: 16px; border: 1px solid var(--line);">
                <div style="background: var(--lilac); color: #14132B; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-bottom: 12px;">3</div>
                <h4 style="color: #fff; margin-bottom: 6px;">Follow & Save PDF</h4>
                <p style="color: var(--text-soft); font-size: 0.9rem; line-height: 1.5;">Download your 1-page A4 schedule & shopping list to keep on your phone or desk.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- THREE STUDENT PERSONA TESTIMONIALS ---
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <span class="tag-pill">CAMPUS VOICES</span>
        <h2 style="font-size: 2.1rem; margin-top: 10px;">Tested across semester schedules.</h2>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3, gap="medium")
    with t1:
        st.markdown("""
        <div class="paper-card">
            <div style="font-size: 1.1rem; margin-bottom: 10px;">⭐️⭐️⭐️⭐️⭐️</div>
            <p style="font-size: 0.95rem; font-style: italic; margin-bottom: 16px;">
                "Other workout apps kept giving me salmon and asparagus recipes that cost half my weekly budget. StudentFit gave me eggs, dal, and oats that cost almost nothing and actually hit 130g protein."
            </p>
            <strong style="display: block; font-family: 'Space Mono', monospace; font-size: 0.82rem; color: var(--coral) !important;">
                3RD YEAR COMPUTER SCIENCE
            </strong>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="paper-card">
            <div style="font-size: 1.1rem; margin-bottom: 10px;">⭐️⭐️⭐️⭐️⭐️</div>
            <p style="font-size: 0.95rem; font-style: italic; margin-bottom: 16px;">
                "During midterm anatomy blocks, I switched to the Exam Stress Relief goal. 20-minute bodyweight mobility sessions and brain-boosting meals kept me energized without feeling burnt out."
            </p>
            <strong style="display: block; font-family: 'Space Mono', monospace; font-size: 0.82rem; color: var(--coral) !important;">
                2ND YEAR PRE-MED
            </strong>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="paper-card">
            <div style="font-size: 1.1rem; margin-bottom: 10px;">⭐️⭐️⭐️⭐️⭐️</div>
            <p style="font-size: 0.95rem; font-style: italic; margin-bottom: 16px;">
                "I have zero kitchen skills besides a microwave and electric kettle. The Microwave Only setting gave me high-protein oatmeal, steamed lentils, and paneer wraps with zero cooking hassle."
            </p>
            <strong style="display: block; font-family: 'Space Mono', monospace; font-size: 0.82rem; color: var(--coral) !important;">
                1ST YEAR ARCHITECTURE
            </strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- CLOSING CTA BAND ---
    st.markdown("""
    <div style="text-align: center; background: linear-gradient(135deg, rgba(255, 107, 84, 0.15) 0%, rgba(228, 255, 91, 0.1) 100%); border: 1px solid var(--coral); border-radius: 22px; padding: 45px 20px;">
        <h2 style="font-size: 2.4rem; margin-bottom: 12px;">Ready to sync your week?</h2>
        <p style="color: var(--text-soft); max-width: 600px; margin: 0 auto 24px auto;">
            Generate your personalized 7-day workout and student meal schedule in under 15 seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1, 1.2, 1])
    with col_c2:
        if st.button("🚀 Launch Generator Studio", key="btn_home_closing_cta", use_container_width=True):
            st.switch_page("pages/generator.py")

if __name__ == "__main__":
    render()
