import os
import sys
from flask import Flask, render_template_string, request, jsonify

# Ensure local directory is in Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from planner.llm_client import (
    get_api_key,
    calculate_macros,
    parse_ai_response,
    generate_plan_mock,
    generate_plan_real,
    CANDIDATE_MODELS
)

app = Flask(__name__)

# --- COMPLETE MULTI-PAGE STREAMLIT DESIGN SYSTEM APPLIED TO VERCEL ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudentFit AI — Fitness that syncs to your syllabus</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Space+Grotesk:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
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
            --line: rgba(246, 241, 227, 0.14);
            --radius: 20px;
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
            background-color: var(--ink);
            color: var(--paper);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* ULTRA-THIN TRANSPARENT SCROLLBAR */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(246, 241, 227, 0.2); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--highlighter); }

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

        /* TOP NAVIGATION BAR (PLANNER TABS) */
        .navbar {
            background: rgba(20, 19, 43, 0.92);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--line);
            padding: 14px 36px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .brand-logo {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--paper);
            cursor: pointer;
            letter-spacing: -0.5px;
        }

        .brand-logo span { color: var(--highlighter); }

        .nav-links {
            display: flex;
            gap: 10px;
            align-items: center;
            list-style: none;
        }

        .nav-link {
            font-family: 'Space Mono', monospace;
            font-size: 0.86rem;
            color: var(--text-soft);
            text-decoration: none;
            font-weight: 600;
            padding: 8px 14px;
            border-radius: 12px;
            transition: all 0.2s ease;
            cursor: pointer;
            border: 1px solid transparent;
        }

        .nav-link:hover {
            color: var(--paper);
            background: rgba(246, 241, 227, 0.06);
        }

        .nav-link.active {
            color: var(--highlighter);
            background: rgba(228, 255, 91, 0.12);
            border-color: rgba(228, 255, 91, 0.35);
        }

        .nav-cta {
            background: var(--coral);
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 12px;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.25s ease;
            box-shadow: 0 4px 15px rgba(255, 107, 84, 0.35);
        }

        .nav-cta:hover {
            background: #ff5238;
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 84, 0.6);
        }

        /* PAGE VIEW CONTAINERS */
        .page-view {
            display: none;
            flex: 1;
            width: 100%;
            position: relative;
            z-index: 1;
            animation: fadeIn 0.35s ease forwards;
        }

        .page-view.active-page { display: block; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* TYPOGRAPHY */
        h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif; font-weight: 700; letter-spacing: -0.5px; }
        .eyebrow { font-family: 'Caveat', cursive; font-size: 1.55rem; color: var(--highlighter); transform: rotate(-2deg); display: inline-block; margin-bottom: 8px; }
        .mono-stat { font-family: 'Space Mono', monospace; font-size: 0.82rem; color: var(--text-soft); text-transform: uppercase; letter-spacing: 0.5px; }

        /* CARDS */
        .card-dark {
            background: var(--ink2);
            border: 1px solid var(--line);
            border-radius: var(--radius);
            padding: 26px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .card-dark:hover {
            border-color: rgba(228, 255, 91, 0.4);
            transform: translateY(-4px);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.4);
        }

        .card-paper {
            background: var(--paper);
            color: #14132B;
            border-radius: var(--radius);
            padding: 24px;
            border: 1px solid rgba(0, 0, 0, 0.08);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
            transition: all 0.3s ease;
        }

        .card-paper h3, .card-paper h4, .card-paper strong { color: #14132B; }
        .card-paper p { color: #334155; }
        .card-paper:hover { transform: translateY(-3px); box-shadow: 0 16px 40px rgba(0, 0, 0, 0.35); }

        /* HERO FANNED 7-CARD DECK */
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

        .marquee-item span { color: var(--highlighter); margin-right: 8px; }

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

        .flip-card { background-color: transparent; height: 220px; perspective: 1000px; }
        .flip-card-inner { position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.6s cubic-bezier(0.4, 0.2, 0.2, 1); transform-style: preserve-3d; border-radius: var(--radius); }
        .flip-card:hover .flip-card-inner { transform: rotateY(180deg); }
        .flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; -webkit-backface-visibility: hidden; backface-visibility: hidden; border-radius: var(--radius); padding: 24px; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .flip-card-front { background: var(--ink2); border: 1px solid var(--line); color: var(--paper); }
        .flip-card-back { background: var(--paper); color: var(--ink); transform: rotateY(180deg); border: 1px solid var(--highlighter); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3); }
        .flip-card-back p { color: #14132B; font-size: 0.95rem; font-weight: 600; line-height: 1.5; }

        /* BUTTONS */
        .btn-coral {
            background: var(--coral);
            color: #ffffff;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            border: none;
            border-radius: 14px;
            padding: 14px 28px;
            cursor: pointer;
            transition: all 0.25s ease;
            box-shadow: 0 4px 18px rgba(255, 107, 84, 0.35);
        }

        .btn-coral:hover {
            background: #ff5238;
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(255, 107, 84, 0.6);
        }

        .btn-secondary {
            background: rgba(246, 241, 227, 0.08);
            color: var(--paper);
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            border: 1px solid var(--line);
            border-radius: 14px;
            padding: 14px 26px;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-secondary:hover {
            background: rgba(246, 241, 227, 0.15);
            border-color: var(--highlighter);
        }

        /* GENERATOR STUDIO STYLES */
        .studio-container { display: flex; width: 100%; flex: 1; }
        .studio-sidebar { width: 360px; background: var(--ink2); border-right: 1px solid var(--line); padding: 26px 22px; overflow-y: auto; max-height: calc(100vh - 72px); position: sticky; top: 72px; }
        .studio-main { flex: 1; padding: 30px 38px; overflow-y: auto; }
        .form-group { margin-bottom: 13px; }
        .form-row { display: flex; gap: 10px; }
        .form-row .form-group { flex: 1; }
        label { display: block; font-size: 0.82rem; color: var(--text-soft); margin-bottom: 4px; font-weight: 600; }
        input, select { width: 100%; background: var(--ink3); border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; color: var(--paper); font-size: 0.9rem; outline: none; }
        input:focus, select:focus { border-color: var(--highlighter); }
        select option { background: var(--ink2); color: var(--paper); }

        .spinner-container { display: none; text-align: center; padding: 60px; }
        .spinner { width: 50px; height: 50px; border: 4px solid rgba(246, 241, 227, 0.1); border-top-color: var(--highlighter); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px auto; }
        @keyframes spin { to { transform: rotate(360deg); } }

        @media (max-width: 900px) {
            .navbar { padding: 14px 20px; }
            .nav-links { display: none; }
            .studio-container { flex-direction: column; }
            .studio-sidebar { width: 100%; position: relative; top: 0; max-height: none; }
        }
    </style>
</head>
<body>
    <div class="ambient-bg">
        <div class="blob-1"></div>
        <div class="blob-2"></div>
    </div>

    <!-- TOP NAVIGATION BAR (PLANNER TABS) -->
    <nav class="navbar">
        <a class="brand-logo" onclick="switchPage('home')">
            ⚡ <span>StudentFit AI</span>
        </a>
        <ul class="nav-links">
            <li><a class="nav-link active" id="nav-home" onclick="switchPage('home')">🏠 Home</a></li>
            <li><a class="nav-link" id="nav-how" onclick="switchPage('how')">📖 How it Works</a></li>
            <li><a class="nav-link" id="nav-features" onclick="switchPage('features')">⚡ Features</a></li>
            <li><a class="nav-link" id="nav-plans" onclick="switchPage('plans')">💳 Plans</a></li>
            <li><a class="nav-link" id="nav-story" onclick="switchPage('story')">🎓 Story</a></li>
            <li><a class="nav-link" id="nav-generator" onclick="switchPage('generator')">🚀 Plan Generator</a></li>
        </ul>
        <button class="nav-cta" onclick="switchPage('generator')">🚀 Generate Plan</button>
    </nav>

    <!-- =========================================================================
         PAGE 1: HOME
         ========================================================================= -->
    <div class="page-view active-page" id="page-home">
        <div style="max-width: 1180px; margin: 50px auto 70px auto; padding: 0 30px;">
            <div class="eyebrow">built between lectures & leftovers</div>
            <h1 style="font-size: 3.4rem; line-height: 1.15; margin-bottom: 20px; max-width: 840px;">
                Fitness that syncs to your syllabus.
            </h1>
            <p style="font-size: 1.15rem; color: var(--text-soft); line-height: 1.6; max-width: 700px; margin-bottom: 30px;">
                Most fitness apps assume a full kitchen, a car, and free time. StudentFit AI plans around what students actually have: dorm-room floor space, a realistic grocery budget, quick cooking, and an exam schedule that can't be ignored.
            </p>

            <div style="display: flex; gap: 16px; margin-bottom: 30px;">
                <button class="btn-coral" onclick="switchPage('generator')">🚀 Generate My Week</button>
                <button class="btn-secondary" onclick="switchPage('how')">📖 See how it works</button>
            </div>

            <!-- HERO FANNED 7-CARD DECK -->
            <div class="hero-deck-container">
                <div class="deck-card" style="left: calc(50% - 330px); transform: rotate(-15deg) translateY(20px); z-index: 1;">
                    <div class="deck-day">Mon</div>
                    <div class="deck-emoji">🏋️</div>
                    <div class="deck-tag">Push Day & Oats</div>
                </div>
                <div class="deck-card" style="left: calc(50% - 220px); transform: rotate(-10deg) translateY(10px); z-index: 2;">
                    <div class="deck-day">Tue</div>
                    <div class="deck-emoji">💪</div>
                    <div class="deck-tag">Pull & Dal Rice</div>
                </div>
                <div class="deck-card" style="left: calc(50% - 110px); transform: rotate(-5deg) translateY(4px); z-index: 3;">
                    <div class="deck-day">Wed</div>
                    <div class="deck-emoji">🧘</div>
                    <div class="deck-tag">Exam De-Stress</div>
                </div>
                <div class="deck-card" style="left: calc(50% - 0px); transform: rotate(0deg) translateY(0px); z-index: 4; border: 2px solid var(--highlighter);">
                    <div class="deck-day" style="color: var(--coral);">Thu</div>
                    <div class="deck-emoji">⚡</div>
                    <div class="deck-tag">Legs & Protein Wrap</div>
                </div>
                <div class="deck-card" style="left: calc(50% + 110px); transform: rotate(5deg) translateY(4px); z-index: 3;">
                    <div class="deck-day">Fri</div>
                    <div class="deck-emoji">🔥</div>
                    <div class="deck-tag">Shoulders & Abs</div>
                </div>
                <div class="deck-card" style="left: calc(50% + 220px); transform: rotate(10deg) translateY(10px); z-index: 2;">
                    <div class="deck-day">Sat</div>
                    <div class="deck-emoji">🥊</div>
                    <div class="deck-tag">Power Circuit</div>
                </div>
                <div class="deck-card" style="left: calc(50% + 330px); transform: rotate(15deg) translateY(20px); z-index: 1;">
                    <div class="deck-day">Sun</div>
                    <div class="deck-emoji">🛒</div>
                    <div class="deck-tag">Batch Meal Prep</div>
                </div>
            </div>

            <!-- SCROLLING STAT TICKER -->
            <div class="marquee-container">
                <div class="marquee-track">
                    <div class="marquee-item"><span>⚡</span> 4 FITNESS GOALS</div>
                    <div class="marquee-item"><span>🏋️</span> 3 GEAR TIERS</div>
                    <div class="marquee-item"><span>🥑</span> 5 CUISINES</div>
                    <div class="marquee-item"><span>💰</span> 3 BUDGET TIERS</div>
                    <div class="marquee-item"><span>🍳</span> 3 COOKING SKILL LEVELS</div>
                    <div class="marquee-item"><span>🗓️</span> 7 DAYS SYNCED</div>
                    <div class="marquee-item"><span>⚡</span> 4 FITNESS GOALS</div>
                    <div class="marquee-item"><span>🏋️</span> 3 GEAR TIERS</div>
                    <div class="marquee-item"><span>🥑</span> 5 CUISINES</div>
                    <div class="marquee-item"><span>💰</span> 3 BUDGET TIERS</div>
                    <div class="marquee-item"><span>🍳</span> 3 COOKING SKILL LEVELS</div>
                    <div class="marquee-item"><span>🗓️</span> 7 DAYS SYNCED</div>
                </div>
            </div>

            <!-- BUILT FOR DORM ROOMS -->
            <div style="text-align: center; margin: 60px 0 30px 0;">
                <h2 style="font-size: 2.2rem;">Built for dorm rooms, not gym floors</h2>
                <p style="color: var(--text-soft); font-size: 1rem;">Fitness programming designed around campus real estate, tight schedules, and shared kitchens.</p>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-bottom: 60px;">
                <div class="card-dark">
                    <div style="font-size: 2.2rem; margin-bottom: 12px;">🏠</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">No Gym Required</h3>
                    <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.5;">Get serious training volume with zero equipment on dorm floors, light dumbbells, or campus facilities.</p>
                </div>
                <div class="card-dark">
                    <div style="font-size: 2.2rem; margin-bottom: 12px;">💰</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Budget-Respected</h3>
                    <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.5;">Every meal plan outputs 1-person weekly grocery lists and localized cost estimates in your currency.</p>
                </div>
                <div class="card-dark">
                    <div style="font-size: 2.2rem; margin-bottom: 12px;">🧠</div>
                    <h3 style="font-size: 1.25rem; margin-bottom: 8px;">Exam-Week-Aware</h3>
                    <p style="color: var(--text-soft); font-size: 0.92rem; line-height: 1.5;">"Exam Stress Relief" is a first-class fitness target, balancing active recovery, mental clarity, and quick-fuel nutrition.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- =========================================================================
         PAGE 2: HOW IT WORKS
         ========================================================================= -->
    <div class="page-view" id="page-how">
        <div style="max-width: 960px; margin: 50px auto 70px auto; padding: 0 30px;">
            <div class="eyebrow">simple, transparent, structured</div>
            <h1 style="font-size: 2.8rem; margin-bottom: 14px;">How StudentFit AI Works</h1>
            <p style="font-size: 1.1rem; color: var(--text-soft); margin-bottom: 35px;">
                Every weekly schedule is dynamically generated across three student lifestyle dimensions.
            </p>

            <div class="card-dark" style="margin-bottom: 24px;">
                <h3 style="font-size: 1.3rem; margin-bottom: 6px; color: var(--coral);">01 · Campus Bio-Data Configuration</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.5; margin-bottom: 10px;">Calculates metabolic energy baselines (BMR) and recommended hydration tailored to campus routines.</p>
                <div class="mono-stat">Options: Gender (Male/Female/Other) · Age (16–40) · Weight (kg/lbs) · Height (cm/ft)</div>
            </div>

            <div class="card-dark" style="margin-bottom: 24px;">
                <h3 style="font-size: 1.3rem; margin-bottom: 6px; color: var(--coral);">02 · Goals & Equipment Adaptability</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.5; margin-bottom: 10px;">Translates available gear into high-efficiency compound movements and progressive overload.</p>
                <div class="mono-stat">Options: Build Muscle · Lose Weight · Get Shredded · Exam Stress Relief | Full Gym · Dumbbells Only · Dorm Floor</div>
            </div>

            <div class="card-dark" style="margin-bottom: 24px;">
                <h3 style="font-size: 1.3rem; margin-bottom: 6px; color: var(--coral);">03 · Kitchen Setup, Cuisine & Local Currency</h3>
                <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.5; margin-bottom: 10px;">Aligns calorie and protein goals with realistic college cooking facilities, bulk staples, and student budgets.</p>
                <div class="mono-stat">Options: Indian · Global · Mediterranean · Asian · Vegan | Cheap · Moderate · Premium | Microwave · Basic Stove · Chef</div>
            </div>

            <button class="btn-coral" style="margin-top: 15px;" onclick="switchPage('generator')">🚀 Try the Generator Now</button>
        </div>
    </div>

    <!-- =========================================================================
         PAGE 3: FEATURES
         ========================================================================= -->
    <div class="page-view" id="page-features">
        <div style="max-width: 1100px; margin: 50px auto 70px auto; padding: 0 30px;">
            <div class="eyebrow">interactive 3d feature matrix</div>
            <h1 style="font-size: 2.8rem; margin-bottom: 14px;">Six Adaptive Dimensions</h1>
            <p style="font-size: 1.1rem; color: var(--text-soft); margin-bottom: 30px;">
                Hover any card to reveal how StudentFit AI customizes your weekly schedule across all 6 core axes.
            </p>

            <div class="flip-grid">
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
        </div>
    </div>

    <!-- =========================================================================
         PAGE 4: PLANS
         ========================================================================= -->
    <div class="page-view" id="page-plans">
        <div style="max-width: 1100px; margin: 50px auto 70px auto; padding: 0 30px;">
            <div class="eyebrow">transparent concept tiers</div>
            <h1 style="font-size: 2.8rem; margin-bottom: 14px;">Budget-Tiered Student Plans</h1>
            <p style="font-size: 1.1rem; color: var(--text-soft); margin-bottom: 35px;">
                Named directly after the app's own budget tiers. Free live access with zero paywalls.
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">
                <div class="card-dark">
                    <div class="mono-stat">TIER 01 · FREE FOREVER</div>
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
                <div class="card-paper" style="border: 2px solid var(--coral);">
                    <div class="mono-stat" style="color: var(--coral);">TIER 02 · MOST POPULAR</div>
                    <h2 style="font-size: 1.8rem; margin: 10px 0 4px 0; color: #14132B;">Moderate ($$)</h2>
                    <div style="font-size: 2rem; font-weight: 700; color: var(--coral); margin-bottom: 16px;">$5 <span style="font-size: 0.9rem; color: #475569;">/ semester</span></div>
                    <ul style="list-style: none; padding-left: 0; font-size: 0.92rem; color: #334155; line-height: 1.8;">
                        <li>✓ Everything in Cheap ($)</li>
                        <li>✓ Exam Stress Relief Adaptive Splits</li>
                        <li>✓ 5 Cuisines & Macro-Calculators</li>
                        <li>✓ Multi-Currency Budget Breakdown</li>
                        <li>✓ Sunday Batch-Prep Blueprints</li>
                    </ul>
                </div>
                <div class="card-dark">
                    <div class="mono-stat">TIER 03 · CAMPUS SQUAD</div>
                    <h2 style="font-size: 1.8rem; margin: 10px 0 4px 0;">Premium ($$$)</h2>
                    <div style="font-size: 2rem; font-weight: 700; color: var(--lilac); margin-bottom: 16px;">$12 <span style="font-size: 0.9rem; color: var(--text-soft);">/ flat of 4</span></div>
                    <ul style="list-style: none; padding-left: 0; font-size: 0.92rem; color: var(--text-soft); line-height: 1.8;">
                        <li>✓ Shared Flat Grocery Consolidation</li>
                        <li>✓ Bulk Meal Prep Sync for Roommates</li>
                        <li>✓ University Gym Progression Logs</li>
                        <li>✓ High-Speed Priority AI Neural Queue</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>

    <!-- =========================================================================
         PAGE 5: STORY
         ========================================================================= -->
    <div class="page-view" id="page-story">
        <div style="max-width: 960px; margin: 50px auto 70px auto; padding: 0 30px;">
            <div class="eyebrow">the student perspective</div>
            <h1 style="font-size: 2.8rem; margin-bottom: 14px;">Why We Built StudentFit AI</h1>
            <p style="font-size: 1.15rem; color: var(--text-soft); margin-bottom: 35px;">
                Mainstream fitness media is built for people with cars, gourmet kitchens, $150 gym memberships, and hours of daily free time. We built StudentFit AI for reality.
            </p>

            <div class="card-dark" style="margin-bottom: 24px;">
                <h3 style="color: var(--highlighter); font-size: 1.35rem; margin-bottom: 8px;">Built for Campus Life, Not Gym Culture</h3>
                <p style="color: var(--paper); font-size: 0.95rem; line-height: 1.6;">
                    When you're balancing semester exams, 8:00 AM lectures, and part-time jobs, spending 2 hours in a commercial gym or cooking elaborate 4-course macros is impossible.
                </p>
                <p style="color: var(--text-soft); font-size: 0.95rem; line-height: 1.6; margin-top: 10px;">
                    StudentFit AI treats your tight budget, small dorm floor, single microwave, and exam weeks as primary constraints, generating high-yield 7-day routines that actually fit your student schedule.
                </p>
            </div>
        </div>
    </div>

    <!-- =========================================================================
         PAGE 6: GENERATOR (PLANNER STUDIO — WIZARD -> SIDEBAR DASHBOARD)
         ========================================================================= -->
    <div class="page-view" id="page-generator">
        <!-- 1. ENTRY SETUP WIZARD (FIRST TIME VIEW) -->
        <div id="studio-entry-view" style="max-width: 920px; margin: 40px auto 80px auto; padding: 0 20px;">
            <div class="card-dark" style="background: rgba(13, 10, 32, 0.9); border: 1px solid rgba(0, 229, 255, 0.35); box-shadow: 0 20px 60px rgba(0,0,0,0.6); padding: 40px; border-radius: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <div class="eyebrow" style="margin-bottom: 4px;">⚡ step 1 of 1 — personalize your week</div>
                    <h2 style="font-size: 2.2rem; font-weight: 800; color: #fff; margin: 8px 0;">Student Fit Profile Setup</h2>
                    <p style="color: var(--text-soft); font-size: 1rem;">Configure your campus fitness constraints once. Your customized 7-day schedule & budget grocery list will generate instantly.</p>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
                    <!-- BIO DATA -->
                    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px;">
                        <h4 style="color: var(--neon-cyan); margin-bottom: 14px; font-size: 1.05rem;">🏃‍♂️ Campus Bio-Data</h4>
                        <div class="form-row">
                            <div class="form-group">
                                <label>Gender</label>
                                <select id="entry_gender" onchange="syncToSidebar('gender', this.value)">
                                    <option value="Male" selected>Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Age</label>
                                <input type="number" id="entry_age" value="20" min="16" max="40" onchange="syncToSidebar('age', this.value)">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group" style="flex: 2;">
                                <label>Weight</label>
                                <input type="number" id="entry_weight" value="70" min="30" max="300" onchange="syncToSidebar('weight', this.value)">
                            </div>
                            <div class="form-group" style="flex: 1.2;">
                                <label>Unit</label>
                                <select id="entry_weightUnit" onchange="syncToSidebar('weightUnit', this.value)">
                                    <option value="kg" selected>kg</option>
                                    <option value="lbs">lbs</option>
                                </select>
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-group" style="flex: 2;">
                                <label>Height</label>
                                <input type="number" id="entry_height" value="170" min="100" max="250" onchange="syncToSidebar('height', this.value)">
                            </div>
                            <div class="form-group" style="flex: 1.2;">
                                <label>Unit</label>
                                <select id="entry_heightUnit" onchange="syncToSidebar('heightUnit', this.value)">
                                    <option value="cm" selected>cm</option>
                                    <option value="ft/in">ft/in</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- GOALS & GEAR -->
                    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px;">
                        <h4 style="color: var(--neon-gold); margin-bottom: 14px; font-size: 1.05rem;">🎯 Goals & Gear</h4>
                        <div class="form-group">
                            <label>Primary Fitness Target</label>
                            <select id="entry_goal" onchange="syncToSidebar('goal', this.value)">
                                <option value="Build Muscle" selected>💪 Build Muscle & Bulk</option>
                                <option value="Lose Weight">🔥 Lose Fat & Lean Out</option>
                                <option value="Get Shredded">⚡ Athletic Tone & Shred</option>
                                <option value="Exam Stress Relief">🧘 Exam Stress Relief & Focus</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Available Equipment</label>
                            <select id="entry_equipment" onchange="syncToSidebar('equipment', this.value)">
                                <option value="Full Gym" selected>🏛️ Full University Gym</option>
                                <option value="Dumbbells Only">🏋️ Dumbbells Only</option>
                                <option value="No Equipment (Dorm)">🏠 No Equipment (Dorm Floor)</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div style="margin-top: 24px; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 20px;">
                    <h4 style="color: var(--coral); margin-bottom: 14px; font-size: 1.05rem;">🥑 Kitchen, Cuisine & Local Currency</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px;">
                        <div class="form-group">
                            <label>Cuisine Preference</label>
                            <select id="entry_cuisine" onchange="syncToSidebar('cuisine', this.value)">
                                <option value="Indian" selected>🍛 Indian</option>
                                <option value="Global">🌍 Global</option>
                                <option value="Mediterranean">🥗 Mediterranean</option>
                                <option value="Asian">🥢 Asian</option>
                                <option value="Vegan">🌱 Vegan</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Budget Tier</label>
                            <select id="entry_budget" onchange="syncToSidebar('budget', this.value)">
                                <option value="Cheap ($)">Cheap ($)</option>
                                <option value="Moderate ($$)" selected>Moderate ($$)</option>
                                <option value="Premium ($$$)">Premium ($$$)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Preferred Currency</label>
                            <select id="entry_currency" onchange="syncToSidebar('currency', this.value)">
                                <option value="INR (₹)" selected>INR (₹) - Rupee</option>
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
                        <select id="entry_cookingSkill" onchange="syncToSidebar('cookingSkill', this.value)">
                            <option value="Microwave Only">⚡ Microwave / Kettle Only (Strict Dorm)</option>
                            <option value="Basic Stove" selected>🍳 Basic Stove / Single Induction</option>
                            <option value="Full Chef">👨‍🍳 Full Kitchen & Oven</option>
                        </select>
                    </div>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <button class="btn-coral" style="width: 100%; max-width: 480px; font-size: 1.15rem;" onclick="submitEntryAndGenerate()">
                        🚀 GENERATE 7-DAY SCHEDULE & GROCERIES
                    </button>
                </div>
            </div>
        </div>

        <!-- 2. STUDIO DASHBOARD VIEW (ACTIVATED AFTER GENERATING, WITH EDITABLE SIDEBAR) -->
        <div id="studio-dashboard-view" class="studio-container" style="display: none;">
            <!-- SIDEBAR -->
            <aside class="studio-sidebar">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h2 style="font-size: 1.3rem; color: var(--paper);">⚡ Studio Controls</h2>
                    <button onclick="showWizardEntry()" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2); color: var(--neon-cyan); border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; cursor: pointer;">✏️ Full View</button>
                </div>

                <div class="mono-stat" style="color: var(--neon-gold); margin-bottom: 8px;">🏃‍♂️ BIO-DATA</div>
                <div class="form-row">
                    <div class="form-group">
                        <label>Gender</label>
                        <select id="gender">
                            <option value="Male" selected>Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Age</label>
                        <input type="number" id="age" value="20" min="16" max="40">
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group" style="flex: 2;">
                        <label>Weight</label>
                        <input type="number" id="weight" value="70" min="30" max="300">
                    </div>
                    <div class="form-group" style="flex: 1.2;">
                        <label>Unit</label>
                        <select id="weightUnit">
                            <option value="kg" selected>kg</option>
                            <option value="lbs">lbs</option>
                        </select>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group" style="flex: 2;">
                        <label>Height</label>
                        <input type="number" id="height" value="170" min="100" max="250">
                    </div>
                    <div class="form-group" style="flex: 1.2;">
                        <label>Unit</label>
                        <select id="heightUnit">
                            <option value="cm" selected>cm</option>
                            <option value="ft/in">ft/in</option>
                        </select>
                    </div>
                </div>

                <div class="mono-stat" style="color: var(--neon-cyan); margin: 16px 0 8px 0;">🎯 GOALS & GEAR</div>
                <div class="form-group">
                    <label>Fitness Target</label>
                    <select id="goal">
                        <option value="Build Muscle" selected>Build Muscle</option>
                        <option value="Lose Weight">Lose Weight</option>
                        <option value="Get Shredded">Get Shredded</option>
                        <option value="Exam Stress Relief">Exam Stress Relief</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>Available Equipment</label>
                    <select id="equipment">
                        <option value="Full Gym" selected>Full Gym</option>
                        <option value="Dumbbells Only">Dumbbells Only</option>
                        <option value="No Equipment (Dorm)">No Equipment (Dorm)</option>
                    </select>
                </div>

                <div class="mono-stat" style="color: var(--coral); margin: 16px 0 8px 0;">🥑 KITCHEN & BUDGET</div>
                <div class="form-group">
                    <label>Cuisine Preference</label>
                    <select id="cuisine">
                        <option value="Indian" selected>Indian</option>
                        <option value="Global">Global</option>
                        <option value="Mediterranean">Mediterranean</option>
                        <option value="Asian">Asian</option>
                        <option value="Vegan">Vegan</option>
                    </select>
                </div>

                <div class="form-row">
                    <div class="form-group" style="flex: 1.5;">
                        <label>Budget Tier</label>
                        <select id="budget">
                            <option value="Cheap ($)">Cheap ($)</option>
                            <option value="Moderate ($$)" selected>Moderate ($$)</option>
                            <option value="Premium ($$$)">Premium ($$$)</option>
                        </select>
                    </div>
                    <div class="form-group" style="flex: 1.5;">
                        <label>Currency</label>
                        <select id="currency">
                            <option value="INR (₹)" selected>INR (₹)</option>
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
                    <select id="cookingSkill">
                        <option value="Microwave Only">Microwave Only</option>
                        <option value="Basic Stove" selected>Basic Stove</option>
                        <option value="Full Chef">Full Chef</option>
                    </select>
                </div>

                <button class="btn-coral" style="width: 100%; margin-top: 15px;" id="generateBtn" onclick="generatePlan()">🔄 RE-GENERATE PLAN</button>
            </aside>

            <!-- MAIN WORKSPACE -->
            <main class="studio-main">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
                    <div>
                        <div class="eyebrow">interactive planner studio</div>
                        <h1 style="font-size: 2.2rem; color: var(--paper);">Weekly Plan Generator</h1>
                    </div>
                    <button id="downloadBtn" class="btn-secondary" style="display: none;" onclick="downloadPDF()">📥 Save Plan (PDF)</button>
                </div>

                <div id="spinner" class="spinner-container">
                    <div class="spinner"></div>
                    <h3 style="color: var(--highlighter); margin-bottom: 6px;">🗓️ Synchronizing your 7-day schedule with AI...</h3>
                    <p style="color: var(--text-soft);">Tailoring exercises, student meals, and localized grocery budgets...</p>
                </div>

                <div id="placeholder" class="card-dark" style="text-align: center; padding: 60px 20px;">
                    <div style="font-size: 2.2rem; margin-bottom: 10px;">👈</div>
                    <h3>Configure in the Sidebar</h3>
                    <p style="color: var(--text-soft); margin-top: 6px;">Set your campus bio-data, gear, and budget in the left sidebar and click <strong>"RE-GENERATE PLAN"</strong>.</p>
                </div>

                <div id="resultsArea" style="display: none; grid-template-columns: 2.4fr 1.2fr; gap: 24px;">
                    <div id="daysContainer"></div>
                    <div class="card-paper" id="groceryCard" style="height: fit-content; position: sticky; top: 90px;"></div>
                </div>
            </main>
        </div>
    </div>

    <script>
        let currentRawPlan = "";

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
            // Synchronize all fields from entry to sidebar
            syncToSidebar('gender', document.getElementById('entry_gender').value);
            syncToSidebar('age', document.getElementById('entry_age').value);
            syncToSidebar('weight', document.getElementById('entry_weight').value);
            syncToSidebar('weightUnit', document.getElementById('entry_weightUnit').value);
            syncToSidebar('height', document.getElementById('entry_height').value);
            syncToSidebar('heightUnit', document.getElementById('entry_heightUnit').value);
            syncToSidebar('goal', document.getElementById('entry_goal').value);
            syncToSidebar('equipment', document.getElementById('entry_equipment').value);
            syncToSidebar('cuisine', document.getElementById('entry_cuisine').value);
            syncToSidebar('budget', document.getElementById('entry_budget').value);
            syncToSidebar('currency', document.getElementById('entry_currency').value);
            syncToSidebar('cookingSkill', document.getElementById('entry_cookingSkill').value);

            // Hide entry view and show studio dashboard view
            document.getElementById('studio-entry-view').style.display = 'none';
            document.getElementById('studio-dashboard-view').style.display = 'flex';
            
            // Trigger generation
            generatePlan();
        }

        function switchPage(pageId) {
            document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active-page'));
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

            const targetPage = document.getElementById('page-' + pageId);
            const targetNav = document.getElementById('nav-' + pageId);

            if (targetPage) targetPage.classList.add('active-page');
            if (targetNav) targetNav.classList.add('active');

            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        async function generatePlan() {
            const btn = document.getElementById('generateBtn');
            const spinner = document.getElementById('spinner');
            const placeholder = document.getElementById('placeholder');
            const resultsArea = document.getElementById('resultsArea');
            const daysContainer = document.getElementById('daysContainer');
            const groceryCard = document.getElementById('groceryCard');
            const downloadBtn = document.getElementById('downloadBtn');

            btn.disabled = true;
            placeholder.style.display = 'none';
            resultsArea.style.display = 'none';
            downloadBtn.style.display = 'none';
            spinner.style.display = 'block';

            const payload = {
                gender: document.getElementById('gender').value,
                age: document.getElementById('age').value,
                weight: document.getElementById('weight').value,
                weight_unit: document.getElementById('weightUnit').value,
                height: document.getElementById('height').value,
                height_unit: document.getElementById('heightUnit').value,
                goal: document.getElementById('goal').value,
                equipment: document.getElementById('equipment').value,
                cuisine: document.getElementById('cuisine').value,
                budget: document.getElementById('budget').value,
                currency: document.getElementById('currency').value,
                cooking_skill: document.getElementById('cookingSkill').value
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
                    placeholder.style.display = 'block';
                } else {
                    currentRawPlan = data.raw || "";
                    daysContainer.innerHTML = '';
                    
                    data.days.forEach(day => {
                        const card = document.createElement('div');
                        card.className = 'card-paper';
                        card.style.marginBottom = '20px';
                        card.innerHTML = `
                            <h3 style="font-size: 1.3rem; border-bottom: 1px solid rgba(0,0,0,0.12); padding-bottom: 6px; margin-bottom: 14px;">
                                🗓️ ${day.day}
                            </h3>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                                <div style="background: rgba(0,0,0,0.04); padding: 12px; border-radius: 10px;">
                                    <div class="mono-stat" style="color: var(--coral); margin-bottom: 6px;">🏋️ WORKOUT ROUTINE</div>
                                    <div style="font-size: 0.9rem; line-height: 1.5; color: #1e293b;">${marked.parse(day.workout)}</div>
                                </div>
                                <div style="background: rgba(0,0,0,0.04); padding: 12px; border-radius: 10px;">
                                    <div class="mono-stat" style="color: #b45309; margin-bottom: 6px;">🥗 SYNCHRONIZED MEALS</div>
                                    <div style="font-size: 0.9rem; line-height: 1.5; color: #1e293b;">${marked.parse(day.meal)}</div>
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
                placeholder.style.display = 'block';
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
                <div style="text-align: center; margin-bottom: 25px; border-bottom: 3px solid #FF6B54; padding-bottom: 12px;">
                    <h1 style="color: #FF6B54; margin: 0; font-size: 24px; font-weight: bold;">⚡ StudentFit AI — Weekly Fitness & Nutrition Plan</h1>
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
