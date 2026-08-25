"""
Theme Module for StudentFit AI.
Defines design tokens, typography, custom CSS, ambient animations, top navigation bar, and shared JS.
"""

import streamlit as st
import streamlit.components.v1 as components

def apply_theme(active_page: str = "Home"):
    """Injects design system styles and renders the top navigation bar."""
    css = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --ink: #14132B;
            --ink2: #1C1A42;
            --ink3: #242155;
            --paper: #F6F1E3;
            --highlighter: #E4FF5B;
            --coral: #FF6B54;
            --lilac: #9C8CFF;
            --text-soft: #B7B3DA;
            --text-faint: #8582AC;
            --line: rgba(246,241,227,0.14);
            --radius: 22px;
        }

        /* HIDE DEFAULT STREAMLIT SIDEBAR & COLLAPSE CONTROL */
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        .stMainBlockContainer {
            padding-top: 12px !important;
            padding-bottom: 60px !important;
            max-width: 1240px !important;
        }

        /* BASE STREAMLIT APP OVERRIDES */
        .stApp {
            background-color: var(--ink) !important;
            color: #ffffff !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* AMBIENT GLOW BLOBS */
        .ambient-blob-1 {
            position: fixed;
            width: 450px;
            height: 450px;
            background: radial-gradient(circle, rgba(156, 140, 255, 0.16) 0%, rgba(20, 19, 43, 0) 70%);
            top: -80px;
            left: -80px;
            z-index: 0;
            pointer-events: none;
            filter: blur(50px);
            animation: drift 18s ease-in-out infinite alternate;
        }
        .ambient-blob-2 {
            position: fixed;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(255, 107, 84, 0.12) 0%, rgba(20, 19, 43, 0) 70%);
            bottom: -100px;
            right: -80px;
            z-index: 0;
            pointer-events: none;
            filter: blur(60px);
            animation: drift 22s ease-in-out infinite alternate-reverse;
        }

        @keyframes drift {
            0% { transform: translate(0, 0) scale(1); }
            100% { transform: translate(40px, 40px) scale(1.08); }
        }

        /* HEADINGS & TYPOGRAPHY */
        h1, h2, h3, .heading-display {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
            color: #ffffff !important;
        }
        
        .eyebrow-caveat {
            font-family: 'Caveat', cursive !important;
            font-size: 1.5rem !important;
            color: var(--highlighter) !important;
            display: inline-block;
            transform: rotate(-2deg);
            margin-bottom: 6px;
        }

        .mono-label {
            font-family: 'Space Mono', monospace !important;
            font-size: 0.85rem !important;
            color: var(--text-soft) !important;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        /* SCROLLBAR */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(246, 241, 227, 0.18); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--highlighter); }

        /* SLEEK TOP NAVBAR STYLING */
        div[data-testid="stHorizontalBlock"]:has(.navbar-anchor) {
            background: rgba(28, 26, 66, 0.9) !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid rgba(246, 241, 227, 0.16) !important;
            border-radius: 20px !important;
            padding: 10px 18px !important;
            margin-bottom: 28px !important;
            align-items: center !important;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45) !important;
        }

        /* TOP NAVBAR BUTTONS */
        .nav-link-btn button {
            background: transparent !important;
            color: var(--text-soft) !important;
            border: 1px solid transparent !important;
            box-shadow: none !important;
            padding: 8px 14px !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
            height: 40px !important;
            white-space: nowrap !important;
        }
        .nav-link-btn button:hover {
            background: rgba(246, 241, 227, 0.08) !important;
            color: #ffffff !important;
            border-color: rgba(246, 241, 227, 0.15) !important;
        }
        .nav-link-active button {
            background: rgba(228, 255, 91, 0.16) !important;
            color: var(--highlighter) !important;
            border: 1px solid var(--highlighter) !important;
            box-shadow: 0 0 16px rgba(228, 255, 91, 0.3) !important;
            padding: 8px 14px !important;
            font-size: 0.88rem !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            height: 40px !important;
            white-space: nowrap !important;
        }

        /* CTA BUTTON IN NAVBAR */
        .nav-cta-btn button {
            background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important;
            color: #ffffff !important;
            border: none !important;
            padding: 8px 16px !important;
            font-size: 0.9rem !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            height: 40px !important;
            box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4) !important;
            white-space: nowrap !important;
        }
        .nav-cta-btn button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(255, 75, 43, 0.65) !important;
        }

        /* CARDS & PANELS */
        .panel-card {
            background: var(--ink2);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            padding: 28px;
            position: relative;
            transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .panel-card:hover {
            border-color: var(--highlighter);
            transform: translateY(-4px);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
        }

        .paper-card {
            background: var(--paper);
            color: #14132B !important;
            border-radius: var(--radius);
            padding: 26px;
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.35);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .paper-card h3, .paper-card h4, .paper-card strong {
            color: #14132B !important;
        }
        .paper-card p, .paper-card li {
            color: #2D2A4A !important;
            line-height: 1.6;
        }

        /* PILL BADGE */
        .tag-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(228, 255, 91, 0.12);
            border: 1px solid var(--highlighter);
            color: var(--highlighter);
            padding: 6px 14px;
            border-radius: 20px;
            font-family: 'Space Mono', monospace;
            font-size: 0.82rem;
            font-weight: 700;
        }

        /* STREAMLIT BUTTON OVERRIDES */
        .stButton>button {
            background: var(--coral) !important;
            color: #ffffff !important;
            border: none !important;
            padding: 10px 18px !important;
            border-radius: 12px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 15px rgba(255, 107, 84, 0.3) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 22px rgba(255, 107, 84, 0.55) !important;
        }
        .stButton>button:focus {
            outline: 2px solid var(--highlighter) !important;
        }

        /* MARQUEE STRIP */
        .marquee-container {
            overflow: hidden;
            white-space: nowrap;
            background: var(--ink3);
            border-top: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
            padding: 14px 0;
            position: relative;
        }
        .marquee-content {
            display: inline-block;
            animation: marquee 25s linear infinite;
            font-family: 'Space Mono', monospace;
            font-size: 0.9rem;
            color: var(--highlighter);
        }
        @keyframes marquee {
            0% { transform: translateX(0%); }
            100% { transform: translateX(-50%); }
        }

        /* FANNED 7-CARD HERO DECK */
        .hero-deck {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 260px;
            position: relative;
            margin: 30px auto;
            max-width: 750px;
        }
        .deck-card {
            width: 140px;
            height: 190px;
            background: var(--paper);
            color: #14132B;
            border-radius: 16px;
            padding: 16px 12px;
            position: absolute;
            box-shadow: 0 12px 28px rgba(0,0,0,0.45);
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            text-align: center;
            border: 1px solid rgba(0,0,0,0.08);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        .deck-card:hover {
            transform: translateY(-24px) scale(1.1) !important;
            z-index: 50 !important;
            box-shadow: 0 20px 45px rgba(228, 255, 91, 0.4);
            border-color: var(--coral);
        }
        .deck-card-1 { transform: translateX(-210px) rotate(-18deg); z-index: 1; }
        .deck-card-2 { transform: translateX(-140px) rotate(-12deg); z-index: 2; }
        .deck-card-3 { transform: translateX(-70px) rotate(-6deg); z-index: 3; }
        .deck-card-4 { transform: translateX(0px) rotate(0deg); z-index: 4; }
        .deck-card-5 { transform: translateX(70px) rotate(6deg); z-index: 5; }
        .deck-card-6 { transform: translateX(140px) rotate(12deg); z-index: 6; }
        .deck-card-7 { transform: translateX(210px) rotate(18deg); z-index: 7; }

        /* FLIP CARDS FOR FEATURES */
        .flip-card-container {
            perspective: 1000px;
            height: 220px;
            margin-bottom: 20px;
        }
        .flip-card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1);
            transform-style: preserve-3d;
            border-radius: var(--radius);
        }
        .flip-card-container:hover .flip-card-inner {
            transform: rotateY(180deg);
        }
        .flip-card-front, .flip-card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            -webkit-backface-visibility: hidden;
            backface-visibility: hidden;
            border-radius: var(--radius);
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 1px solid var(--line);
        }
        .flip-card-front {
            background: var(--ink2);
            color: #ffffff;
        }
        .flip-card-back {
            background: var(--ink3);
            color: var(--highlighter);
            transform: rotateY(180deg);
            border-color: var(--highlighter);
        }
    </style>

    <!-- AMBIENT BLOBS -->
    <div class="ambient-blob-1"></div>
    <div class="ambient-blob-2"></div>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    # --- RENDER TOP NAVBAR ---
    with st.container():
        col_logo, col_h, col_hw, col_f, col_p, col_s, col_g, col_cta = st.columns(
            [2.2, 1, 1.3, 1.1, 1, 1, 1.3, 1.4], gap="small"
        )
        
        with col_logo:
            st.markdown("""
            <div class="navbar-anchor" style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 1.3rem; color: #fff; padding-top: 7px; display: flex; align-items: center; gap: 6px;">
                ⚡ <span style="background: linear-gradient(90deg, #ffffff, #E4FF5B); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">StudentFit AI</span>
            </div>
            """, unsafe_allow_html=True)

        with col_h:
            st.markdown(f'<div class="{"nav-link-active" if active_page == "Home" else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("🏠 Home", key="nav_btn_home", use_container_width=True):
                st.switch_page("pages/home.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_hw:
            st.markdown(f'<div class="{"nav-link-active" if active_page == "How it Works" else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("📖 How it Works", key="nav_btn_how", use_container_width=True):
                st.switch_page("pages/how_it_works.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_f:
            st.markdown(f'<div class="{"nav-link-active" if active_page == "Features" else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("✨ Features", key="nav_btn_feat", use_container_width=True):
                st.switch_page("pages/features.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_p:
            st.markdown(f'<div class="{"nav-link-active" if active_page == "Plans" else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("🏷️ Plans", key="nav_btn_plans", use_container_width=True):
                st.switch_page("pages/plans.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_s:
            st.markdown(f'<div class="{"nav-link-active" if active_page == "Story" else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("💡 Story", key="nav_btn_story", use_container_width=True):
                st.switch_page("pages/story.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_g:
            st.markdown(f'<div class="{"nav-link-active" if active_page == "AI Generator" else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("⚡ Generator", key="nav_btn_gen", use_container_width=True):
                st.switch_page("pages/generator.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_cta:
            st.markdown('<div class="nav-cta-btn">', unsafe_allow_html=True)
            if st.button("🚀 Plan Week", key="nav_btn_cta", use_container_width=True):
                st.switch_page("pages/generator.py")
            st.markdown('</div>', unsafe_allow_html=True)

    # 3D Tilt JS
    js_code = """
    <script>
    (function() {
        const doc = window.parent.document;
        doc.querySelectorAll('.tilt').forEach(el => {
            el.addEventListener('mousemove', e => {
                const rect = el.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                el.style.transform = `perspective(900px) rotateX(${-y / 15}deg) rotateY(${x / 15}deg) scale3d(1.02, 1.02, 1.02)`;
            });
            el.addEventListener('mouseleave', () => {
                el.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
            });
        });
    })();
    </script>
    """
    components.html(js_code, height=0, width=0)
