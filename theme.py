"""
Theme Module for StudentFit AI.
Defines design tokens, typography, custom CSS, ambient animations, and shared JS.
"""

import streamlit as st
import streamlit.components.v1 as components

def apply_theme():
    """Injects the cohesive design system and styles into the Streamlit page."""
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

        /* BASE STREAMLIT APP OVERRIDES */
        .stApp {
            background-color: var(--ink) !important;
            color: #ffffff !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* 3D AMBIENT DEPTH LAYERS */
        .bg-grid-3d {
            position: fixed;
            width: 200vw;
            height: 100vh;
            bottom: -30vh;
            left: -50vw;
            background: 
                linear-gradient(to top, rgba(20, 19, 43, 0) 0%, var(--ink) 85%),
                linear-gradient(rgba(156, 140, 255, 0.12) 1px, transparent 1px),
                linear-gradient(90deg, rgba(156, 140, 255, 0.12) 1px, transparent 1px);
            background-size: 100% 100%, 60px 60px, 60px 60px;
            transform: perspective(450px) rotateX(65deg);
            transform-origin: center bottom;
            z-index: 0;
            pointer-events: none;
            opacity: 0.7;
            animation: gridMove 20s linear infinite;
        }
        @keyframes gridMove {
            0% { background-position: 0 0, 0 0, 0 0; }
            100% { background-position: 0 0, 0 60px, 0 0; }
        }

        .ambient-blob-1 {
            position: fixed;
            width: 550px;
            height: 550px;
            background: radial-gradient(circle, rgba(156, 140, 255, 0.2) 0%, rgba(20, 19, 43, 0) 70%);
            top: -100px;
            left: -100px;
            z-index: 0;
            pointer-events: none;
            filter: blur(60px);
            animation: drift3D 18s ease-in-out infinite alternate;
        }
        .ambient-blob-2 {
            position: fixed;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(255, 107, 84, 0.16) 0%, rgba(20, 19, 43, 0) 70%);
            bottom: -120px;
            right: -100px;
            z-index: 0;
            pointer-events: none;
            filter: blur(70px);
            animation: drift3D 22s ease-in-out infinite alternate-reverse;
        }
        .ambient-blob-3 {
            position: fixed;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(228, 255, 91, 0.1) 0%, rgba(20, 19, 43, 0) 70%);
            top: 40%;
            left: 45%;
            z-index: 0;
            pointer-events: none;
            filter: blur(80px);
            animation: drift3D 25s ease-in-out infinite alternate;
        }

        @keyframes drift3D {
            0% { transform: translate3d(0, 0, 0) scale(1); }
            50% { transform: translate3d(50px, -40px, 30px) scale(1.1); }
            100% { transform: translate3d(-30px, 50px, -20px) scale(0.95); }
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
            padding: 12px 24px !important;
            border-radius: 14px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 6px 20px rgba(255, 107, 84, 0.35) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 10px 28px rgba(255, 107, 84, 0.6) !important;
        }
        .stButton>button:focus {
            outline: 2px solid var(--highlighter) !important;
        }

        /* STREAMLIT SIDEBAR */
        [data-testid="stSidebar"] {
            background-color: var(--ink2) !important;
            border-right: 1px solid var(--line) !important;
        }

        /* STREAMLIT NAVIGATION PILL BAR */
        [data-testid="stSidebarNav"] {
            background: transparent !important;
            padding-top: 10px !important;
        }
        [data-testid="stSidebarNav"] a {
            border-radius: 12px !important;
            color: var(--text-soft) !important;
            font-weight: 600 !important;
            margin-bottom: 4px !important;
            transition: all 0.2s ease !important;
        }
        [data-testid="stSidebarNav"] a:hover {
            background: rgba(246, 241, 227, 0.08) !important;
            color: #ffffff !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: rgba(228, 255, 91, 0.15) !important;
            color: var(--highlighter) !important;
            border-left: 3px solid var(--highlighter) !important;
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
            transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.3s ease, border-color 0.3s ease;
            text-align: center;
            border: 1px solid rgba(0,0,0,0.08);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            will-change: transform;
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
        }
        .deck-card-1 { transform: translateX(-210px) rotate(-18deg); z-index: 1; }
        .deck-card-2 { transform: translateX(-140px) rotate(-12deg); z-index: 2; }
        .deck-card-3 { transform: translateX(-70px) rotate(-6deg); z-index: 3; }
        .deck-card-4 { transform: translateX(0px) rotate(0deg); z-index: 4; border: 2px solid var(--coral); }
        .deck-card-5 { transform: translateX(70px) rotate(6deg); z-index: 5; }
        .deck-card-6 { transform: translateX(140px) rotate(12deg); z-index: 6; }
        .deck-card-7 { transform: translateX(210px) rotate(18deg); z-index: 7; }

        .deck-card:hover {
            z-index: 50 !important;
            box-shadow: 0 22px 48px rgba(228, 255, 91, 0.5);
            border-color: var(--coral) !important;
        }

        .deck-card-1:hover { transform: translateX(-210px) translateY(-26px) rotate(-18deg) scale(1.08) !important; }
        .deck-card-2:hover { transform: translateX(-140px) translateY(-26px) rotate(-12deg) scale(1.08) !important; }
        .deck-card-3:hover { transform: translateX(-70px) translateY(-26px) rotate(-6deg) scale(1.08) !important; }
        .deck-card-4:hover { transform: translateX(0px) translateY(-26px) rotate(0deg) scale(1.08) !important; }
        .deck-card-5:hover { transform: translateX(70px) translateY(-26px) rotate(6deg) scale(1.08) !important; }
        .deck-card-6:hover { transform: translateX(140px) translateY(-26px) rotate(12deg) scale(1.08) !important; }
        .deck-card-7:hover { transform: translateX(210px) translateY(-26px) rotate(18deg) scale(1.08) !important; }

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

        /* COMPREHENSIVE RESPONSIVE STYLING */
        @media (max-width: 860px) {
            .hero-deck {
                transform: scale(0.72);
                transform-origin: center center;
                height: 190px;
                margin: 0 auto;
                max-width: 100%;
            }
        }

        @media (max-width: 600px) {
            h1 { font-size: 2.2rem !important; }
            h2 { font-size: 1.7rem !important; }
            .hero-deck {
                transform: scale(0.54);
                height: 150px;
            }
            .panel-card, .paper-card {
                padding: 18px 14px !important;
                border-radius: 16px !important;
            }
        }

        @media (max-width: 380px) {
            h1 { font-size: 1.85rem !important; }
            .hero-deck {
                transform: scale(0.44);
                height: 125px;
            }
        }

        /* REDUCED MOTION */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>

    <!-- 3D AMBIENT BACKGROUND ELEMENTS -->
    <div class="bg-grid-3d"></div>
    <div class="ambient-blob-1"></div>
    <div class="ambient-blob-2"></div>
    <div class="ambient-blob-3"></div>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    # Injected helper for 3D tilt
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
