import os
import sys
from flask import Flask, render_template_string, request, jsonify

# Ensure local directory is in Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (
    get_api_key,
    calculate_macros,
    parse_ai_response,
    generate_plan_mock,
    generate_plan_real,
    create_fitness_pdf,
    CANDIDATE_MODELS
)

app = Flask(__name__)

# --- COMPLETE COHESIVE 6-PAGE STUDENTFIT AI WEB EXPERIENCE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudentFit AI ⚡ | Fitness that Syncs to Your Syllabus</title>
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><defs><linearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'><stop offset='0%25' stop-color='%23FF6B54'/><stop offset='100%25' stop-color='%23E4FF5B'/></linearGradient></defs><circle cx='50' cy='50' r='46' fill='%2314132B' stroke='url(%23grad)' stroke-width='6'/><path d='M54 18 L32 52 L48 52 L44 82 L72 44 L54 44 Z' fill='url(%23grad)'/></svg>">
    <link rel="alternate icon" type="image/png" href="https://img.icons8.com/fluency/48/lightning-bolt.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
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

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
            scrollbar-width: thin;
            scrollbar-color: rgba(246, 241, 227, 0.2) transparent;
        }

        body {
            background: var(--ink);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* SCROLLBAR */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(246, 241, 227, 0.18); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--highlighter); }

        /* 3D AMBIENT DEPTH LAYERS */
        #bg-3d-canvas {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 0;
            pointer-events: none;
            opacity: 0.65;
        }

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

        /* TYPOGRAPHY */
        h1, h2, h3, .heading-display {
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #ffffff;
        }

        .eyebrow-caveat {
            font-family: 'Caveat', cursive;
            font-size: 1.5rem;
            color: var(--highlighter);
            display: inline-block;
            transform: rotate(-2deg);
            margin-bottom: 6px;
        }

        .mono-label {
            font-family: 'Space Mono', monospace;
            font-size: 0.82rem;
            color: var(--text-soft);
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }

        /* TOP NAVIGATION BAR */
        .navbar {
            background: rgba(20, 19, 43, 0.92);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--line);
            padding: 12px 24px;
            position: sticky;
            top: 0;
            z-index: 1000;
            width: 100%;
        }

        .navbar-inner {
            max-width: 1180px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
        }

        .brand-logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.45rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            color: #fff;
            cursor: pointer;
        }

        .brand-logo span { color: var(--highlighter); }

        .nav-links {
            display: flex;
            gap: 12px;
            align-items: center;
            list-style: none;
        }

        .nav-link {
            color: var(--text-soft);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.92rem;
            transition: all 0.2s ease;
            cursor: pointer;
            padding: 8px 14px;
            border-radius: 12px;
        }

        .nav-link:hover {
            color: #ffffff;
            background: rgba(246, 241, 227, 0.08);
        }

        .nav-link.active {
            color: var(--highlighter);
            background: rgba(228, 255, 91, 0.12);
            border: 1px solid var(--highlighter);
        }

        .nav-cta {
            background: var(--coral);
            color: #fff;
            border: none;
            padding: 10px 22px;
            border-radius: 14px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 0.92rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 16px rgba(255, 107, 84, 0.35);
        }

        .nav-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 22px rgba(255, 107, 84, 0.6);
        }

        /* PAGE VIEWS */
        .page-view {
            display: none;
            flex: 1;
            width: 100%;
            position: relative;
            z-index: 1;
            animation: fadeIn 0.3s ease forwards;
        }

        .page-view.active-page { display: block; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* PANELS & CARDS */
        .panel-card {
            background: var(--ink2);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            padding: 28px;
            transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .panel-card:hover {
            border-color: var(--highlighter);
            transform: translateY(-4px);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
        }

        /* SCHEDULE & GROCERY LIST CARDS (HIGH CONTRAST VIBRANT COLORS) */
        .schedule-card {
            background: var(--ink2);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            padding: 24px;
            margin-bottom: 24px;
            transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .schedule-card:hover {
            border-color: var(--highlighter);
            transform: translateY(-3px);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
        }
        .schedule-card h3 {
            color: var(--highlighter) !important;
            font-size: 1.35rem;
            margin: 0;
        }

        .grocery-panel {
            background: var(--ink2);
            border: 1px solid var(--coral);
            border-radius: var(--radius);
            padding: 26px 22px;
            height: fit-content;
            position: sticky;
            top: 90px;
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
        }
        .grocery-panel h4 {
            color: var(--highlighter) !important;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            border-bottom: 1px solid var(--line);
            padding-bottom: 8px;
            margin-top: 20px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .grocery-panel h4:first-child { margin-top: 0; }
        .grocery-panel ul {
            list-style: none !important;
            padding-left: 0 !important;
            margin-bottom: 16px;
        }
        .grocery-panel li {
            margin-bottom: 12px;
            font-size: 0.95rem;
            color: #FFFFFF !important;
            line-height: 1.6;
            display: flex;
            align-items: flex-start;
            gap: 10px;
        }
        .grocery-panel li::before {
            content: "•";
            color: var(--coral) !important;
            font-size: 1.4rem;
            line-height: 1;
            font-weight: 800;
        }
        .grocery-panel strong {
            color: var(--highlighter) !important;
            font-weight: 700;
        }
        .grocery-panel p {
            color: var(--text-soft) !important;
            font-size: 0.92rem;
            line-height: 1.6;
            margin-bottom: 12px;
        }

        .workout-routine-box {
            background: rgba(20, 19, 43, 0.7);
            border: 1px solid rgba(255, 107, 84, 0.3);
            border-radius: 14px;
            padding: 16px;
        }
        .workout-routine-box ul { list-style: none !important; padding-left: 0 !important; }
        .workout-routine-box li {
            margin-bottom: 10px;
            font-size: 0.92rem;
            color: #FFFFFF !important;
            line-height: 1.6;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }
        .workout-routine-box li::before {
            content: "▸";
            color: var(--coral) !important;
            font-weight: bold;
            font-size: 1.1rem;
        }
        .workout-routine-box strong { color: var(--coral) !important; }

        .meal-routine-box {
            background: rgba(20, 19, 43, 0.7);
            border: 1px solid rgba(228, 255, 91, 0.3);
            border-radius: 14px;
            padding: 16px;
        }
        .meal-routine-box ul { list-style: none !important; padding-left: 0 !important; }
        .meal-routine-box li {
            margin-bottom: 10px;
            font-size: 0.92rem;
            color: #FFFFFF !important;
            line-height: 1.6;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }
        .meal-routine-box li::before {
            content: "▸";
            color: var(--highlighter) !important;
            font-weight: bold;
            font-size: 1.1rem;
        }
        .meal-routine-box strong { color: var(--highlighter) !important; }

        .paper-card {
            background: var(--paper);
            color: #14132B !important;
            border-radius: var(--radius);
            padding: 26px;
            box-shadow: 0 14px 34px rgba(0, 0, 0, 0.35);
        }
        .paper-card h3, .paper-card h4, .paper-card strong { color: #14132B !important; }
        .paper-card p, .paper-card li { color: #2D2A4A !important; line-height: 1.6; }

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

        .btn-primary-lg {
            background: var(--coral);
            color: white;
            padding: 16px 34px;
            border-radius: 14px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 6px 25px rgba(255, 107, 84, 0.4);
        }
        .btn-primary-lg:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 30px rgba(255, 107, 84, 0.7);
        }

        .btn-secondary-lg {
            background: rgba(246, 241, 227, 0.08);
            color: white;
            padding: 16px 30px;
            border-radius: 14px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.05rem;
            font-weight: 700;
            border: 1px solid var(--line);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .btn-secondary-lg:hover {
            background: rgba(246, 241, 227, 0.15);
            border-color: var(--highlighter);
            transform: translateY(-3px);
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

        /* MARQUEE */
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
            animation: marquee 28s linear infinite;
            font-family: 'Space Mono', monospace;
            font-size: 0.9rem;
            color: var(--highlighter);
        }
        @keyframes marquee {
            0% { transform: translateX(0%); }
            100% { transform: translateX(-50%); }
        }

        /* FLIP CARDS */
        .flip-card-container { perspective: 1000px; height: 220px; margin-bottom: 20px; cursor: pointer; }
        .flip-card-inner { position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1); transform-style: preserve-3d; border-radius: var(--radius); }
        .flip-card-container:hover .flip-card-inner, .flip-card-container.flipped .flip-card-inner { transform: rotateY(180deg); }
        .flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; -webkit-backface-visibility: hidden; backface-visibility: hidden; border-radius: var(--radius); padding: 24px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: 1px solid var(--line); }
        .flip-card-front { background: var(--ink2); color: #ffffff; }
        .flip-card-back { background: var(--ink3); color: var(--highlighter); transform: rotateY(180deg); border-color: var(--highlighter); }

        /* STUDIO LAYOUT & SIDEBAR */
        .studio-container { display: flex; width: 100%; flex: 1; }
        .studio-sidebar { width: 360px; background: var(--ink2); border-right: 1px solid var(--line); padding: 26px 22px; overflow-y: auto; max-height: calc(100vh - 72px); position: sticky; top: 72px; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .studio-sidebar.sidebar-closed { display: none !important; }
        .form-group { margin-bottom: 13px; }
        .form-row { display: flex; gap: 10px; }
        .form-row .form-group { flex: 1; }
        label { display: block; font-size: 0.82rem; color: var(--text-soft); margin-bottom: 4px; font-weight: 600; font-family: 'Space Mono', monospace; }
        input, select { width: 100%; background: rgba(246, 241, 227, 0.08); border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; color: #fff; font-size: 0.9rem; outline: none; transition: all 0.2s; }
        input:focus, select:focus { border-color: var(--highlighter); box-shadow: 0 0 10px rgba(228, 255, 91, 0.3); }
        select option { background: #1C1A42; color: #fff; }
        .btn-generate { width: 100%; background: var(--coral); color: #fff; border: none; padding: 14px; border-radius: 12px; font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1rem; cursor: pointer; margin-top: 15px; transition: all 0.3s; box-shadow: 0 4px 18px rgba(255, 107, 84, 0.4); }
        .btn-generate:hover { transform: translateY(-2px); box-shadow: 0 6px 25px rgba(255, 107, 84, 0.7); }
        .btn-generate:disabled { opacity: 0.6; cursor: not-allowed; }

        .studio-main { flex: 1; padding: 30px 38px; overflow-y: auto; transition: all 0.3s ease; }
        .studio-grid { display: grid; grid-template-columns: 2.2fr 1.3fr; gap: 28px; }

        .spinner-container { display: none; text-align: center; padding: 60px; }
        .spinner { width: 50px; height: 50px; border: 4px solid rgba(246, 241, 227, 0.15); border-top-color: var(--coral); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px auto; }
        @keyframes spin { to { transform: rotate(360deg); } }

        .navbar-top-row {
            display: contents;
        }

        @media (max-width: 1080px) {
            .navbar { padding: 14px 20px; }
            .nav-links { gap: 8px; }
            .nav-link { padding: 6px 10px; font-size: 0.85rem; }
            .studio-main { padding: 24px 20px; }
        }

        @media (max-width: 860px) {
            .navbar {
                padding: 10px 14px 8px 14px;
                background: rgba(20, 19, 43, 0.96) !important;
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border-bottom: 1px solid var(--line);
                position: sticky;
                top: 0;
                z-index: 10000;
            }
            .navbar-inner {
                display: flex;
                flex-direction: column;
                gap: 8px;
                width: 100%;
            }
            .navbar-top-row {
                display: flex;
                width: 100%;
                justify-content: flex-start;
                align-items: center;
            }
            .brand-logo { font-size: 1.2rem; }
            .nav-cta { padding: 7px 14px; font-size: 0.8rem; border-radius: 10px; }
            .nav-links {
                width: 100%;
                overflow-x: auto;
                white-space: nowrap;
                padding: 2px 2px 6px 2px;
                justify-content: flex-start;
                gap: 8px;
                -webkit-overflow-scrolling: touch;
                scrollbar-width: none !important;
                -ms-overflow-style: none !important;
            }
            .nav-links::-webkit-scrollbar {
                display: none !important;
                width: 0 !important;
                height: 0 !important;
            }
            .nav-link {
                font-size: 0.82rem;
                padding: 6px 12px;
                flex-shrink: 0;
                border-radius: 20px;
                background: rgba(246, 241, 227, 0.06);
                border: 1px solid rgba(246, 241, 227, 0.08);
            }
            .nav-link.active {
                background: rgba(228, 255, 91, 0.18);
                border-color: var(--highlighter);
                color: var(--highlighter);
            }

            /* HERO SECTION */
            .hero-grid {
                grid-template-columns: 1fr !important;
                gap: 24px !important;
                text-align: center;
            }
            .hero-grid .eyebrow-caveat { margin: 0 auto; }
            .hero-btns {
                justify-content: center !important;
                flex-direction: column !important;
            }
            .hero-btns button { width: 100% !important; }

            .hero-deck {
                transform: scale(0.72);
                transform-origin: center center;
                height: 190px;
                margin: 0 auto;
                max-width: 100%;
            }

            /* STUDIO */
            .studio-container { flex-direction: column; }
            .studio-sidebar {
                width: 100%;
                position: relative;
                top: 0;
                max-height: none;
                border-right: none;
                border-bottom: 1px solid var(--line);
                padding: 20px 16px;
            }
            .studio-grid { grid-template-columns: 1fr !important; }
            .grocery-panel { position: relative; top: 0; }
        }

        @media (max-width: 600px) {
            h1 { font-size: 2.2rem !important; }
            h2 { font-size: 1.7rem !important; }
            .hero-deck {
                transform: scale(0.56);
                height: 150px;
            }
            section { padding: 40px 16px !important; }
            .panel-card, .paper-card, .schedule-card, .grocery-panel {
                padding: 18px 14px !important;
                border-radius: 16px !important;
            }
            .form-row { flex-direction: column !important; gap: 0 !important; }
            .entry-grid-3 { grid-template-columns: 1fr !important; }
            .entry-grid-2 { grid-template-columns: 1fr !important; }
            .schedule-card-inner { grid-template-columns: 1fr !important; }
            .story-grid { grid-template-columns: 1fr !important; }
        }

        @media (max-width: 380px) {
            h1 { font-size: 1.85rem !important; }
            .hero-deck {
                transform: scale(0.46);
                height: 125px;
            }
        }
    </style>
</head>
<body>
    <canvas id="bg-3d-canvas"></canvas>
    <div class="bg-grid-3d"></div>
    <div class="ambient-blob-1"></div>
    <div class="ambient-blob-2"></div>
    <div class="ambient-blob-3"></div>

    <!-- TOP NAVIGATION BAR -->
    <nav class="navbar">
        <div class="navbar-inner">
            <div class="navbar-top-row">
                <a class="brand-logo" onclick="switchPage('home')">
                    <span style="display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; background: linear-gradient(135deg, var(--coral), var(--highlighter)); border-radius: 9px; box-shadow: 0 4px 12px rgba(255, 107, 84, 0.4); margin-right: 2px;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" fill="#14132B" stroke="#14132B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </span>
                    StudentFit <span>AI</span>
                </a>
            </div>
            <ul class="nav-links">
                <li><a class="nav-link active" id="nav-home" onclick="switchPage('home')">🏠 Home</a></li>
                <li><a class="nav-link" id="nav-how" onclick="switchPage('how')">📖 How it Works</a></li>
                <li><a class="nav-link" id="nav-features" onclick="switchPage('features')">✨ Features</a></li>
                <li><a class="nav-link" id="nav-plans" onclick="switchPage('plans')">🏷️ Plans</a></li>
                <li><a class="nav-link" id="nav-story" onclick="switchPage('story')">💡 Story</a></li>
                <li><a class="nav-link" id="nav-generator" onclick="switchPage('generator')">⚡ Generator</a></li>
            </ul>
        </div>
    </nav>

    <!-- =========================================================================
         PAGE 1: HOME
         ========================================================================= -->
    <div class="page-view active-page" id="page-home">
        <section style="padding: 60px 40px 40px 40px; max-width: 1200px; margin: 0 auto;">
            <div class="hero-grid" style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 40px; align-items: center;">
                <div>
                    <div class="eyebrow-caveat">built between lectures & leftovers ~</div>
                    <h1 style="font-size: 3.2rem; line-height: 1.15; margin-bottom: 18px;">Fitness that syncs to your <span style="color: var(--highlighter);">syllabus.</span></h1>
                    <p style="font-size: 1.1rem; color: var(--text-soft); line-height: 1.6; margin-bottom: 28px;">
                        Most fitness apps assume a full kitchen, a car, and endless free time. <strong>StudentFit AI</strong> plans around what students actually have: dorm-room gear, a real grocery budget, cooking skill, and an exam schedule that can't be ignored.
                    </p>
                    <div class="hero-btns" style="display: flex; gap: 14px;">
                        <button class="btn-primary-lg" onclick="switchPage('generator')">⚡ Generate My Week</button>
                        <button class="btn-secondary-lg" onclick="switchPage('how')">📖 See how it works</button>
                    </div>
                </div>

                <!-- 7-CARD HERO DECK -->
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
                    <div class="deck-card deck-card-4">
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
            </div>
        </section>

        <!-- REAL STAT TICKER -->
        <div class="marquee-container">
            <div class="marquee-content">
                ⚡ 4 FITNESS GOALS &nbsp;•&nbsp; 3 GEAR TIERS &nbsp;•&nbsp; 5 CUISINES &nbsp;•&nbsp; 3 BUDGET TIERS &nbsp;•&nbsp; 3 COOKING SKILL LEVELS &nbsp;•&nbsp; 7 DAYS FULLY SYNCHRONIZED &nbsp;•&nbsp; 100% STUDENT-FOCUSED &nbsp;•&nbsp; 4 FITNESS GOALS &nbsp;•&nbsp; 3 GEAR TIERS &nbsp;•&nbsp; 5 CUISINES &nbsp;•&nbsp; 3 BUDGET TIERS &nbsp;•&nbsp; 3 COOKING SKILL LEVELS &nbsp;•&nbsp; 7 DAYS FULLY SYNCHRONIZED
            </div>
        </div>

        <!-- DORM ROOM BAND -->
        <section style="padding: 70px 40px; max-width: 1140px; margin: 0 auto;">
            <div style="text-align: center; margin-bottom: 35px;">
                <span class="tag-pill">STUDENT REALITY CHECK</span>
                <h2 style="font-size: 2.3rem; margin-top: 10px;">Built for dorm rooms, not gym floors.</h2>
                <p style="color: var(--text-soft); max-width: 680px; margin: 0 auto;">Everything engineered around college constraints so you stay consistent through midterms and finals.</p>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
                <div class="panel-card">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">🏠</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">No Gym Required</h3>
                    <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.6;">Only have 2m² of carpet next to your desk? Get bodyweight and dumbbell routines with calculated tempo.</p>
                </div>
                <div class="panel-card">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">💰</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Budget Respected</h3>
                    <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.6;">Get weekly grocery shopping lists with quantities and localized prices (₹, $, €, £) mapped to high-protein staples.</p>
                </div>
                <div class="panel-card">
                    <div style="font-size: 2.4rem; margin-bottom: 12px;">📚</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Exam-Week Aware</h3>
                    <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.6;">"Exam Stress Relief" is a first-class fitness goal that balances nervous system fatigue with brain-power nutrition.</p>
                </div>
            </div>
        </section>

        <!-- TESTIMONIALS -->
        <section style="padding: 40px 40px 80px 40px; max-width: 1140px; margin: 0 auto;">
            <div style="text-align: center; margin-bottom: 30px;">
                <span class="tag-pill">CAMPUS VOICES</span>
                <h2 style="font-size: 2.1rem; margin-top: 10px;">Tested across semester schedules.</h2>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
                <div class="paper-card">
                    <div style="font-size: 1.1rem; margin-bottom: 10px;">⭐️⭐️⭐️⭐️⭐️</div>
                    <p style="font-size: 0.95rem; font-style: italic; margin-bottom: 16px;">
                        "Other workout apps kept giving me salmon and asparagus recipes that cost half my weekly budget. StudentFit gave me eggs, dal, and oats that cost almost nothing and hit 130g protein."
                    </p>
                    <strong style="display: block; font-family: 'Space Mono', monospace; font-size: 0.82rem; color: var(--coral) !important;">3RD YEAR COMPUTER SCIENCE</strong>
                </div>
                <div class="paper-card">
                    <div style="font-size: 1.1rem; margin-bottom: 10px;">⭐️⭐️⭐️⭐️⭐️</div>
                    <p style="font-size: 0.95rem; font-style: italic; margin-bottom: 16px;">
                        "During midterm anatomy blocks, I switched to Exam Stress Relief. 20-minute mobility sessions and brain-boosting meals kept me energized without burnout."
                    </p>
                    <strong style="display: block; font-family: 'Space Mono', monospace; font-size: 0.82rem; color: var(--coral) !important;">2ND YEAR PRE-MED</strong>
                </div>
                <div class="paper-card">
                    <div style="font-size: 1.1rem; margin-bottom: 10px;">⭐️⭐️⭐️⭐️⭐️</div>
                    <p style="font-size: 0.95rem; font-style: italic; margin-bottom: 16px;">
                        "I have zero kitchen skills besides a microwave. The Microwave Only setting gave me high-protein oatmeal, steamed lentils, and paneer wraps with zero cooking hassle."
                    </p>
                    <strong style="display: block; font-family: 'Space Mono', monospace; font-size: 0.82rem; color: var(--coral) !important;">1ST YEAR ARCHITECTURE</strong>
                </div>
            </div>
        </section>
    </div>

    <!-- =========================================================================
         PAGE 2: HOW IT WORKS
         ========================================================================= -->
    <div class="page-view" id="page-how">
        <section style="padding: 60px 40px; max-width: 1000px; margin: 0 auto;">
            <div class="eyebrow-caveat">step by step logic ~</div>
            <h1 style="font-size: 2.8rem; margin-bottom: 12px;">How StudentFit AI Works</h1>
            <p style="color: var(--text-soft); font-size: 1.1rem; line-height: 1.6; margin-bottom: 35px;">
                Every axis calculates exercises, meals, and weekly grocery quantities based on your simultaneous constraints.
            </p>

            <div class="panel-card" style="margin-bottom: 24px;">
                <span class="tag-pill">STEP 1</span>
                <h3 style="margin: 8px 0; font-size: 1.4rem;">Campus Bio-Data</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem;">Gender (Male/Female/Other), Age (16-40), Weight (kg/lbs), Height (cm/ft).</p>
            </div>
            <div class="panel-card" style="margin-bottom: 24px;">
                <span class="tag-pill" style="border-color: var(--coral); color: var(--coral);">STEP 2</span>
                <h3 style="margin: 8px 0; font-size: 1.4rem;">Goals & Available Gear</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem;">4 Goals (Build Muscle / Lose Weight / Get Shredded / Exam Stress Relief) x 3 Gear Tiers (Full Gym / Dumbbells / Dorm Floor).</p>
            </div>
            <div class="panel-card" style="margin-bottom: 24px;">
                <span class="tag-pill" style="border-color: var(--lilac); color: var(--lilac);">STEP 3</span>
                <h3 style="margin: 8px 0; font-size: 1.4rem;">Kitchen Setup, Cuisine & Local Currency</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem;">5 Cuisines (Indian/Global/Mediterranean/Asian/Vegan) x 3 Budget Tiers x 3 Cooking Skills (Microwave/Basic Stove/Full Chef).</p>
            </div>

            <div style="text-align: center; margin-top: 40px;">
                <button class="btn-primary-lg" onclick="switchPage('generator')">⚡ Launch AI Generator</button>
            </div>
        </section>
    </div>

    <!-- =========================================================================
         PAGE 3: FEATURES
         ========================================================================= -->
    <div class="page-view" id="page-features">
        <section style="padding: 60px 40px; max-width: 1140px; margin: 0 auto;">
            <div class="eyebrow-caveat">complete feature breakdown ~</div>
            <h1 style="font-size: 2.8rem; margin-bottom: 12px;">Six Core Pillars of StudentFit AI</h1>
            <p style="color: var(--text-soft); font-size: 1.1rem; line-height: 1.6; margin-bottom: 35px;">
                Hover or tap each card to flip and discover how every dimension adapts simultaneously to campus life.
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px;">
                <div class="flip-card-container" onclick="this.classList.toggle('flipped')">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div style="font-size: 2.4rem; margin-bottom: 10px;">🏃‍♂️</div>
                            <h3>Bio-Data Personalization</h3>
                            <p style="color: var(--text-soft); font-size: 0.85rem;">Tap or hover to flip</p>
                        </div>
                        <div class="flip-card-back">
                            <h4>Adaptive Calorie Math</h4>
                            <p style="font-size: 0.9rem; color: #fff;">Calculates baseline metabolic rates according to student age, gender, and metrics in kg/lbs.</p>
                        </div>
                    </div>
                </div>
                <div class="flip-card-container" onclick="this.classList.toggle('flipped')">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div style="font-size: 2.4rem; margin-bottom: 10px;">🎯</div>
                            <h3>Goal-Driven Programming</h3>
                            <p style="color: var(--text-soft); font-size: 0.85rem;">Tap or hover to flip</p>
                        </div>
                        <div class="flip-card-back">
                            <h4>Targeted Splits</h4>
                            <p style="font-size: 0.9rem; color: #fff;">Switches workout volume between muscle bulking, fat loss, and exam stress relief.</p>
                        </div>
                    </div>
                </div>
                <div class="flip-card-container" onclick="this.classList.toggle('flipped')">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div style="font-size: 2.4rem; margin-bottom: 10px;">🏋️</div>
                            <h3>Gear-Adaptive Workouts</h3>
                            <p style="color: var(--text-soft); font-size: 0.85rem;">Tap or hover to flip</p>
                        </div>
                        <div class="flip-card-back">
                            <h4>Space & Equipment Fit</h4>
                            <p style="font-size: 0.9rem; color: #fff;">Substitutes exercises whether you have gym access, light dumbbells, or dorm floor space.</p>
                        </div>
                    </div>
                </div>
                <div class="flip-card-container" onclick="this.classList.toggle('flipped')">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div style="font-size: 2.4rem; margin-bottom: 10px;">🥗</div>
                            <h3>Cuisine-Flexible Meals</h3>
                            <p style="color: var(--text-soft); font-size: 0.85rem;">Tap or hover to flip</p>
                        </div>
                        <div class="flip-card-back">
                            <h4>Cultural Respect</h4>
                            <p style="font-size: 0.9rem; color: #fff;">Builds recipes around Indian, Mediterranean, Asian, Vegan, and Global staples.</p>
                        </div>
                    </div>
                </div>
                <div class="flip-card-container" onclick="this.classList.toggle('flipped')">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div style="font-size: 2.4rem; margin-bottom: 10px;">🛒</div>
                            <h3>Budget-Tiered Groceries</h3>
                            <p style="color: var(--text-soft); font-size: 0.85rem;">Tap or hover to flip</p>
                        </div>
                        <div class="flip-card-back">
                            <h4>1-Person Shopping List</h4>
                            <p style="font-size: 0.9rem; color: #fff;">Weekly shopping list with exact quantities and realistic costs in INR, USD, EUR, GBP, etc.</p>
                        </div>
                    </div>
                </div>
                <div class="flip-card-container" onclick="this.classList.toggle('flipped')">
                    <div class="flip-card-inner">
                        <div class="flip-card-front">
                            <div style="font-size: 2.4rem; margin-bottom: 10px;">🍳</div>
                            <h3>Cooking-Skill Recipes</h3>
                            <p style="color: var(--text-soft); font-size: 0.85rem;">Tap or hover to flip</p>
                        </div>
                        <div class="flip-card-back">
                            <h4>Appliance Matching</h4>
                            <p style="font-size: 0.9rem; color: #fff;">Meal prep tailored to your exact appliances: Microwave Only, Basic Stove, or Full Chef.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- =========================================================================
         PAGE 4: PLANS
         ========================================================================= -->
    <div class="page-view" id="page-plans">
        <section style="padding: 60px 40px; max-width: 1140px; margin: 0 auto;">
            <div class="eyebrow-caveat">transparent tiers ~</div>
            <h1 style="font-size: 2.8rem; margin-bottom: 12px;">Student Plans & Tiers</h1>
            <p style="color: var(--text-soft); font-size: 1.1rem; line-height: 1.6; margin-bottom: 35px;">
                Named after our budget philosophy. (Note: Pricing below is illustrative and conceptual — the core AI generator is 100% free for all students).
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
                <div class="panel-card">
                    <span class="mono-label">TIER 1</span>
                    <h3 style="font-size: 1.5rem; margin: 8px 0;">Cheap Tier</h3>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 14px;">$0 <span style="font-size: 0.9rem; color: var(--text-soft);">/ forever</span></div>
                    <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 16px;">Essential 7-day synchronization for students on tight hostel budgets.</p>
                    <ul style="list-style: none; padding-left: 0; color: var(--text-soft); font-size: 0.9rem; line-height: 1.8;">
                        <li>✅ 7-Day Mon–Sun Plan Generation</li>
                        <li>✅ Dorm & Bodyweight Exercises</li>
                        <li>✅ 1-Person Weekly Grocery Checklist</li>
                        <li>✅ Local Currency Conversions</li>
                        <li>✅ PDF Export</li>
                    </ul>
                </div>
                <div class="panel-card" style="border: 2px solid var(--highlighter); background: var(--ink3);">
                    <span class="mono-label" style="color: var(--highlighter);">TIER 2 • MOST POPULAR</span>
                    <h3 style="font-size: 1.5rem; margin: 8px 0; color: var(--highlighter);">Moderate Tier</h3>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 14px;">$3 <span style="font-size: 0.9rem; color: var(--text-soft);">/ semester (concept)</span></div>
                    <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 16px;">Advanced exam block optimization with multiple cuisine swaps.</p>
                    <ul style="list-style: none; padding-left: 0; color: #fff; font-size: 0.9rem; line-height: 1.8;">
                        <li>✅ Everything in Cheap Tier</li>
                        <li>✅ Exam Stress Relief Auto-Tuning</li>
                        <li>✅ Multi-Cuisine Meal Swaps</li>
                        <li>✅ High-Protein Bulk Cheatsheets</li>
                    </ul>
                </div>
                <div class="panel-card">
                    <span class="mono-label" style="color: var(--coral);">TIER 3</span>
                    <h3 style="font-size: 1.5rem; margin: 8px 0;">Premium Tier</h3>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #fff; margin-bottom: 14px;">$8 <span style="font-size: 0.9rem; color: var(--text-soft);">/ room (concept)</span></div>
                    <p style="color: var(--text-soft); font-size: 0.9rem; margin-bottom: 16px;">Designed for dorm flatmates pooling shared groceries and recipes.</p>
                    <ul style="list-style: none; padding-left: 0; color: var(--text-soft); font-size: 0.9rem; line-height: 1.8;">
                        <li>✅ Everything in Moderate Tier</li>
                        <li>✅ Shared Flat Grocery Pooling</li>
                        <li>✅ Roommate Synchronized Meal Prep</li>
                    </ul>
                </div>
            </div>
        </section>
    </div>

    <!-- =========================================================================
         PAGE 5: STORY
         ========================================================================= -->
    <div class="page-view" id="page-story">
        <section style="padding: 60px 40px; max-width: 900px; margin: 0 auto;">
            <div class="eyebrow-caveat">our mission & philosophy ~</div>
            <h1 style="font-size: 2.8rem; margin-bottom: 12px;">Built for Students, Not Gym Culture</h1>
            <div class="panel-card" style="margin: 25px 0 35px 0; border-left: 4px solid var(--highlighter);">
                <p style="font-size: 1.1rem; line-height: 1.7; color: #fff; margin-bottom: 12px;">
                    The fitness industry is designed for working adults with fully equipped kitchens, cars for weekly supermarket runs, disposable income for specialty supplements, and predictable 9-to-5 schedules.
                </p>
                <p style="font-size: 1rem; line-height: 1.7; color: var(--text-soft);">
                    When students try to follow these plans, they hit walls: dorm floors with zero equipment, tight budgets that can't afford expensive recipes, microwave-only limits, and exam weeks where high-intensity training leads to burnout.
                </p>
            </div>

            <h3 style="margin-bottom: 20px;">Who StudentFit AI Is Built For</h3>
            <div class="story-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="panel-card">
                    <h4>🏠 Dorm & Hostel Dwellers</h4>
                    <p style="color: var(--text-soft); font-size: 0.9rem; margin-top: 6px;">Workouts adapted to small rooms and campus walking.</p>
                </div>
                <div class="panel-card">
                    <h4>💵 Budget-Conscious Students</h4>
                    <p style="color: var(--text-soft); font-size: 0.9rem; margin-top: 6px;">Prioritizes cheap high-protein staples: eggs, dal, oats, tofu.</p>
                </div>
                <div class="panel-card">
                    <h4>🧠 Exam-Week Survivors</h4>
                    <p style="color: var(--text-soft); font-size: 0.9rem; margin-top: 6px;">Active recovery and brain focus during midterms & finals.</p>
                </div>
                <div class="panel-card">
                    <h4>🍳 First-Time Cooks</h4>
                    <p style="color: var(--text-soft); font-size: 0.9rem; margin-top: 6px;">Fast batch meal prep taking under 20 minutes.</p>
                </div>
            </div>
        </section>
    </div>

    <!-- =========================================================================
         PAGE 6: GENERATOR STUDIO (ENTRY WIZARD -> SIDEBAR DASHBOARD)
         ========================================================================= -->
    <div class="page-view" id="page-generator">
        <!-- 1. ENTRY SETUP WIZARD (FIRST TIME VIEW) -->
        <div id="studio-entry-view" style="max-width: 900px; margin: 40px auto 80px auto; padding: 0 20px;">
            <div class="panel-card" style="background: var(--ink2); border: 1px solid var(--coral); box-shadow: 0 20px 60px rgba(0,0,0,0.6); padding: 40px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <div class="tag-pill">⚡ Step 1 of 1 — Personalize Your Week</div>
                    <h2 style="font-size: 2.2rem; font-weight: 800; color: #fff; margin: 10px 0;">Student Fit Profile Setup</h2>
                    <p style="color: var(--text-soft); font-size: 1rem;">Configure your campus fitness constraints once. Your customized 7-day schedule & budget grocery list will generate instantly.</p>
                </div>

                <div class="entry-grid-2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                    <!-- BIO DATA -->
                    <div style="background: rgba(20, 19, 43, 0.6); border: 1px solid var(--line); border-radius: 14px; padding: 20px;">
                        <h4 style="color: var(--highlighter); margin-bottom: 14px; font-size: 1.05rem;">🏃‍♂️ Campus Bio-Data</h4>
                        <div class="form-row">
                            <div class="form-group">
                                <label>Gender</label>
                                <select id="entry_gender" autocomplete="off" onchange="syncToSidebar('gender', this.value)">
                                    <option value="" disabled selected hidden>Select Gender</option>
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Age</label>
                                <input type="number" id="entry_age" placeholder="Age (e.g. 20)" min="16" max="40" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" onchange="syncToSidebar('age', this.value)">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group" style="flex: 2;">
                                <label>Weight</label>
                                <input type="number" id="entry_weight" placeholder="Weight (e.g. 70)" min="30" max="300" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" onchange="syncToSidebar('weight', this.value)">
                            </div>
                            <div class="form-group" style="flex: 1.2;">
                                <label>Unit</label>
                                <select id="entry_weightUnit" autocomplete="off" onchange="syncToSidebar('weightUnit', this.value)">
                                    <option value="kg" selected>kg</option>
                                    <option value="lbs">lbs</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group" style="flex: 2;">
                                <label>Height</label>
                                <input type="number" id="entry_height" placeholder="Height (e.g. 170)" min="100" max="250" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" onchange="syncToSidebar('height', this.value)">
                            </div>
                            <div class="form-group" style="flex: 1.2;">
                                <label>Unit</label>
                                <select id="entry_heightUnit" autocomplete="off" onchange="syncToSidebar('heightUnit', this.value)">
                                    <option value="cm" selected>cm</option>
                                    <option value="ft/in">ft/in</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- GOALS & GEAR -->
                    <div style="background: rgba(20, 19, 43, 0.6); border: 1px solid var(--line); border-radius: 14px; padding: 20px;">
                        <h4 style="color: var(--coral); margin-bottom: 14px; font-size: 1.05rem;">🎯 Goals & Gear</h4>
                        <div class="form-group">
                            <label>Primary Fitness Target</label>
                            <select id="entry_goal" autocomplete="off" onchange="handleGoalChange('entry', this.value)">
                                <option value="" disabled selected hidden>Select Fitness Goal</option>
                                <option value="Build Muscle">💪 Build Muscle & Bulk</option>
                                <option value="Lose Weight">🔥 Lose Fat & Lean Out</option>
                                <option value="Get Shredded">⚡ Athletic Tone & Shred</option>
                                <option value="Exam Stress Relief">🧘 Exam Stress Relief & Focus</option>
                                <option value="Custom">✍️ Custom / Type Your Own Goal...</option>
                            </select>
                            <input type="text" id="entry_custom_goal" placeholder="e.g. Marathon Prep, Fix Posture, Jump Higher..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" style="display: none; margin-top: 8px; border-color: var(--highlighter);" oninput="syncToSidebar('custom_goal', this.value)">
                        </div>
                        <div class="form-group">
                            <label>Available Equipment</label>
                            <select id="entry_equipment" autocomplete="off" onchange="syncToSidebar('equipment', this.value)">
                                <option value="" disabled selected hidden>Select Available Gear</option>
                                <option value="Full Gym">🏛️ Full University Gym</option>
                                <option value="Dumbbells Only">🏋️ Dumbbells Only</option>
                                <option value="No Equipment (Dorm)">🏠 No Equipment (Dorm Floor)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 24px; background: rgba(20, 19, 43, 0.6); border: 1px solid var(--line); border-radius: 14px; padding: 20px;">
                    <h4 style="color: var(--lilac); margin-bottom: 14px; font-size: 1.05rem;">🥑 Kitchen, Cuisine & Local Currency</h4>
                    <div class="entry-grid-3" style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px;">
                        <div class="form-group">
                            <label>Cuisine Preference</label>
                            <select id="entry_cuisine" autocomplete="off" onchange="syncToSidebar('cuisine', this.value)">
                                <option value="" disabled selected hidden>Select Cuisine</option>
                                <option value="Indian">🍛 Indian</option>
                                <option value="Global">🌍 Global</option>
                                <option value="Mediterranean">🥗 Mediterranean</option>
                                <option value="Asian">🥢 Asian</option>
                                <option value="Vegan">🌱 Vegan</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Budget Tier</label>
                            <select id="entry_budget" autocomplete="off" onchange="syncToSidebar('budget', this.value)">
                                <option value="" disabled selected hidden>Select Budget Tier</option>
                                <option value="Cheap ($)">Cheap ($)</option>
                                <option value="Moderate ($$)">Moderate ($$)</option>
                                <option value="Premium ($$$)">Premium ($$$)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Preferred Currency</label>
                            <select id="entry_currency" autocomplete="off" onchange="syncToSidebar('currency', this.value)">
                                <option value="" disabled selected hidden>Select Currency</option>
                                <option value="INR (₹)">INR (₹) - Rupee</option>
                                <option value="USD ($)">USD ($) - Dollar</option>
                                <option value="EUR (€)">EUR (€) - Euro</option>
                                <option value="GBP (£)">GBP (£) - Pound</option>
                                <option value="CAD ($)">CAD ($) - Dollar</option>
                                <option value="AUD ($)">AUD ($) - Dollar</option>
                                <option value="AED (د.إ)">AED (د.إ) - Dirham</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group" style="margin-top: 10px;">
                        <label>Cooking Setup / Facility</label>
                        <select id="entry_cookingSkill" autocomplete="off" onchange="syncToSidebar('cookingSkill', this.value)">
                            <option value="" disabled selected hidden>Select Cooking Setup</option>
                            <option value="Microwave Only">⚡ Microwave / Kettle Only (Strict Dorm)</option>
                            <option value="Basic Stove">🍳 Basic Stove / Single Induction</option>
                            <option value="Full Chef">👨‍🍳 Full Kitchen & Oven</option>
                        </select>
                    </div>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <button class="btn-primary-lg" style="width: 100%; max-width: 480px; font-size: 1.15rem;" onclick="submitEntryAndGenerate()">
                        🚀 GENERATE 7-DAY SCHEDULE & GROCERIES
                    </button>
                </div>
            </div>
        </div>

        <!-- 2. STUDIO DASHBOARD VIEW -->
        <div id="studio-dashboard-view" class="studio-container" style="display: none;">
            <aside class="studio-sidebar" id="studioSidebar">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h2 style="font-size: 1.25rem;">⚡ Studio Controls</h2>
                    <div style="display: flex; gap: 6px; align-items: center;">
                        <button onclick="showWizardEntry()" style="background: rgba(246,241,227,0.08); border: 1px solid var(--line); color: var(--highlighter); border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; cursor: pointer;">✏️ Full View</button>
                        <button onclick="toggleSidebar()" title="Close Sidebar" style="background: rgba(255, 107, 84, 0.15); border: 1px solid var(--coral); color: var(--coral); border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; cursor: pointer; font-weight: 700;">✕ Close</button>
                    </div>
                </div>

                <span class="mono-label">🏃‍♂️ BIO-DATA</span>
                <div class="form-row" style="margin-top: 8px;">
                    <div class="form-group">
                        <label>Gender</label>
                        <select id="gender" autocomplete="off">
                            <option value="" disabled selected hidden>Select Gender</option>
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Age</label>
                        <input type="number" id="age" placeholder="Age" min="16" max="40" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group" style="flex: 2;">
                        <label>Weight</label>
                        <input type="number" id="weight" placeholder="Weight" min="30" max="300" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
                    </div>
                    <div class="form-group" style="flex: 1.2;">
                        <label>Unit</label>
                        <select id="weightUnit" autocomplete="off">
                            <option value="kg" selected>kg</option>
                            <option value="lbs">lbs</option>
                        </select>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group" style="flex: 2;">
                        <label>Height</label>
                        <input type="number" id="height" placeholder="Height" min="100" max="250" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
                    </div>
                    <div class="form-group" style="flex: 1.2;">
                        <label>Unit</label>
                        <select id="heightUnit" autocomplete="off">
                            <option value="cm" selected>cm</option>
                            <option value="ft/in">ft/in</option>
                        </select>
                    </div>
                </div>

                <span class="mono-label" style="display: block; margin-top: 14px;">🎯 GOALS & GEAR</span>
                <div class="form-group" style="margin-top: 8px;">
                    <label>Fitness Target</label>
                    <select id="goal" autocomplete="off" onchange="handleGoalChange('sidebar', this.value)">
                        <option value="" disabled selected hidden>Select Fitness Goal</option>
                        <option value="Build Muscle">Build Muscle</option>
                        <option value="Lose Weight">Lose Weight</option>
                        <option value="Get Shredded">Get Shredded</option>
                        <option value="Exam Stress Relief">Exam Stress Relief</option>
                        <option value="Custom">✍️ Custom Goal...</option>
                    </select>
                    <input type="text" id="custom_goal" placeholder="Describe your custom goal..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" style="display: none; margin-top: 8px; border-color: var(--highlighter);">
                </div>

                <div class="form-group">
                    <label>Available Equipment</label>
                    <select id="equipment" autocomplete="off">
                        <option value="" disabled selected hidden>Select Available Gear</option>
                        <option value="Full Gym">Full Gym</option>
                        <option value="Dumbbells Only">Dumbbells Only</option>
                        <option value="No Equipment (Dorm)">No Equipment (Dorm)</option>
                    </select>
                </div>

                <span class="mono-label" style="display: block; margin-top: 14px;">🥑 KITCHEN & BUDGET</span>
                <div class="form-group" style="margin-top: 8px;">
                    <label>Cuisine Preference</label>
                    <select id="cuisine" autocomplete="off">
                        <option value="" disabled selected hidden>Select Cuisine</option>
                        <option value="Indian">Indian</option>
                        <option value="Global">Global</option>
                        <option value="Mediterranean">Mediterranean</option>
                        <option value="Asian">Asian</option>
                        <option value="Vegan">Vegan</option>
                    </select>
                </div>

                <div class="form-row">
                    <div class="form-group" style="flex: 1.5;">
                        <label>Budget Tier</label>
                        <select id="budget" autocomplete="off">
                            <option value="" disabled selected hidden>Select Budget Tier</option>
                            <option value="Cheap ($)">Cheap ($)</option>
                            <option value="Moderate ($$)">Moderate ($$)</option>
                            <option value="Premium ($$$)">Premium ($$$)</option>
                        </select>
                    </div>
                    <div class="form-group" style="flex: 1.5;">
                        <label>Currency</label>
                        <select id="currency" autocomplete="off">
                            <option value="" disabled selected hidden>Select Currency</option>
                            <option value="INR (₹)">INR (₹)</option>
                            <option value="USD ($)">USD ($)</option>
                            <option value="EUR (€)">EUR (€)</option>
                            <option value="GBP (£)">GBP (£)</option>
                            <option value="CAD ($)">CAD ($)</option>
                            <option value="AUD ($)">AUD ($)</option>
                            <option value="AED (د.إ)">AED (د.إ)</option>
                        </select>
                    </div>
                </div>

                <div class="form-group">
                    <label>Cooking Facility</label>
                    <select id="cookingSkill" autocomplete="off">
                        <option value="" disabled selected hidden>Select Cooking Setup</option>
                        <option value="Microwave Only">Microwave Only</option>
                        <option value="Basic Stove">Basic Stove</option>
                        <option value="Full Chef">Full Chef</option>
                    </select>
                </div>

                <button class="btn-generate" id="generateBtn" onclick="generatePlan()">🔄 RE-GENERATE PLAN</button>
            </aside>

            <!-- STUDIO WORKSPACE -->
            <main class="studio-main">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid var(--line); padding-bottom: 14px; flex-wrap: wrap; gap: 12px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <button id="toggleOpenSidebarBtn" onclick="toggleSidebar()" style="display: none; background: rgba(228, 255, 91, 0.15); border: 1px solid var(--highlighter); color: var(--highlighter); border-radius: 10px; padding: 8px 14px; font-family: 'Space Mono', monospace; font-size: 0.85rem; cursor: pointer; font-weight: bold; transition: all 0.2s;">
                            ⚡ Show Controls ▸
                        </button>
                        <div>
                            <h1>AI Planner Studio ⚡</h1>
                            <p style="color: var(--text-soft); font-size: 0.95rem;">Synchronized Monday–Sunday Workout & Meal Schedules</p>
                        </div>
                    </div>
                    <button id="downloadBtn" class="nav-cta" style="display: none;" onclick="downloadPDF()">📥 Save Plan (PDF)</button>
                </div>

                <div id="spinner" class="spinner-container">
                    <div class="spinner"></div>
                    <h3 style="color: var(--highlighter); margin-bottom: 6px;">🗓️ AI Neural Engine is Synchronizing Your Week...</h3>
                    <p style="color: var(--text-soft);">Tailoring exercises, student meals, and localized grocery budgets...</p>
                </div>

                <div id="resultsArea" class="studio-grid" style="display: none;">
                    <div id="daysContainer"></div>
                    <div class="grocery-panel" id="groceryCard"></div>
                </div>
            </main>
        </div>
    </div>

    <!-- JAVASCRIPT -->
    <script>
        let currentRawPlan = "";

        function toggleSidebar() {
            const sidebar = document.getElementById('studioSidebar');
            const openBtn = document.getElementById('toggleOpenSidebarBtn');
            if (sidebar) {
                if (sidebar.classList.contains('sidebar-closed')) {
                    sidebar.classList.remove('sidebar-closed');
                    if (openBtn) openBtn.style.display = 'none';
                } else {
                    sidebar.classList.add('sidebar-closed');
                    if (openBtn) openBtn.style.display = 'inline-flex';
                }
            }
        }

        function handleGoalChange(source, val) {
            const entryCustom = document.getElementById('entry_custom_goal');
            const sidebarCustom = document.getElementById('custom_goal');

            if (source === 'entry') {
                syncToSidebar('goal', val);
                if (val === 'Custom') {
                    if (entryCustom) {
                        entryCustom.style.display = 'block';
                        entryCustom.focus();
                    }
                    if (sidebarCustom) sidebarCustom.style.display = 'block';
                } else {
                    if (entryCustom) entryCustom.style.display = 'none';
                    if (sidebarCustom) sidebarCustom.style.display = 'none';
                }
            } else {
                if (val === 'Custom') {
                    if (sidebarCustom) {
                        sidebarCustom.style.display = 'block';
                        sidebarCustom.focus();
                    }
                    if (entryCustom) entryCustom.style.display = 'block';
                } else {
                    if (sidebarCustom) sidebarCustom.style.display = 'none';
                    if (entryCustom) entryCustom.style.display = 'none';
                }
            }
        }

        function syncToSidebar(id, val) {
            const sidebarElem = document.getElementById(id);
            if (sidebarElem) sidebarElem.value = val;
        }

        function showWizardEntry() {
            document.getElementById('studio-entry-view').style.display = 'block';
            document.getElementById('studio-dashboard-view').style.display = 'none';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function submitEntryAndGenerate() {
            const gender = document.getElementById('entry_gender').value;
            const age = document.getElementById('entry_age').value;
            const weight = document.getElementById('entry_weight').value;
            const weightUnit = document.getElementById('entry_weightUnit').value;
            const height = document.getElementById('entry_height').value;
            const heightUnit = document.getElementById('entry_heightUnit').value;
            let goal = document.getElementById('entry_goal').value;
            const equipment = document.getElementById('entry_equipment').value;
            const cuisine = document.getElementById('entry_cuisine').value;
            const budget = document.getElementById('entry_budget').value;
            const currency = document.getElementById('entry_currency').value;
            const cookingSkill = document.getElementById('entry_cookingSkill').value;

            if (goal === 'Custom') {
                const customGoalVal = (document.getElementById('entry_custom_goal').value || '').trim();
                if (!customGoalVal) {
                    alert('⚠️ Please type your custom fitness target in the box!');
                    document.getElementById('entry_custom_goal').focus();
                    return;
                }
                goal = customGoalVal;
                syncToSidebar('custom_goal', customGoalVal);
            }

            if (!gender || !age || !weight || !height || !goal || !equipment || !cuisine || !budget || !currency || !cookingSkill) {
                alert('⚠️ Please fill in all information fields (Age, Weight, Height, Goal, Equipment, Cuisine, etc.) to generate your personalized plan!');
                return;
            }

            syncToSidebar('gender', gender);
            syncToSidebar('age', age);
            syncToSidebar('weight', weight);
            syncToSidebar('weightUnit', weightUnit);
            syncToSidebar('height', height);
            syncToSidebar('heightUnit', heightUnit);
            syncToSidebar('equipment', equipment);
            syncToSidebar('cuisine', cuisine);
            syncToSidebar('budget', budget);
            syncToSidebar('currency', currency);
            syncToSidebar('cookingSkill', cookingSkill);

            document.getElementById('studio-entry-view').style.display = 'none';
            document.getElementById('studio-dashboard-view').style.display = 'flex';
            
            generatePlan();
        }

        function switchPage(pageId) {
            document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active-page'));
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

            const targetPage = document.getElementById('page-' + pageId);
            const targetNav = document.getElementById('nav-' + pageId);

            if (targetPage) targetPage.classList.add('active-page');
            if (targetNav) {
                targetNav.classList.add('active');
                targetNav.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            }

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        async function generatePlan() {
            const gender = document.getElementById('gender').value;
            const age = document.getElementById('age').value;
            const weight = document.getElementById('weight').value;
            const weightUnit = document.getElementById('weightUnit').value;
            const height = document.getElementById('height').value;
            const heightUnit = document.getElementById('heightUnit').value;
            let goal = document.getElementById('goal').value;
            const equipment = document.getElementById('equipment').value;
            const cuisine = document.getElementById('cuisine').value;
            const budget = document.getElementById('budget').value;
            const currency = document.getElementById('currency').value;
            const cookingSkill = document.getElementById('cookingSkill').value;

            if (goal === 'Custom') {
                const customGoalVal = (document.getElementById('custom_goal').value || '').trim();
                if (!customGoalVal) {
                    alert('⚠️ Please type your custom fitness target!');
                    document.getElementById('custom_goal').focus();
                    return;
                }
                goal = customGoalVal;
            }

            if (!gender || !age || !weight || !height || !goal || !equipment || !cuisine || !budget || !currency || !cookingSkill) {
                alert('⚠️ Please provide all information in the sidebar controls to generate your plan.');
                return;
            }

            const btn = document.getElementById('generateBtn');
            const spinner = document.getElementById('spinner');
            const resultsArea = document.getElementById('resultsArea');
            const daysContainer = document.getElementById('daysContainer');
            const groceryCard = document.getElementById('groceryCard');
            const downloadBtn = document.getElementById('downloadBtn');

            btn.disabled = true;
            resultsArea.style.display = 'none';
            downloadBtn.style.display = 'none';
            spinner.style.display = 'block';

            const payload = {
                gender: gender,
                age: age,
                weight: weight,
                weight_unit: weightUnit,
                height: height,
                height_unit: heightUnit,
                goal: goal,
                equipment: equipment,
                cuisine: cuisine,
                budget: budget,
                currency: currency,
                cookingSkill: cookingSkill
            };

            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (!response.ok || data.error) {
                    alert(data.error || 'Failed to generate schedule.');
                } else {
                    currentRawPlan = data.raw || "";
                    daysContainer.innerHTML = '';
                    
                    data.days.forEach(day => {
                        const card = document.createElement('div');
                        card.className = 'schedule-card';
                        card.innerHTML = `
                            <div style="border-bottom: 1px solid var(--line); padding-bottom: 8px; margin-bottom: 14px;">
                                <h3 style="margin: 0; font-size: 1.35rem; color: var(--highlighter) !important;">🗓️ ${day.day.toUpperCase()}</h3>
                            </div>
                            <div class="schedule-card-inner" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                                <div class="workout-routine-box">
                                    <strong style="color: var(--coral) !important; display: block; margin-bottom: 8px; font-size: 0.95rem; letter-spacing: 0.5px;">🏋️ WORKOUT ROUTINE</strong>
                                    <div>${marked.parse(day.workout)}</div>
                                </div>
                                <div class="meal-routine-box">
                                    <strong style="color: var(--highlighter) !important; display: block; margin-bottom: 8px; font-size: 0.95rem; letter-spacing: 0.5px;">🥗 SYNCHRONIZED MEALS</strong>
                                    <div>${marked.parse(day.meal)}</div>
                                </div>
                            </div>
                        `;
                        daysContainer.appendChild(card);
                    });

                    groceryCard.innerHTML = marked.parse(data.grocery);
                    resultsArea.style.display = 'grid';
                    downloadBtn.style.display = 'inline-block';
                }
            } catch (err) {
                alert('Connection error: ' + err.message);
            } finally {
                spinner.style.display = 'none';
                btn.disabled = false;
            }
        }

        function downloadPDF() {
            if (!currentRawPlan) return;
            
            const element = document.createElement('div');
            element.style.padding = '25px 30px';
            element.style.background = '#ffffff';
            element.style.color = '#1e293b';
            element.style.fontFamily = 'Arial, sans-serif';
            
            const daysContainer = document.getElementById('daysContainer').cloneNode(true);
            const groceryCard = document.getElementById('groceryCard').cloneNode(true);
            
            element.innerHTML = `
                <div style="text-align: center; margin-bottom: 25px; border-bottom: 3px solid #ff416c; padding-bottom: 12px;">
                    <h1 style="color: #ff416c; margin: 0; font-size: 24px; font-weight: bold;">⚡ StudentFit AI — Weekly Fitness & Nutrition Plan</h1>
                    <p style="color: #64748b; font-size: 13px; margin-top: 4px;">Personalized for University Students | Workout Routines & Budget Grocery Plan</p>
                </div>
                <div style="margin-bottom: 30px;">
                    <h2 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; font-size: 17px; margin-bottom: 15px;">🗓️ 7-Day Workout & Synchronized Meal Schedule</h2>
                    ${daysContainer.innerHTML}
                </div>
                <div style="page-break-before: always; margin-top: 25px;">
                    <h2 style="color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; font-size: 17px; margin-bottom: 15px;">🛒 Weekly Student Grocery List & Budget</h2>
                    ${groceryCard.innerHTML}
                </div>
            `;

            const opt = {
                margin: [10, 10, 10, 10],
                filename: 'StudentFit_Weekly_Schedule.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2, useCORS: true },
                jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
            };

            html2pdf().set(opt).from(element).save();
        }

        // --- 3D PARTICLE & STARFIELD PARALLAX ENGINE ---
        (function init3DBackground() {
            const canvas = document.getElementById('bg-3d-canvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            let width = canvas.width = window.innerWidth;
            let height = canvas.height = window.innerHeight;

            let mouseX = width / 2;
            let mouseY = height / 2;
            let targetMouseX = mouseX;
            let targetMouseY = mouseY;
            let time = 0;

            const particles = [];
            const numParticles = Math.min(70, Math.floor(width / 20));
            const colors = ['#E4FF5B', '#FF6B54', '#9C8CFF', '#00E5FF'];

            for (let i = 0; i < numParticles; i++) {
                particles.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    z: Math.random() * 800 + 150,
                    size: Math.random() * 2 + 1.2,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    vx: (Math.random() - 0.5) * 0.35,
                    vy: (Math.random() - 0.5) * 0.35,
                    vz: Math.random() * 0.4 + 0.15
                });
            }

            window.addEventListener('resize', () => {
                width = canvas.width = window.innerWidth;
                height = canvas.height = window.innerHeight;
            });

            window.addEventListener('mousemove', (e) => {
                targetMouseX = e.clientX;
                targetMouseY = e.clientY;
            });

            window.addEventListener('touchmove', (e) => {
                if (e.touches && e.touches.length > 0) {
                    targetMouseX = e.touches[0].clientX;
                    targetMouseY = e.touches[0].clientY;
                }
            }, { passive: true });

            function render3D() {
                time += 0.012;
                const autoDriftX = Math.sin(time * 0.7) * 45;
                const autoDriftY = Math.cos(time * 0.5) * 30;

                mouseX += (targetMouseX - mouseX) * 0.05;
                mouseY += (targetMouseY - mouseY) * 0.05;
                const offsetX = (mouseX + autoDriftX - width / 2) * 0.06;
                const offsetY = (mouseY + autoDriftY - height / 2) * 0.06;

                ctx.clearRect(0, 0, width, height);

                for (let i = 0; i < particles.length; i++) {
                    const p = particles[i];
                    p.x += p.vx;
                    p.y += p.vy;
                    p.z -= p.vz;

                    if (p.z <= 50) p.z = 1000;
                    if (p.x < 0) p.x = width;
                    if (p.x > width) p.x = 0;
                    if (p.y < 0) p.y = height;
                    if (p.y > height) p.y = 0;

                    const fov = 420;
                    const scale = fov / p.z;
                    const projX = (p.x - width / 2 + offsetX * (1000 - p.z) * 0.0008) * scale + width / 2;
                    const projY = (p.y - height / 2 + offsetY * (1000 - p.z) * 0.0008) * scale + height / 2;
                    const radius = Math.max(0.6, p.size * scale);
                    const alpha = Math.min(1, (1000 - p.z) / 750) * 0.75;

                    ctx.beginPath();
                    ctx.arc(projX, projY, radius, 0, Math.PI * 2);
                    ctx.fillStyle = p.color;
                    ctx.globalAlpha = alpha;
                    ctx.shadowBlur = 12;
                    ctx.shadowColor = p.color;
                    ctx.fill();

                    for (let j = i + 1; j < particles.length; j++) {
                        const p2 = particles[j];
                        const dx = p.x - p2.x;
                        const dy = p.y - p2.y;
                        const dist = Math.sqrt(dx * dx + dy * dy);
                        if (dist < 130) {
                            const scale2 = fov / p2.z;
                            const projX2 = (p2.x - width / 2 + offsetX * (1000 - p2.z) * 0.0008) * scale2 + width / 2;
                            const projY2 = (p2.y - height / 2 + offsetY * (1000 - p2.z) * 0.0008) * scale2 + height / 2;

                            ctx.beginPath();
                            ctx.moveTo(projX, projY);
                            ctx.lineTo(projX2, projY2);
                            ctx.strokeStyle = p.color;
                            ctx.globalAlpha = (1 - dist / 130) * alpha * 0.25;
                            ctx.lineWidth = 0.9;
                            ctx.stroke();
                        }
                    }
                }

                requestAnimationFrame(render3D);
            }
            render3D();
        })();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json or {}
    api_key = get_api_key(data.get("apiKey"))
    use_demo = data.get("demoMode", False) or not api_key
    chosen_model = data.get("model", "openai/gpt-oss-20b")
    
    if use_demo:
        raw_text = generate_plan_mock(data)
        source = "Simulation (Demo Mode)"
    else:
        raw_text, used_model = generate_plan_real(data, api_key, chosen_model)
        source = f"Groq ({used_model})" if used_model else "Groq"

    if raw_text.startswith("Error:"):
        return jsonify({"error": raw_text}), 500

    days, grocery = parse_ai_response(raw_text)
    
    if not days:
        return jsonify({"error": "Failed to parse schedule format. Please retry."}), 500

    return jsonify({
        "days": days,
        "grocery": grocery,
        "raw": raw_text,
        "source": source
    })

@app.route("/api/macros", methods=["POST"])
def macros_endpoint():
    data = request.json or {}
    result = calculate_macros(
        age=data.get("age", 20),
        gender=data.get("gender", "Male"),
        weight=data.get("weight", 70),
        weight_unit=data.get("weight_unit", "kg"),
        height=data.get("height", 170),
        height_unit=data.get("height_unit", "cm"),
        goal=data.get("goal", "Build Muscle")
    )
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
