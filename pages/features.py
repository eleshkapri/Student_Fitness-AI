"""
StudentFit AI — Features Page
"""

import streamlit as st
from theme import apply_theme

def show_features_page():
    apply_theme()

    st.markdown('<div class="eyebrow">interactive 3d feature matrix</div>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size: 2.8rem; margin-bottom: 14px;">Six Adaptive Dimensions</h1>
    <p style="font-size: 1.1rem; color: var(--text-soft); max-width: 720px; margin-bottom: 30px; line-height: 1.6;">
        Hover or tap any card to reveal how StudentFit AI customizes your weekly schedule across all 6 core axes.
    </p>
    """, unsafe_allow_html=True)

    # --- SIX 3D FLIP CARDS ---
    st.markdown("""
    <div class="flip-grid">
        <!-- 1. Bio-Data Personalization -->
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">🏃‍♂️</div>
                    <h3>Bio-Data Personalization</h3>
                    <div class="mono-stat" style="margin-top: 8px; color: var(--coral);">AXIS 01</div>
                </div>
                <div class="flip-card-back">
                    <h4 style="color: var(--coral); margin-bottom: 6px;">Metabolic Precision</h4>
                    <p>Calculates exact BMR, campus activity multipliers, and personalized hydration targets in kg/lbs and cm/ft.</p>
                </div>
            </div>
        </div>

        <!-- 2. Goal-Driven Programming -->
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">🎯</div>
                    <h3>Goal-Driven Programming</h3>
                    <div class="mono-stat" style="margin-top: 8px; color: var(--coral);">AXIS 02</div>
                </div>
                <div class="flip-card-back">
                    <h4 style="color: var(--coral); margin-bottom: 6px;">Targeted Splits</h4>
                    <p>Build Muscle, Lose Fat, Athletic Shred, or Exam Stress Relief with progressive overload and active recovery.</p>
                </div>
            </div>
        </div>

        <!-- 3. Gear-Adaptive Workouts -->
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">🏋️</div>
                    <h3>Gear-Adaptive Workouts</h3>
                    <div class="mono-stat" style="margin-top: 8px; color: var(--coral);">AXIS 03</div>
                </div>
                <div class="flip-card-back">
                    <h4 style="color: var(--coral); margin-bottom: 6px;">Zero Equipment to Gym</h4>
                    <p>Seamlessly scales movements from dorm room floors and light dumbbells to full campus fitness centers.</p>
                </div>
            </div>
        </div>

        <!-- 4. Cuisine-Flexible Meals -->
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">🥑</div>
                    <h3>Cuisine-Flexible Meals</h3>
                    <div class="mono-stat" style="margin-top: 8px; color: var(--coral);">AXIS 04</div>
                </div>
                <div class="flip-card-back">
                    <h4 style="color: var(--coral); margin-bottom: 6px;">Authentic Flavors</h4>
                    <p>Indian, Global, Mediterranean, Asian, and Vegan meal formulas respecting your culinary culture.</p>
                </div>
            </div>
        </div>

        <!-- 5. Budget-Tiered Groceries -->
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">🛒</div>
                    <h3>Budget-Tiered Groceries</h3>
                    <div class="mono-stat" style="margin-top: 8px; color: var(--coral);">AXIS 05</div>
                </div>
                <div class="flip-card-back">
                    <h4 style="color: var(--coral); margin-bottom: 6px;">Localized Currency</h4>
                    <p>Generates 1-person weekly grocery shopping lists with exact cost estimates in INR, USD, EUR, GBP, CAD, AUD, AED.</p>
                </div>
            </div>
        </div>

        <!-- 6. Cooking-Skill Matched -->
        <div class="flip-card">
            <div class="flip-card-inner">
                <div class="flip-card-front">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">🍳</div>
                    <h3>Cooking-Skill Matched</h3>
                    <div class="mono-stat" style="margin-top: 8px; color: var(--coral);">AXIS 06</div>
                </div>
                <div class="flip-card-back">
                    <h4 style="color: var(--coral); margin-bottom: 6px;">Dorm Facility Aware</h4>
                    <p>Recipes adapted for Microwave Only, Basic Single Stove, or Full Chef kitchen facilities without wasted study time.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- MARQUEE STRIP LISTING EVERY LITERAL OPTION ---
    st.markdown("""
    <div class="marquee-container" style="margin-top: 40px;">
        <div class="marquee-track">
            <div class="marquee-item"><span>OPTION:</span> Male · Female · Other</div>
            <div class="marquee-item"><span>OPTION:</span> Build Muscle · Lose Weight · Get Shredded · Exam Stress Relief</div>
            <div class="marquee-item"><span>OPTION:</span> Full Gym · Dumbbells Only · No Equipment (Dorm)</div>
            <div class="marquee-item"><span>OPTION:</span> Indian · Global · Mediterranean · Asian · Vegan</div>
            <div class="marquee-item"><span>OPTION:</span> Cheap ($) · Moderate ($$) · Premium ($$$)</div>
            <div class="marquee-item"><span>OPTION:</span> Microwave Only · Basic Stove · Full Chef</div>
            <!-- Loop -->
            <div class="marquee-item"><span>OPTION:</span> Male · Female · Other</div>
            <div class="marquee-item"><span>OPTION:</span> Build Muscle · Lose Weight · Get Shredded · Exam Stress Relief</div>
            <div class="marquee-item"><span>OPTION:</span> Full Gym · Dumbbells Only · No Equipment (Dorm)</div>
            <div class="marquee-item"><span>OPTION:</span> Indian · Global · Mediterranean · Asian · Vegan</div>
            <div class="marquee-item"><span>OPTION:</span> Cheap ($) · Moderate ($$) · Premium ($$$)</div>
            <div class="marquee-item"><span>OPTION:</span> Microwave Only · Basic Stove · Full Chef</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Test Out the 6-Axis Generator", key="feat_cta_btn"):
        st.switch_page("pages/generator.py")

if __name__ == "__main__":
    show_features_page()
