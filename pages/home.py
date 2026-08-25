"""
StudentFit AI — Home Page
"""

import streamlit as st
from theme import apply_theme

def show_home_page():
    apply_theme()

    # --- HERO SECTION ---
    st.markdown('<div class="eyebrow">built between lectures & leftovers</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size: 3.2rem; line-height: 1.15; margin-bottom: 18px; max-width: 820px;">
        Fitness that syncs to your syllabus.
    </h1>
    <p style="font-size: 1.15rem; color: var(--text-soft); line-height: 1.6; max-width: 680px; margin-bottom: 28px;">
        Most fitness apps assume a full kitchen, a car, and free time. StudentFit AI plans around what students actually have: dorm-room floor space, a realistic grocery budget, quick cooking, and an exam schedule that can't be ignored.
    </p>
    """, unsafe_allow_html=True)

    col_cta1, col_cta2, _ = st.columns([1.4, 1.4, 3])
    with col_cta1:
        if st.button("🚀 Generate My Week", key="home_gen_btn", use_container_width=True):
            st.switch_page("pages/generator.py")
    with col_cta2:
        if st.button("📖 See how it works", key="home_how_btn", use_container_width=True):
            st.switch_page("pages/how_it_works.py")

    # --- HERO FANNED DECK (MON - SUN) ---
    st.markdown("""
    <div class="hero-deck-container">
        <div class="deck-card tilt" style="left: calc(50% - 330px); transform: rotate(-15deg) translateY(20px); z-index: 1;">
            <div class="deck-day">Mon</div>
            <div class="deck-emoji">🏋️</div>
            <div class="deck-tag">Push Day & Oats</div>
        </div>
        <div class="deck-card tilt" style="left: calc(50% - 220px); transform: rotate(-10deg) translateY(10px); z-index: 2;">
            <div class="deck-day">Tue</div>
            <div class="deck-emoji">💪</div>
            <div class="deck-tag">Pull & Dal Rice</div>
        </div>
        <div class="deck-card tilt" style="left: calc(50% - 110px); transform: rotate(-5deg) translateY(4px); z-index: 3;">
            <div class="deck-day">Wed</div>
            <div class="deck-emoji">🧘</div>
            <div class="deck-tag">Exam De-Stress</div>
        </div>
        <div class="deck-card tilt" style="left: calc(50% - 0px); transform: rotate(0deg) translateY(0px); z-index: 4; border: 2px solid var(--highlighter);">
            <div class="deck-day" style="color: var(--highlighter);">Thu</div>
            <div class="deck-emoji">⚡</div>
            <div class="deck-tag">Legs & Protein Wrap</div>
        </div>
        <div class="deck-card tilt" style="left: calc(50% + 110px); transform: rotate(5deg) translateY(4px); z-index: 3;">
            <div class="deck-day">Fri</div>
            <div class="deck-emoji">🔥</div>
            <div class="deck-tag">Shoulders & Abs</div>
        </div>
        <div class="deck-card tilt" style="left: calc(50% + 220px); transform: rotate(10deg) translateY(10px); z-index: 2;">
            <div class="deck-day">Sat</div>
            <div class="deck-emoji">🥊</div>
            <div class="deck-tag">Power Circuit</div>
        </div>
        <div class="deck-card tilt" style="left: calc(50% + 330px); transform: rotate(15deg) translateY(20px); z-index: 1;">
            <div class="deck-day">Sun</div>
            <div class="deck-emoji">🛒</div>
            <div class="deck-tag">Batch Meal Prep</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- SCROLLING STAT TICKER (REAL CONFIG COUNTS) ---
    st.markdown("""
    <div class="marquee-container">
        <div class="marquee-track">
            <div class="marquee-item"><span>⚡</span> 4 FITNESS GOALS</div>
            <div class="marquee-item"><span>🏋️</span> 3 GEAR TIERS</div>
            <div class="marquee-item"><span>🥑</span> 5 CUISINES</div>
            <div class="marquee-item"><span>💰</span> 3 BUDGET TIERS</div>
            <div class="marquee-item"><span>🍳</span> 3 COOKING SKILL LEVELS</div>
            <div class="marquee-item"><span>🗓️</span> 7 DAYS SYNCED</div>
            <!-- Duplicate for infinite loop -->
            <div class="marquee-item"><span>⚡</span> 4 FITNESS GOALS</div>
            <div class="marquee-item"><span>🏋️</span> 3 GEAR TIERS</div>
            <div class="marquee-item"><span>🥑</span> 5 CUISINES</div>
            <div class="marquee-item"><span>💰</span> 3 BUDGET TIERS</div>
            <div class="marquee-item"><span>🍳</span> 3 COOKING SKILL LEVELS</div>
            <div class="marquee-item"><span>🗓️</span> 7 DAYS SYNCED</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- BUILT FOR DORM ROOMS, NOT GYM FLOORS ---
    st.markdown("""
    <div style="text-align: center; margin: 40px 0 24px 0;">
        <h2 style="font-size: 2.2rem;">Built for dorm rooms, not gym floors</h2>
        <p style="color: var(--text-soft); font-size: 1rem;">Fitness programming designed around campus real estate, tight schedules, and shared kitchens.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card-dark tilt">
            <div style="font-size: 2rem; margin-bottom: 12px;">🏠</div>
            <h3 style="font-size: 1.25rem; margin-bottom: 8px;">No Gym Required</h3>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.5;">
                Get serious training volume with zero equipment on dorm floors, light dumbbells, or campus facilities.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card-dark tilt">
            <div style="font-size: 2rem; margin-bottom: 12px;">💰</div>
            <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Budget-Respected</h3>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.5;">
                Every meal plan outputs 1-person weekly grocery lists and localized cost estimates in your currency (INR, USD, EUR, etc.).
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card-dark tilt">
            <div style="font-size: 2rem; margin-bottom: 12px;">🧠</div>
            <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Exam-Week-Aware</h3>
            <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.5;">
                "Exam Stress Relief" is a first-class fitness target, balancing active recovery, mental clarity, and quick-fuel nutrition.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- THREE-CARD FEATURE PREVIEW (MIRRORING SIDEBAR) ---
    st.markdown("""
    <div style="text-align: center; margin: 60px 0 24px 0;">
        <h2 style="font-size: 2.2rem;">Driven by 3 Simple Dimensions</h2>
        <p style="color: var(--text-soft); font-size: 1rem;">No complicated tracking. Complete weekly alignment generated from your routine.</p>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown("""
        <div class="card-paper">
            <div class="mono-stat" style="color: var(--coral);">DIMENSION 01</div>
            <h3 style="margin: 10px 0 6px 0;">🏃‍♂️ Campus Bio-Data</h3>
            <p style="font-size: 0.92rem; line-height: 1.5; color: #475569;">
                Age, Gender, Weight (kg/lbs), and Height (cm/ft). Personalized to your exact student metabolic profile.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="card-paper">
            <div class="mono-stat" style="color: var(--coral);">DIMENSION 02</div>
            <h3 style="margin: 10px 0 6px 0;">🎯 Goals & Gear</h3>
            <p style="font-size: 0.92rem; line-height: 1.5; color: #475569;">
                Build Muscle, Fat Loss, Shred, or Exam Stress Relief paired with Full Gym, Dumbbells, or Dorm Floor.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="card-paper">
            <div class="mono-stat" style="color: var(--coral);">DIMENSION 03</div>
            <h3 style="margin: 10px 0 6px 0;">🥑 Kitchen & Budget</h3>
            <p style="font-size: 0.92rem; line-height: 1.5; color: #475569;">
                Cuisines (Indian, Global, Mediterranean, Asian, Vegan) + Budget Tiers + Microwave vs Basic Stove vs Chef.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- THREE TESTIMONIAL PERSONAS (YEAR + MAJOR ONLY) ---
    st.markdown("""
    <div style="text-align: center; margin: 60px 0 24px 0;">
        <h2 style="font-size: 2.2rem;">Tested Across University Campuses</h2>
        <p style="color: var(--text-soft); font-size: 1rem;">Real student routines, zero fitness influencer fluff.</p>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
        <div class="card-dark tilt">
            <p style="color: var(--paper); font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;">
                "Other apps told me to cook 4 different meals a day. StudentFit gave me a Sunday batch recipe of chickpea curry and 20-min dumbbell routines between lectures."
            </p>
            <div class="mono-stat" style="color: var(--highlighter);">2ND YEAR · COMPUTER SCIENCE</div>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="card-dark tilt">
            <p style="color: var(--paper); font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;">
                "I only have a microwave and electric kettle in my dorm. Setting cooking skill to 'Microwave Only' completely solved my student protein intake."
            </p>
            <div class="mono-stat" style="color: var(--highlighter);">3RD YEAR · BIOTECHNOLOGY</div>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="card-dark tilt">
            <p style="color: var(--paper); font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;">
                "The exam stress relief option during finals saved my sleep and neck stiffness. It balances campus walks with quick bodyweight workouts."
            </p>
            <div class="mono-stat" style="color: var(--highlighter);">FINAL YEAR · MECHANICAL ENG</div>
        </div>
        """, unsafe_allow_html=True)

    # --- CLOSING CTA BAND ---
    st.markdown("""
    <div style="background: var(--ink3); border: 1px solid var(--line); border-radius: var(--radius); padding: 40px; text-align: center; margin: 60px 0 20px 0;">
        <div class="eyebrow">your semester starts here</div>
        <h2 style="font-size: 2.3rem; margin: 10px 0 16px 0;">Ready to synchronize your weekly plan?</h2>
        <p style="color: var(--text-soft); max-width: 600px; margin: 0 auto 24px auto;">
            Generate your personalized 7-day workout routine and localized student grocery list in 5 seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_b_center, _ = st.columns([2, 3])
    with col_b_center:
        if st.button("⚡ Launch Weekly Generator", key="home_bottom_cta", use_container_width=True):
            st.switch_page("pages/generator.py")

if __name__ == "__main__":
    show_home_page()
