"""
Theme Module for StudentFit AI.
Defines design tokens, typography, custom CSS, ambient animations, exact matching top navigation bar, and shared JS.
"""

import streamlit as st
import streamlit.components.v1 as components

def apply_theme(active_page: str = "Home & Features"):
    """Injects design system styles and renders the top navigation bar matching the design screenshot."""
    css = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --ink: #0d0a20;
            --ink2: #17133d;
            --ink3: #221d52;
            --paper: #F6F1E3;
            --highlighter: #E4FF5B;
            --neon-cyan: #00e5ff;
            --coral: #FF6B54;
            --pink-gradient: linear-gradient(90deg, #ff416c, #ff4b2b);
            --lilac: #9C8CFF;
            --text-soft: #B7B3DA;
            --text-faint: #8582AC;
            --line: rgba(255, 255, 255, 0.12);
            --radius: 20px;
        }

        /* HIDE DEFAULT STREAMLIT SIDEBAR & COLLAPSE CONTROL */
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        .stMainBlockContainer {
            padding-top: 0px !important;
            max-width: 1240px !important;
        }

        /* BASE STREAMLIT APP OVERRIDES */
        .stApp {
            background: linear-gradient(135deg, #09071c 0%, #17133d 50%, #15112e 100%) !important;
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
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 800 !important;
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
        ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.18); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

        /* EXACT TOP NAVBAR STYLING MATCHING USER SCREENSHOT */
        .top-navbar-wrapper {
            background: rgba(13, 10, 32, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 28px;
            margin-bottom: 30px;
            border-radius: 0 0 16px 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }

        /* CARDS & PANELS */
        .panel-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(14px);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            padding: 28px;
            position: relative;
            transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .panel-card:hover {
            border-color: rgba(0, 229, 255, 0.6);
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
            background: rgba(0, 229, 255, 0.12);
            border: 1px solid rgba(0, 229, 255, 0.4);
            color: var(--neon-cyan);
            padding: 6px 16px;
            border-radius: 24px;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        /* STREAMLIT BUTTON OVERRIDES */
        .stButton>button {
            background: var(--pink-gradient) !important;
            color: #ffffff !important;
            border: none !important;
            padding: 10px 22px !important;
            border-radius: 24px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 18px rgba(255, 65, 108, 0.4) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(255, 65, 108, 0.7) !important;
        }

        /* NAVBAR LINK BUTTONS */
        .nav-link-btn>button {
            background: transparent !important;
            color: var(--text-soft) !important;
            border: none !important;
            box-shadow: none !important;
            padding: 8px 16px !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        .nav-link-btn>button:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            color: #ffffff !important;
            transform: none !important;
            box-shadow: none !important;
        }
        .nav-link-btn-active>button {
            background: rgba(255, 255, 255, 0.08) !important;
            color: var(--neon-cyan) !important;
            border: none !important;
            border-bottom: 2px solid var(--neon-cyan) !important;
            border-radius: 8px 8px 0 0 !important;
            box-shadow: none !important;
            padding: 8px 16px !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            transform: none !important;
        }

        /* MARQUEE STRIP */
        .marquee-container {
            overflow: hidden;
            white-space: nowrap;
            background: rgba(255, 255, 255, 0.03);
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
            color: var(--neon-cyan);
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
            box-shadow: 0 20px 45px rgba(0, 229, 255, 0.4);
            border-color: var(--neon-cyan);
        }
        .deck-card-1 { transform: translateX(-210px) rotate(-18deg); z-index: 1; }
        .deck-card-2 { transform: translateX(-140px) rotate(-12deg); z-index: 2; }
        .deck-card-3 { transform: translateX(-70px) rotate(-6deg); z-index: 3; }
        .deck-card-4 { transform: translateX(0px) rotate(0deg); z-index: 4; }
        .deck-card-5 { transform: translateX(70px) rotate(6deg); z-index: 5; }
        .deck-card-6 { transform: translateX(140px) rotate(12deg); z-index: 6; }
        .deck-card-7 { transform: translateX(210px) rotate(18deg); z-index: 7; }
    </style>

    <!-- AMBIENT BLOBS -->
    <div class="ambient-blob-1"></div>
    <div class="ambient-blob-2"></div>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    # --- RENDER TOP NAVBAR MATCHING EXACT SCREENSHOT ---
    with st.container():
        st.markdown('<div class="top-navbar-wrapper">', unsafe_allow_html=True)
        col_logo, col_h, col_g, col_m, col_cta = st.columns([2.2, 1.3, 1.3, 1.3, 1.4], gap="medium")
        
        with col_logo:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; font-weight: 800; font-size: 1.4rem; color: #fff; padding-top: 4px; cursor: pointer;">
                <span style="color: #ff6b54; font-size: 1.5rem;">⚡</span>
                <span style="background: linear-gradient(90deg, #ffffff, #00e5ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">StudentFit AI</span>
            </div>
            """, unsafe_allow_html=True)

        with col_h:
            is_active = (active_page == "Home & Features")
            st.markdown(f'<div class="{"nav-link-btn-active" if is_active else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("🏠 Home & Features", key="top_nav_home", use_container_width=True):
                st.switch_page("pages/home.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_g:
            is_active = (active_page == "AI Planner Studio")
            st.markdown(f'<div class="{"nav-link-btn-active" if is_active else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("⚡ AI Planner Studio", key="top_nav_studio", use_container_width=True):
                st.switch_page("pages/generator.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_m:
            is_active = (active_page == "Student Macro Hub")
            st.markdown(f'<div class="{"nav-link-btn-active" if is_active else "nav-link-btn"}">', unsafe_allow_html=True)
            if st.button("📊 Student Macro Hub", key="top_nav_macros", use_container_width=True):
                st.switch_page("pages/macros.py")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_cta:
            if st.button("🚀 Launch AI Studio", key="top_nav_cta", use_container_width=True):
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
