"""
StudentFit AI — Shared Design System & Theme
Injects CSS custom properties, Google Fonts, base typography, and vanilla JS on every page.
"""

import streamlit as st
import streamlit.components.v1 as components

SHARED_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Space+Grotesk:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

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
        --line: rgba(246, 241, 227, 0.14);
        --radius: 20px;
    }

    /* GLOBAL STREAMLIT OVERRIDES */
    .stApp {
        background-color: var(--ink) !important;
        color: var(--paper) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        overflow-x: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--ink2) !important;
        border-right: 1px solid var(--line) !important;
    }

    /* TOP PLANNER TAB NAVIGATION */
    [data-testid="stSidebarNav"] {
        padding-top: 10px;
    }
    
    [data-testid="stSidebarNav"] ul {
        gap: 6px;
    }

    [data-testid="stSidebarNav"] a {
        border-radius: 12px !important;
        padding: 8px 14px !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 0.88rem !important;
        color: var(--text-soft) !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: rgba(246, 241, 227, 0.06) !important;
        color: var(--paper) !important;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: rgba(228, 255, 91, 0.12) !important;
        color: var(--highlighter) !important;
        border-color: rgba(228, 255, 91, 0.35) !important;
        font-weight: 700 !important;
    }

    /* ULTRA-THIN TRANSPARENT SCROLLBAR */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(246, 241, 227, 0.2); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--highlighter); }

    /* TYPOGRAPHY SYSTEM */
    h1, h2, h3, h4, h5, h6, .display-head {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        color: var(--paper) !important;
    }

    .eyebrow {
        font-family: 'Caveat', cursive !important;
        font-size: 1.55rem !important;
        color: var(--highlighter) !important;
        letter-spacing: 0.5px !important;
        display: inline-block;
        transform: rotate(-2deg);
        margin-bottom: 8px;
    }

    .mono-stat {
        font-family: 'Space Mono', monospace !important;
        font-size: 0.85rem !important;
        color: var(--text-soft) !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase;
    }

    /* AMBIENT BACKGROUND BLOBS */
    .ambient-bg {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }

    .blob-1 {
        position: absolute;
        width: 500px;
        height: 500px;
        top: -150px;
        right: -100px;
        background: radial-gradient(circle, rgba(156, 140, 255, 0.16) 0%, transparent 70%);
        filter: blur(80px);
        animation: floatBlob 18s ease-in-out infinite alternate;
    }

    .blob-2 {
        position: absolute;
        width: 450px;
        height: 450px;
        bottom: 10%;
        left: -150px;
        background: radial-gradient(circle, rgba(255, 107, 84, 0.12) 0%, transparent 70%);
        filter: blur(80px);
        animation: floatBlob 14s ease-in-out infinite alternate-reverse;
    }

    @keyframes floatBlob {
        0% { transform: translate(0, 0) scale(1); }
        100% { transform: translate(40px, 60px) scale(1.1); }
    }

    /* CARD STYLES */
    .card-dark {
        background: var(--ink2);
        border: 1px solid var(--line);
        border-radius: var(--radius);
        padding: 26px;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
    }

    .card-dark:hover {
        border-color: rgba(228, 255, 91, 0.4);
        transform: translateY(-4px);
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
    }

    .card-paper {
        background: var(--paper) !important;
        color: #14132B !important;
        border-radius: var(--radius);
        padding: 24px;
        border: 1px solid rgba(0, 0, 0, 0.08);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
        transition: all 0.3s ease;
    }

    .card-paper h3, .card-paper h4, .card-paper strong {
        color: #14132B !important;
    }

    .card-paper:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
    }

    /* HERO FANNED DECK OF 7 CARDS */
    .hero-deck-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 280px;
        position: relative;
        perspective: 1000px;
        margin: 25px 0 45px 0;
    }

    .deck-card {
        position: absolute;
        width: 140px;
        height: 190px;
        background: var(--paper);
        color: var(--ink);
        border-radius: 16px;
        padding: 16px 12px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s;
        cursor: pointer;
    }

    .deck-card:hover {
        transform: translateY(-24px) scale(1.08) !important;
        box-shadow: 0 20px 45px rgba(228, 255, 91, 0.35);
        z-index: 100 !important;
        border-color: var(--coral);
    }

    .deck-day { font-family: 'Space Mono', monospace; font-size: 0.75rem; font-weight: 700; color: var(--coral); text-transform: uppercase; }
    .deck-emoji { font-size: 2.2rem; text-align: center; }
    .deck-tag { font-size: 0.78rem; font-weight: 700; color: var(--ink); text-align: center; line-height: 1.2; }

    /* TICKER MARQUEE */
    .marquee-container {
        overflow: hidden;
        white-space: nowrap;
        background: var(--ink3);
        border-top: 1px solid var(--line);
        border-bottom: 1px solid var(--line);
        padding: 12px 0;
        margin: 40px 0;
    }

    .marquee-track {
        display: inline-block;
        animation: marqueeScroll 28s linear infinite;
    }

    .marquee-item {
        display: inline-block;
        font-family: 'Space Mono', monospace;
        font-size: 0.88rem;
        font-weight: 700;
        color: var(--paper);
        margin: 0 24px;
    }

    .marquee-item span {
        color: var(--highlighter);
        margin-right: 8px;
    }

    @keyframes marqueeScroll {
        from { transform: translateX(0); }
        to { transform: translateX(-50%); }
    }

    /* 3D FLIP CARDS */
    .flip-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        margin: 30px 0;
    }

    .flip-card {
        background-color: transparent;
        height: 220px;
        perspective: 1000px;
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

    .flip-card:hover .flip-card-inner {
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
    }

    .flip-card-front {
        background: var(--ink2);
        border: 1px solid var(--line);
        color: var(--paper);
    }

    .flip-card-back {
        background: var(--paper);
        color: var(--ink);
        transform: rotateY(180deg);
        border: 1px solid var(--highlighter);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    }

    .flip-card-back p {
        color: #14132B !important;
        font-size: 0.95rem;
        font-weight: 600;
        line-height: 1.5;
    }

    /* BUTTONS */
    .stButton>button {
        background: var(--coral) !important;
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px 24px !important;
        transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 4px 18px rgba(255, 107, 84, 0.35) !important;
    }

    .stButton>button:hover {
        background: #ff5238 !important;
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 24px rgba(255, 107, 84, 0.6) !important;
    }

    /* FORM INPUTS */
    input, select, textarea, [data-baseweb="select"] {
        border-radius: 10px !important;
    }

    /* ACCESSIBILITY & PREFERS REDUCED MOTION */
    @media (prefers-reduced-motion: reduce) {
        *, .deck-card, .flip-card-inner, .marquee-track, .blob-1, .blob-2 {
            animation: none !important;
            transition: none !important;
            transform: none !important;
        }
    }

    :focus-visible {
        outline: 2px solid var(--highlighter) !important;
        outline-offset: 2px !important;
    }
</style>

<div class="ambient-bg">
    <div class="blob-1"></div>
    <div class="blob-2"></div>
</div>
"""

SHARED_JS = """
<script>
    (function() {
        const doc = window.parent ? window.parent.document : document;
        
        // 3D Mouse Tilt on elements with class 'tilt'
        doc.addEventListener('mousemove', function(e) {
            const tiltElements = doc.querySelectorAll('.tilt');
            tiltElements.forEach(el => {
                const rect = el.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                if (x >= 0 && x <= rect.width && y >= 0 && y <= rect.height) {
                    const xPct = (x / rect.width - 0.5) * 16;
                    const yPct = (y / rect.height - 0.5) * -16;
                    el.style.transform = `perspective(900px) rotateX(${yPct}deg) rotateY(${xPct}deg) translateY(-4px)`;
                }
            });
        });

        doc.addEventListener('mouseleave', function() {
            const tiltElements = doc.querySelectorAll('.tilt');
            tiltElements.forEach(el => {
                el.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg)';
            });
        });
    })();
</script>
"""

def apply_theme():
    """Injects the shared StudentFit design system on any Streamlit page."""
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    # Inject interactive JS via invisible component
    components.html(SHARED_JS, height=0, width=0)
