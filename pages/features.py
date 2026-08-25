"""
Features Page for StudentFit AI.
Features 6 3D interactive flip cards for each configuration axis and a full literal options marquee strip.
"""

import streamlit as st
from theme import apply_theme

def render():
    apply_theme()

    st.markdown('<div class="eyebrow-caveat">complete feature breakdown ~</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 2.8rem; margin-bottom: 12px;">Six Core Pillars of StudentFit AI</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="color: var(--text-soft); font-size: 1.1rem; max-width: 800px; line-height: 1.6; margin-bottom: 35px;">
        Hover or tap each card to flip and discover how every dimension adapts simultaneously to campus life.
    </p>
    """, unsafe_allow_html=True)

    # --- 6 FLIP CARDS (2 ROWS OF 3) ---
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown("""
        <div class="flip-card-container">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.5rem; margin-bottom: 12px;">🏃‍♂️</div>
                    <h3 style="font-size: 1.25rem;">Bio-Data Personalization</h3>
                    <p style="color: var(--text-soft); font-size: 0.85rem; margin-top: 6px;">Hover to reveal details</p>
                </div>
                <div class="flip-card-back">
                    <h4 style="font-size: 1.1rem; margin-bottom: 8px;">Adaptive Calorie Math</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5; color: #fff;">
                        Calculates baseline metabolic rates according to student age, gender, and metrics in kg/lbs and cm/ft.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="flip-card-container">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.5rem; margin-bottom: 12px;">🎯</div>
                    <h3 style="font-size: 1.25rem;">Goal-Driven Programming</h3>
                    <p style="color: var(--text-soft); font-size: 0.85rem; margin-top: 6px;">Hover to reveal details</p>
                </div>
                <div class="flip-card-back">
                    <h4 style="font-size: 1.1rem; margin-bottom: 8px;">Targeted Splits</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5; color: #fff;">
                        Switches workout intensity and macro surpluses/deficits between muscle bulking, shredding, and exam stress relief.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="flip-card-container">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.5rem; margin-bottom: 12px;">🏋️</div>
                    <h3 style="font-size: 1.25rem;">Gear-Adaptive Workouts</h3>
                    <p style="color: var(--text-soft); font-size: 0.85rem; margin-top: 6px;">Hover to reveal details</p>
                </div>
                <div class="flip-card-back">
                    <h4 style="font-size: 1.1rem; margin-bottom: 8px;">Space & Equipment Fit</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5; color: #fff;">
                        Substitutes exercises seamlessly whether you have access to a university gym, light dumbbells, or just dorm floor space.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3, gap="medium")

    with c4:
        st.markdown("""
        <div class="flip-card-container">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.5rem; margin-bottom: 12px;">🥗</div>
                    <h3 style="font-size: 1.25rem;">Cuisine-Flexible Meals</h3>
                    <p style="color: var(--text-soft); font-size: 0.85rem; margin-top: 6px;">Hover to reveal details</p>
                </div>
                <div class="flip-card-back">
                    <h4 style="font-size: 1.1rem; margin-bottom: 8px;">Cultural Respect</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5; color: #fff;">
                        Builds recipes around Indian, Mediterranean, Asian, Vegan, and Global staples without forcing unfamiliar western diets.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div class="flip-card-container">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.5rem; margin-bottom: 12px;">🛒</div>
                    <h3 style="font-size: 1.25rem;">Budget-Tiered Groceries</h3>
                    <p style="color: var(--text-soft); font-size: 0.85rem; margin-top: 6px;">Hover to reveal details</p>
                </div>
                <div class="flip-card-back">
                    <h4 style="font-size: 1.1rem; margin-bottom: 8px;">1-Person Precise List</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5; color: #fff;">
                        Generates a weekly shopping list with exact quantities and realistic price totals in INR, USD, EUR, GBP, CAD, AUD, AED.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown("""
        <div class="flip-card-container">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.5rem; margin-bottom: 12px;">🍳</div>
                    <h3 style="font-size: 1.25rem;">Cooking-Skill Recipes</h3>
                    <p style="color: var(--text-soft); font-size: 0.85rem; margin-top: 6px;">Hover to reveal details</p>
                </div>
                <div class="flip-card-back">
                    <h4 style="font-size: 1.1rem; margin-bottom: 8px;">Appliance Matching</h4>
                    <p style="font-size: 0.9rem; line-height: 1.5; color: #fff;">
                        Ensures all suggested meal prep can be accomplished with your exact setup, from Microwave Only to Basic Stove or Full Chef.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- COMPLETE LITERAL MARQUEE STRIP ---
    st.markdown("""
    <div style="margin: 30px 0;">
        <span class="mono-label" style="display: block; margin-bottom: 8px;">EVERY LITERAL CONFIGURATION AXIS:</span>
        <div class="marquee-container">
            <div class="marquee-content">
                MALE • FEMALE • OTHER • BUILD MUSCLE • LOSE WEIGHT • GET SHREDDED • EXAM STRESS RELIEF • FULL GYM • DUMBBELLS ONLY • NO EQUIPMENT (DORM) • INDIAN • GLOBAL • MEDITERRANEAN • ASIAN • VEGAN • CHEAP ($) • MODERATE ($$) • PREMIUM ($$$) • MICROWAVE ONLY • BASIC STOVE • FULL CHEF • INR (₹) • USD ($) • EUR (€) • GBP (£) • CAD ($) • AUD ($) • AED (د.إ)
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3 = st.columns([1, 1.4, 1])
    with col_b2:
        if st.button("⚡ Test All Features in Generator", use_container_width=True):
            st.switch_page("pages/generator.py")

if __name__ == "__main__":
    render()
