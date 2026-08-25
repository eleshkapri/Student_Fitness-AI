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
    CANDIDATE_MODELS
)

app = Flask(__name__)

# --- COMPLETE MULTI-PAGE 3D ANIMATED MODERN WEB INTERFACE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudentFit AI ⚡ | The #1 Student Fitness & Nutrition Platform</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #09071c 0%, #17133d 50%, #15112e 100%);
            --card-bg: rgba(255, 255, 255, 0.04);
            --card-border: rgba(255, 255, 255, 0.1);
            --neon-cyan: #00e5ff;
            --neon-gold: #FFD700;
            --neon-pink: #ff416c;
            --neon-orange: #ff4b2b;
            --text-primary: #ffffff;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            scrollbar-width: thin;
            scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
        }

        body {
            background: var(--bg-gradient);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* ULTRA-THIN TRANSPARENT SCROLLBAR */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.18); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0, 229, 255, 0.6); }

        /* TOP NAVIGATION BAR */
        .navbar {
            background: rgba(13, 10, 32, 0.85);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 16px 36px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .brand-logo {
            font-size: 1.45rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: #fff;
            cursor: pointer;
            letter-spacing: -0.5px;
        }

        .brand-logo span {
            background: linear-gradient(90deg, #ffffff, #00e5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .nav-links {
            display: flex;
            gap: 28px;
            align-items: center;
            list-style: none;
        }

        .nav-link {
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s ease;
            cursor: pointer;
            padding: 6px 12px;
            border-radius: 8px;
        }

        .nav-link:hover, .nav-link.active {
            color: #ffffff;
            background: rgba(255, 255, 255, 0.08);
        }

        .nav-link.active {
            color: var(--neon-cyan);
            border-bottom: 2px solid var(--neon-cyan);
            border-radius: 8px 8px 0 0;
        }

        .nav-cta {
            background: linear-gradient(90deg, var(--neon-pink), var(--neon-orange));
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 65, 108, 0.35);
        }

        .nav-cta:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 65, 108, 0.6);
        }

        /* PAGE ROUTER CONTAINERS */
        .page-view {
            display: none;
            flex: 1;
            width: 100%;
            animation: fadeIn 0.4s ease forwards;
        }

        .page-view.active-page {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ==========================================================================
           PAGE 1: 3D LANDING PAGE STYLES
           ========================================================================== */
        .landing-hero {
            padding: 70px 40px 50px 40px;
            max-width: 1240px;
            margin: 0 auto;
            text-align: center;
            position: relative;
        }

        .pill-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(0, 229, 255, 0.12);
            border: 1px solid rgba(0, 229, 255, 0.4);
            color: var(--neon-cyan);
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 0.88rem;
            font-weight: 700;
            margin-bottom: 24px;
            letter-spacing: 0.5px;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
        }

        .hero-title {
            font-size: 3.4rem;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 20px;
            letter-spacing: -1px;
        }

        .hero-title .gradient-text {
            background: linear-gradient(90deg, #ffffff 0%, #00e5ff 50%, #FFD700 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero-subtitle {
            font-size: 1.2rem;
            color: var(--text-secondary);
            max-width: 780px;
            margin: 0 auto 35px auto;
            line-height: 1.6;
        }

        .hero-cta-group {
            display: flex;
            gap: 16px;
            justify-content: center;
            align-items: center;
            margin-bottom: 60px;
        }

        .btn-primary-lg {
            background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
            color: white;
            padding: 16px 36px;
            border-radius: 14px;
            font-size: 1.05rem;
            font-weight: 700;
            border: none;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 6px 25px rgba(255, 75, 43, 0.45);
        }

        .btn-primary-lg:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 30px rgba(255, 75, 43, 0.7);
        }

        .btn-secondary-lg {
            background: rgba(255, 255, 255, 0.08);
            color: white;
            padding: 16px 32px;
            border-radius: 14px;
            font-size: 1.05rem;
            font-weight: 700;
            border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn-secondary-lg:hover {
            background: rgba(255, 255, 255, 0.15);
            border-color: var(--neon-cyan);
            transform: translateY(-3px);
        }

        /* 3D FLOATING SHOWCASE CARDS */
        .showcase-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 28px;
            margin: 40px auto 80px auto;
            max-width: 1200px;
            perspective: 1200px;
        }

        .card-3d {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 32px 26px;
            text-align: left;
            transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), border-color 0.4s ease, box-shadow 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .card-3d::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .card-3d:hover {
            transform: translateY(-8px) rotateX(4deg) rotateY(-2deg);
            border-color: rgba(0, 229, 255, 0.5);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px rgba(0, 229, 255, 0.2);
        }

        .card-3d:hover::before {
            opacity: 1;
        }

        .card-icon {
            font-size: 2.4rem;
            margin-bottom: 16px;
            display: inline-block;
            filter: drop-shadow(0 4px 10px rgba(0, 229, 255, 0.3));
        }

        .card-3d h3 {
            font-size: 1.35rem;
            color: #fff;
            margin-bottom: 12px;
            font-weight: 700;
        }

        .card-3d p {
            font-size: 0.95rem;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* 3-STEP GUIDE SECTION */
        .guide-section {
            background: rgba(0, 0, 0, 0.25);
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 80px 40px;
        }

        .section-header {
            text-align: center;
            max-width: 700px;
            margin: 0 auto 50px auto;
        }

        .section-header h2 {
            font-size: 2.3rem;
            font-weight: 800;
            margin-bottom: 12px;
            color: #fff;
        }

        .section-header p {
            color: var(--text-secondary);
            font-size: 1.05rem;
        }

        .steps-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            max-width: 1140px;
            margin: 0 auto;
        }

        .step-box {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 18px;
            padding: 30px 24px;
            position: relative;
            transition: all 0.3s ease;
        }

        .step-box:hover {
            border-color: var(--neon-gold);
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }

        .step-number {
            background: linear-gradient(135deg, var(--neon-gold), #ff9100);
            color: #000;
            font-weight: 800;
            width: 36px;
            height: 36px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            margin-bottom: 18px;
        }

        .step-box h4 {
            font-size: 1.2rem;
            color: #fff;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .step-box p {
            color: var(--text-secondary);
            font-size: 0.93rem;
            line-height: 1.6;
        }

        /* COMPARISON TABLE */
        .comparison-section {
            max-width: 1000px;
            margin: 80px auto;
            padding: 0 20px;
        }

        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .comparison-table th, .comparison-table td {
            padding: 18px 22px;
            text-align: left;
        }

        .comparison-table th {
            background: rgba(255, 255, 255, 0.06);
            color: var(--neon-gold);
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .comparison-table tr:not(:last-child) {
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .comparison-table td {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        .check-badge {
            color: #00e676;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .cross-badge {
            color: #ff5252;
            font-weight: 600;
        }

        /* ==========================================================================
           PAGE 2: AI PLANNER STUDIO STYLES
           ========================================================================== */
        .studio-container {
            display: flex;
            width: 100%;
            flex: 1;
        }

        .studio-sidebar {
            width: 360px;
            background: rgba(13, 10, 30, 0.96);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            padding: 26px 22px;
            overflow-y: auto;
            max-height: calc(100vh - 72px);
            position: sticky;
            top: 72px;
        }

        .studio-sidebar h2 {
            font-size: 1.3rem;
            color: #fff;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .studio-sidebar h3 {
            font-size: 0.92rem;
            color: var(--neon-gold);
            margin: 18px 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-group { margin-bottom: 13px; }
        .form-row { display: flex; gap: 10px; }
        .form-row .form-group { flex: 1; }
        label { display: block; font-size: 0.82rem; color: var(--text-muted); margin-bottom: 4px; font-weight: 600; }
        
        input, select {
            width: 100%;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 10px 12px;
            color: #fff;
            font-size: 0.9rem;
            outline: none;
            transition: all 0.2s;
        }

        input:focus, select:focus {
            border-color: var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
        }

        select option { background: #161233; color: #fff; }

        .btn-generate {
            width: 100%;
            background: linear-gradient(90deg, var(--neon-pink) 0%, var(--neon-orange) 100%);
            color: #fff;
            border: none;
            padding: 14px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 15px;
            transition: all 0.3s;
            box-shadow: 0 4px 18px rgba(255, 75, 43, 0.4);
        }

        .btn-generate:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(255, 75, 43, 0.7);
        }

        .btn-generate:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

        /* STUDIO MAIN VIEW */
        .studio-main {
            flex: 1;
            padding: 30px 38px;
            overflow-y: auto;
        }

        .studio-toolbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .studio-title-block h1 {
            font-size: 2.1rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff, #00e5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .studio-title-block p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin-top: 4px;
        }

        .filter-tabs {
            display: flex;
            gap: 8px;
            background: rgba(255, 255, 255, 0.05);
            padding: 4px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .tab-btn {
            background: transparent;
            color: var(--text-muted);
            border: none;
            padding: 7px 14px;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .tab-btn.active, .tab-btn:hover {
            background: rgba(0, 229, 255, 0.15);
            color: #fff;
        }

        .tab-btn.active { color: var(--neon-cyan); }

        .action-btn {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #fff;
            border-radius: 8px;
            padding: 8px 14px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        .action-btn:hover { background: rgba(0, 229, 255, 0.2); border-color: var(--neon-cyan); }

        /* STUDIO CARDS */
        .studio-grid {
            display: grid;
            grid-template-columns: 2.4fr 1.2fr;
            gap: 28px;
        }

        .day-card {
            background: var(--card-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--card-border);
            border-radius: 18px;
            padding: 22px;
            margin-bottom: 22px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .day-card:hover {
            border-color: rgba(0, 229, 255, 0.6);
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
        }

        .day-header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 215, 0, 0.3);
            padding-bottom: 8px;
            margin-bottom: 16px;
        }

        .day-title {
            color: var(--neon-gold);
            font-size: 1.3rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .day-columns {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .workout-box, .meal-box {
            background: rgba(0, 0, 0, 0.25);
            border-radius: 12px;
            padding: 18px 20px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .box-header {
            color: var(--neon-cyan);
            font-weight: 800;
            font-size: 0.95rem;
            margin-bottom: 16px;
            display: block;
            letter-spacing: 0.8px;
            border-bottom: 1px dashed rgba(0, 229, 255, 0.25);
            padding-bottom: 8px;
        }

        .plan-item {
            margin-bottom: 13px;
            font-size: 0.92rem;
            line-height: 1.65;
            color: #cbd5e1;
        }

        .plan-item strong {
            color: #ffffff;
            font-weight: 700;
        }

        /* GROCERY CARD */
        .grocery-card {
            background: rgba(0, 0, 0, 0.38);
            border: 1.5px solid var(--neon-gold);
            border-radius: 18px;
            padding: 24px 22px;
            height: fit-content;
            position: sticky;
            top: 92px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
        }

        .grocery-header-main {
            color: var(--neon-gold);
            font-size: 1.15rem;
            font-weight: 800;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255, 215, 0, 0.3);
            padding-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .grocery-category-title {
            color: #ffffff;
            font-weight: 700;
            font-size: 0.98rem;
            margin-top: 18px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .grocery-category-title::before {
            content: "•";
            color: var(--neon-cyan);
            font-weight: 900;
            font-size: 1.3rem;
            line-height: 1;
        }

        .grocery-sub-list {
            list-style: none;
            padding-left: 24px;
            margin-bottom: 16px;
        }

        .grocery-sub-item {
            margin-bottom: 10px;
            font-size: 0.92rem;
            line-height: 1.6;
            color: #cbd5e1;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }

        .grocery-sub-item::before {
            content: "•";
            color: var(--neon-cyan);
            font-size: 1.1rem;
            line-height: 1.1;
        }

        /* ==========================================================================
           PAGE 3: STUDENT MACRO & NUTRITION HUB STYLES
           ========================================================================== */
        .hub-container {
            max-width: 1140px;
            margin: 40px auto 80px auto;
            padding: 0 30px;
        }

        .macro-calc-grid {
            display: grid;
            grid-template-columns: 1fr 1.3fr;
            gap: 30px;
            margin-top: 30px;
        }

        .calc-form-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 30px;
        }

        .calc-result-card {
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid rgba(0, 229, 255, 0.4);
            border-radius: 20px;
            padding: 30px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .macro-metrics-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin: 24px 0;
        }

        .macro-metric-box {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .macro-metric-box .val {
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--neon-cyan);
        }

        .macro-metric-box .lbl {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            margin-top: 4px;
        }

        .macro-bar-container {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            height: 12px;
            overflow: hidden;
            display: flex;
            margin-top: 10px;
        }

        .macro-bar-protein { background: #ff416c; }
        .macro-bar-carbs { background: var(--neon-gold); }
        .macro-bar-fats { background: var(--neon-cyan); }

        /* TIPS GRID */
        .tips-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 22px;
            margin-top: 40px;
        }

        .tip-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 22px;
            transition: all 0.2s ease;
        }

        .tip-card:hover {
            border-color: var(--neon-cyan);
            transform: translateY(-3px);
        }

        .tip-card h4 {
            color: var(--neon-gold);
            margin-bottom: 8px;
            font-size: 1.05rem;
        }

        .tip-card p {
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* SPINNER */
        .spinner-container { display: none; text-align: center; padding: 60px; }
        .spinner { width: 50px; height: 50px; border: 4px solid rgba(255, 255, 255, 0.1); border-top-color: var(--neon-cyan); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px auto; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .info-placeholder { background: rgba(255, 255, 255, 0.03); border: 1px dashed rgba(255, 255, 255, 0.2); border-radius: 16px; padding: 60px; text-align: center; color: var(--text-muted); font-size: 1.1rem; }

        @media (max-width: 960px) {
            .studio-container { flex-direction: column; }
            .studio-sidebar { width: 100%; position: relative; top: 0; max-height: none; }
            .studio-grid { grid-template-columns: 1fr; }
            .day-columns { grid-template-columns: 1fr; }
            .hero-title { font-size: 2.4rem; }
            .macro-calc-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>

    <!-- TOP NAVIGATION BAR -->
    <nav class="navbar">
        <a class="brand-logo" onclick="switchPage('home')">
            ⚡ <span>StudentFit AI</span>
        </a>
        <ul class="nav-links">
            <li><a class="nav-link active" id="nav-home" onclick="switchPage('home')">🏠 Home & Features</a></li>
            <li><a class="nav-link" id="nav-studio" onclick="switchPage('studio')">⚡ AI Planner Studio</a></li>
            <li><a class="nav-link" id="nav-macros" onclick="switchPage('macros')">📊 Student Macro Hub</a></li>
        </ul>
        <button class="nav-cta" onclick="switchPage('studio')">🚀 Launch AI Studio</button>
    </nav>

    <!-- =========================================================================
         PAGE 1: 3D ANIMATED LANDING PAGE
         ========================================================================= -->
    <div class="page-view active-page" id="page-home">
        <section class="landing-hero">
            <div class="pill-badge">🎓 Built Exclusively for College & University Students</div>
            <h1 class="hero-title">
                Smart Fitness & Nutrition.<br>
                <span class="gradient-text">Zero Compromise on Budget or Studies.</span>
            </h1>
            <p class="hero-subtitle">
                Unlike generic fitness apps, StudentFit AI understands the reality of campus life: tight budgets, microwave/dorm rooms, and intense study schedules. Powered by high-speed Groq AI.
            </p>
            <div class="hero-cta-group">
                <button class="btn-primary-lg" onclick="switchPage('studio')">⚡ Generate My 7-Day Plan</button>
                <button class="btn-secondary-lg" onclick="switchPage('macros')">📊 Calculate Daily Macros</button>
            </div>

            <!-- 3D FLOATING SHOWCASE CARDS -->
            <div class="showcase-grid">
                <div class="card-3d">
                    <div class="card-icon">🏋️</div>
                    <h3>Dorm & Campus Adaptive</h3>
                    <p>Whether you only have 2 square meters on a dorm floor, light dumbbells, or a university gym, the AI designs exact sets, reps, and active recovery routines.</p>
                </div>
                <div class="card-3d">
                    <div class="card-icon">🥗</div>
                    <h3>Cultural & Student Cuisine</h3>
                    <p>Respects your culinary heritage (Indian, Global, Mediterranean, Asian, Vegan) while factoring in simple appliances (Microwave Only, Basic Stove, or Full Chef).</p>
                </div>
                <div class="card-3d">
                    <div class="card-icon">🛒</div>
                    <h3>Localized Grocery & Budget</h3>
                    <p>Auto-computes essential 1-person weekly grocery quantities with estimated costs in your local currency (INR ₹, USD $, EUR €, GBP £, CAD $, etc.).</p>
                </div>
            </div>
        </section>

        <!-- 3-STEP GUIDE SECTION -->
        <section class="guide-section">
            <div class="section-header">
                <h2>How It Works in 3 Simple Steps</h2>
                <p>No complicated tracking. Just clear, synchronized weekly schedules designed for student routines.</p>
            </div>
            <div class="steps-container">
                <div class="step-box">
                    <div class="step-number">1</div>
                    <h4>Enter Campus Bio-Data</h4>
                    <p>Provide your age, weight (kg/lbs), height, fitness target, cooking equipment, and weekly budget tier in seconds.</p>
                </div>
                <div class="step-box">
                    <div class="step-number">2</div>
                    <h4>AI Synchronizes Mon–Sun</h4>
                    <p>Groq's high-speed neural engine aligns your daily workouts directly with high-protein student meals for optimal muscle recovery and focus.</p>
                </div>
                <div class="step-box">
                    <div class="step-number">3</div>
                    <h4>Shop, Prep & Succeed</h4>
                    <p>Use the integrated shopping checklist, meal prep tips, and save your plan as Markdown to crush your fitness goals during semester.</p>
                </div>
            </div>
        </section>

        <!-- COMPARISON SECTION -->
        <section class="comparison-section">
            <div class="section-header">
                <h2>Why Students Choose StudentFit AI</h2>
                <p>See how StudentFit AI outperforms generic fitness and calorie tracker apps.</p>
            </div>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Generic Fitness Apps</th>
                        <th>StudentFit AI ⚡</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Dorm Room Equipment Adaptability</strong></td>
                        <td class="cross-badge">❌ Requires full commercial gym</td>
                        <td class="check-badge">✅ Adapts to Dorm Floor, Dumbbells, or Gym</td>
                    </tr>
                    <tr>
                        <td><strong>Student Budget & Local Currency</strong></td>
                        <td class="cross-badge">❌ Expensive generic meal suggestions</td>
                        <td class="check-badge">✅ Strict student budget in INR, USD, EUR, etc.</td>
                    </tr>
                    <tr>
                        <td><strong>Cooking Facility Constraints</strong></td>
                        <td class="cross-badge">❌ Assumes full chef kitchen</td>
                        <td class="check-badge">✅ Microwave-friendly & Basic Stove modes</td>
                    </tr>
                    <tr>
                        <td><strong>Cultural Cuisine Awareness</strong></td>
                        <td class="cross-badge">❌ Western-only food databases</td>
                        <td class="check-badge">✅ Indian, Mediterranean, Asian, Vegan, Global</td>
                    </tr>
                    <tr>
                        <td><strong>Weekly Grocery List Generator</strong></td>
                        <td class="cross-badge">❌ Paywalled premium feature</td>
                        <td class="check-badge">✅ Free 1-Person exact shopping checklist</td>
                    </tr>
                </tbody>
            </table>
        </section>
    </div>

    <!-- =========================================================================
         PAGE 2: AI PLANNER STUDIO (ENTRY WIZARD -> SIDEBAR DASHBOARD)
         ========================================================================= -->
    <div class="page-view" id="page-studio">
        <!-- 1. ENTRY SETUP WIZARD (FIRST TIME VIEW) -->
        <div id="studio-entry-view" style="max-width: 900px; margin: 40px auto 80px auto; padding: 0 20px;">
            <div class="card-3d" style="background: rgba(13, 10, 32, 0.85); border: 1px solid rgba(0, 229, 255, 0.35); box-shadow: 0 20px 60px rgba(0,0,0,0.6); padding: 40px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <div class="pill-badge">⚡ Step 1 of 1 — Personalize Your Week</div>
                    <h2 style="font-size: 2.2rem; font-weight: 800; color: #fff; margin: 10px 0;">Student Fit Profile Setup</h2>
                    <p style="color: var(--text-secondary); font-size: 1rem;">Configure your campus fitness constraints once. Your customized 7-day schedule & budget grocery list will generate instantly.</p>
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
                    <h4 style="color: var(--neon-pink); margin-bottom: 14px; font-size: 1.05rem;">🥑 Kitchen, Cuisine & Local Currency</h4>
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
                    <button class="btn-primary-lg" style="width: 100%; max-width: 480px; font-size: 1.15rem;" onclick="submitEntryAndGenerate()">
                        🚀 GENERATE 7-DAY SCHEDULE & GROCERIES
                    </button>
                </div>
            </div>
        </div>

        <!-- 2. STUDIO DASHBOARD VIEW (ACTIVATED AFTER GENERATING, WITH EDITABLE SIDEBAR) -->
        <div id="studio-dashboard-view" class="studio-container" style="display: none;">
            <!-- LIVE EDITABLE SIDEBAR -->
            <aside class="studio-sidebar">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <h2>⚡ Studio Controls</h2>
                    <button onclick="showWizardEntry()" style="background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.2); color: var(--neon-cyan); border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; cursor: pointer;">✏️ Full View</button>
                </div>

                <h3>🏃‍♂️ Bio-Data</h3>
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

                <h3>🎯 Goals & Gear</h3>
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

                <h3>🥑 Kitchen & Budget</h3>
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

                <button class="btn-generate" id="generateBtn" onclick="generatePlan()">🔄 RE-GENERATE PLAN</button>
            </aside>

            <!-- STUDIO WORKSPACE -->
            <main class="studio-main">
                <div class="studio-toolbar">
                    <div class="studio-title-block">
                        <h1>AI Planner Studio ⚡</h1>
                        <p>Synchronized Monday–Sunday Workout & Meal Schedules</p>
                    </div>
                    <div style="display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
                        <div class="filter-tabs">
                            <button class="tab-btn active" onclick="filterView('all', this)">All</button>
                            <button class="tab-btn" onclick="filterView('workout', this)">🏋️ Workouts</button>
                            <button class="tab-btn" onclick="filterView('meal', this)">🥗 Meals</button>
                        </div>
                        <button id="downloadBtn" class="action-btn" style="display: none;" onclick="downloadPDF()">📥 Save Plan (PDF)</button>
                    </div>
                </div>

                <div id="spinner" class="spinner-container">
                    <div class="spinner"></div>
                    <h3 style="color: var(--neon-cyan); margin-bottom: 6px;">🗓️ AI Neural Engine is Synchronizing Your Week...</h3>
                    <p style="color: var(--text-muted);">Crafting campus workouts, macro-dense meals, and localized grocery lists...</p>
                </div>

                <div id="placeholder" class="info-placeholder">
                    👈 Customize your student bio-data, available gear, and cuisine in the live sidebar, then click <strong>"RE-GENERATE PLAN"</strong>.
                </div>

                <div id="resultsArea" class="studio-grid" style="display: none;">
                    <div id="daysContainer"></div>
                    <div class="grocery-card" id="groceryCard"></div>
                </div>
            </main>
        </div>
    </div>

    <!-- =========================================================================
         PAGE 3: STUDENT MACRO & NUTRITION HUB
         ========================================================================= -->
    <div class="page-view" id="page-macros">
        <div class="hub-container">
            <div class="section-header">
                <h2>Student BMR & Macro Calculator</h2>
                <p>Calculate your daily maintenance calories and optimal macronutrient split for study energy and muscle growth.</p>
            </div>

            <div class="macro-calc-grid">
                <!-- FORM CARD -->
                <div class="calc-form-card">
                    <h3 style="color: var(--neon-gold); margin-bottom: 18px;">Personal Metrics</h3>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Gender</label>
                            <select id="m_gender">
                                <option value="Male" selected>Male</option>
                                <option value="Female">Female</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Age</label>
                            <input type="number" id="m_age" value="20">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group" style="flex: 2;">
                            <label>Weight</label>
                            <input type="number" id="m_weight" value="70">
                        </div>
                        <div class="form-group" style="flex: 1.2;">
                            <label>Unit</label>
                            <select id="m_weight_unit">
                                <option value="kg" selected>kg</option>
                                <option value="lbs">lbs</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group" style="flex: 2;">
                            <label>Height</label>
                            <input type="number" id="m_height" value="170">
                        </div>
                        <div class="form-group" style="flex: 1.2;">
                            <label>Unit</label>
                            <select id="m_height_unit">
                                <option value="cm" selected>cm</option>
                                <option value="ft/in">ft/in</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Target Goal</label>
                        <select id="m_goal">
                            <option value="Build Muscle" selected>Build Muscle (Surplus +350 kcal)</option>
                            <option value="Lose Weight">Lose Weight (Deficit -400 kcal)</option>
                            <option value="Exam Stress Relief">Maintain & Energy</option>
                        </select>
                    </div>
                    <button class="btn-generate" onclick="calculateStudentMacros()">⚡ Calculate Macros</button>
                </div>

                <!-- RESULT CARD -->
                <div class="calc-result-card">
                    <h3 style="color: #fff; font-size: 1.4rem; margin-bottom: 6px;">Daily Target</h3>
                    <div style="font-size: 3rem; font-weight: 800; color: var(--neon-cyan);" id="res_calories">2,400 <span style="font-size: 1.2rem; color: #fff;">kcal/day</span></div>
                    <p style="color: var(--text-muted); font-size: 0.9rem;" id="res_meta">BMR: 1,650 kcal | TDEE: 2,050 kcal</p>

                    <div class="macro-metrics-row">
                        <div class="macro-metric-box">
                            <div class="val" id="res_protein" style="color: var(--neon-pink);">140g</div>
                            <div class="lbl">Protein</div>
                        </div>
                        <div class="macro-metric-box">
                            <div class="val" id="res_carbs" style="color: var(--neon-gold);">290g</div>
                            <div class="lbl">Carbs</div>
                        </div>
                        <div class="macro-metric-box">
                            <div class="val" id="res_fats" style="color: var(--neon-cyan);">65g</div>
                            <div class="lbl">Fats</div>
                        </div>
                    </div>

                    <div style="font-size: 0.85rem; color: var(--text-muted); display: flex; justify-content: space-between;">
                        <span>Macro Ratio</span>
                        <span id="res_water">💧 Water Target: 2.8 Liters/day</span>
                    </div>
                    <div class="macro-bar-container">
                        <div class="macro-bar-protein" id="bar_p" style="width: 25%;"></div>
                        <div class="macro-bar-carbs" id="bar_c" style="width: 50%;"></div>
                        <div class="macro-bar-fats" id="bar_f" style="width: 25%;"></div>
                    </div>
                </div>
            </div>

            <!-- NUTRITION TIPS -->
            <div class="tips-grid">
                <div class="tip-card">
                    <h4>🥚 #1 Cheap Protein: Eggs & Soya</h4>
                    <p>Eggs, Paneer, Tofu, and Soya chunks provide over 20g of high-bioavailability protein for less than ₹30 / $0.50 per serving.</p>
                </div>
                <div class="tip-card">
                    <h4>🍲 Batch Cook Starches on Sunday</h4>
                    <p>Cook 3 days of brown rice or boil 500g chickpeas in one pot. Store in containers to save 45 minutes of daily study time.</p>
                </div>
                <div class="tip-card">
                    <h4>🧠 Study Focus & Hydration</h4>
                    <p>Dehydration drops cognitive performance by 15%. Keep a 1L water bottle at your desk and aim for 3 refills during exam weeks.</p>
                </div>
                <div class="tip-card">
                    <h4>🥜 Smart Healthy Fats</h4>
                    <p>Peanut butter and whole oats provide sustained slow-release energy for long university lecture schedules.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- JAVASCRIPT FOR MULTI-PAGE & AI STUDIO -->
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
                cookingSkill: document.getElementById('cookingSkill').value
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
                        card.className = 'day-card';
                        card.innerHTML = `
                            <div class="day-header-row">
                                <div class="day-title">🗓️ ${day.day}</div>
                            </div>
                            <div class="day-columns">
                                <div class="workout-box">
                                    <span class="box-header">🏋️ WORKOUT ROUTINE</span>
                                    <div>${formatLines(day.workout)}</div>
                                </div>
                                <div class="meal-box">
                                    <span class="box-header">🥗 SYNCHRONIZED MEALS</span>
                                    <div>${formatLines(day.meal)}</div>
                                </div>
                            </div>
                        `;
                        daysContainer.appendChild(card);
                    });

                    groceryCard.innerHTML = formatGroceryList(data.grocery);
                    resultsArea.style.display = 'grid';
                    downloadBtn.style.display = 'inline-flex';
                }
            } catch (err) {
                alert('Connection error: ' + err.message);
                placeholder.style.display = 'block';
            } finally {
                spinner.style.display = 'none';
                btn.disabled = false;
            }
        }

        function formatLines(text) {
            if (!text) return "";
            const lines = text.split('\\n');
            let html = '';
            lines.forEach(line => {
                line = line.trim();
                if (!line) return;
                line = line.replace(/^[\\*\\-]\\s*/, '');
                line = line.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color: #ffffff;">$1</strong>');
                html += `<div class="plan-item">${line}</div>`;
            });
            return html;
        }

        function formatGroceryList(text) {
            if (!text) return "";
            let html = '<div class="grocery-header-main">🛒 Weekly Student Shopping List</div>';
            const lines = text.split('\\n');
            let listOpen = false;

            lines.forEach(line => {
                line = line.trim();
                if (!line) return;

                if (line.startsWith('####') || line.startsWith('###') || (line.startsWith('**') && line.endsWith('**') && !line.includes('₹') && !line.includes('$'))) {
                    if (listOpen) {
                        html += '</ul>';
                        listOpen = false;
                    }
                    let title = line.replace(/^[#\\*]+\\s*/, '').replace(/\\*+/g, '').trim();
                    html += `<div class="grocery-category-title">${title}</div><ul class="grocery-sub-list">`;
                    listOpen = true;
                } else if (line.startsWith('*') || line.startsWith('-')) {
                    if (!listOpen) {
                        html += '<ul class="grocery-sub-list">';
                        listOpen = true;
                    }
                    let item = line.replace(/^[\\*\\-]\\s*/, '').trim();
                    item = item.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color: #ffffff;">$1</strong>');
                    html += `<li class="grocery-sub-item">${item}</li>`;
                } else {
                    let item = line.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color: #ffffff;">$1</strong>');
                    html += `<div class="plan-item">${item}</div>`;
                }
            });

            if (listOpen) html += '</ul>';
            return html;
        }

        function filterView(type, btn) {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const workoutBoxes = document.querySelectorAll('.workout-box');
            const mealBoxes = document.querySelectorAll('.meal-box');

            if (type === 'workout') {
                workoutBoxes.forEach(b => b.style.display = 'block');
                mealBoxes.forEach(b => b.style.display = 'none');
            } else if (type === 'meal') {
                workoutBoxes.forEach(b => b.style.display = 'none');
                mealBoxes.forEach(b => b.style.display = 'block');
            } else {
                workoutBoxes.forEach(b => b.style.display = 'block');
                mealBoxes.forEach(b => b.style.display = 'block');
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

            // Adjust styles for clean printing on white background
            element.querySelectorAll('.day-card').forEach(c => {
                c.style.background = '#f8fafc';
                c.style.border = '1px solid #cbd5e1';
                c.style.color = '#1e293b';
                c.style.marginBottom = '16px';
                c.style.padding = '14px';
                c.style.borderRadius = '8px';
            });
            element.querySelectorAll('.day-title').forEach(t => {
                t.style.color = '#ff416c';
                t.style.fontSize = '15px';
                t.style.fontWeight = 'bold';
            });
            element.querySelectorAll('.box-header, .col-header').forEach(h => {
                h.style.color = '#0284c7';
                h.style.fontWeight = 'bold';
                h.style.fontSize = '13px';
            });
            element.querySelectorAll('.workout-box, .meal-box, .col-box').forEach(b => {
                b.style.background = '#ffffff';
                b.style.border = '1px solid #e2e8f0';
                b.style.padding = '10px 12px';
                b.style.borderRadius = '6px';
                b.style.marginBottom = '8px';
            });
            element.querySelectorAll('li, p, div').forEach(p => {
                p.style.color = '#334155';
            });
            element.querySelectorAll('strong').forEach(s => {
                s.style.color = '#0f172a';
            });
            element.querySelectorAll('h4').forEach(h => {
                h.style.color = '#b45309';
                h.style.borderBottom = '1px solid #e2e8f0';
                h.style.paddingBottom = '4px';
                h.style.marginTop = '14px';
            });

            const opt = {
                margin: [10, 10, 10, 10],
                filename: 'StudentFit_Weekly_Schedule.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2, useCORS: true },
                jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
            };

            html2pdf().set(opt).from(element).save();
        }

        async function calculateStudentMacros() {
            const age = document.getElementById('m_age').value;
            const gender = document.getElementById('m_gender').value;
            const weight = document.getElementById('m_weight').value;
            const weight_unit = document.getElementById('m_weight_unit').value;
            const height = document.getElementById('m_height').value;
            const height_unit = document.getElementById('m_height_unit').value;
            const goal = document.getElementById('m_goal').value;

            try {
                const res = await fetch('/api/macros', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ age, gender, weight, weight_unit, height, height_unit, goal })
                });
                const data = await res.json();

                document.getElementById('res_calories').innerHTML = `${data.target_calories.toLocaleString()} <span style="font-size: 1.2rem; color: #fff;">kcal/day</span>`;
                document.getElementById('res_meta').innerText = `BMR: ${data.bmr} kcal | TDEE: ${data.tdee} kcal`;
                document.getElementById('res_protein').innerText = `${data.protein_g}g`;
                document.getElementById('res_carbs').innerText = `${data.carbs_g}g`;
                document.getElementById('res_fats').innerText = `${data.fats_g}g`;
                document.getElementById('res_water').innerText = `💧 Water Target: ${data.water_liters} Liters/day`;

                const totalG = data.protein_g + data.carbs_g + data.fats_g;
                document.getElementById('bar_p').style.width = ((data.protein_g / totalG) * 100) + '%';
                document.getElementById('bar_c').style.width = ((data.carbs_g / totalG) * 100) + '%';
                document.getElementById('bar_f').style.width = ((data.fats_g / totalG) * 100) + '%';
            } catch (e) {
                alert('Macro computation error: ' + e.message);
            }
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
