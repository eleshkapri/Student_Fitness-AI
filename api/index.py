import os
import sys
from flask import Flask, render_template_string, request, jsonify

# Ensure local modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import (
    get_api_key,
    parse_ai_response,
    generate_plan_mock,
    generate_plan_real,
    CANDIDATE_MODELS
)

app = Flask(__name__)

# --- MINIFIED & OPTIMIZED HTML TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudentFit AI ⚡ | 7-Day Aligned Schedule</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; scrollbar-width: thin; scrollbar-color: rgba(255, 255, 255, 0.2) transparent; }
        body { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); color: #fff; min-height: 100vh; display: flex; flex-direction: column; }
        
        /* ULTRA-THIN & TRANSPARENT SCROLLBAR */
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.18); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0, 229, 255, 0.5); }

        .container { display: flex; flex: 1; width: 100%; }
        
        /* SIDEBAR */
        .sidebar { width: 340px; background: rgba(18, 18, 18, 0.95); backdrop-filter: blur(15px); border-right: 1px solid rgba(255, 255, 255, 0.1); padding: 25px 20px; overflow-y: auto; max-height: 100vh; position: sticky; top: 0; }
        .sidebar h2 { font-size: 1.3rem; color: #fff; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }
        .sidebar h3 { font-size: 0.95rem; color: #FFD700; margin: 18px 0 10px 0; text-transform: uppercase; letter-spacing: 0.5px; }
        .form-group { margin-bottom: 13px; }
        .form-row { display: flex; gap: 10px; }
        .form-row .form-group { flex: 1; }
        label { display: block; font-size: 0.82rem; color: #bbb; margin-bottom: 4px; font-weight: 500; }
        input, select { width: 100%; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 9px 12px; color: #fff; font-size: 0.9rem; outline: none; transition: border-color 0.2s; }
        input:focus, select:focus { border-color: #00e5ff; }
        select option { background: #1a1a2e; color: #fff; }
        
        /* BUTTONS */
        .btn-generate { width: 100%; background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%); color: #fff; border: none; padding: 14px; border-radius: 12px; font-weight: 700; font-size: 1rem; cursor: pointer; margin-top: 15px; transition: all 0.3s; box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4); }
        .btn-generate:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6); }
        .btn-generate:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        
        .action-btn { background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.2); color: #fff; border-radius: 8px; padding: 8px 14px; cursor: pointer; font-size: 0.85rem; font-weight: 600; transition: all 0.2s; }
        .action-btn:hover { background: rgba(0, 229, 255, 0.2); border-color: #00e5ff; }

        /* MAIN CONTENT */
        .main-content { flex: 1; padding: 35px 40px; overflow-y: auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
        .header h1 { font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #ffffff, #00e5ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .header p { color: #aaa; font-size: 0.95rem; margin-top: 4px; }
        .badge-status { background: rgba(0, 229, 255, 0.15); border: 1px solid #00e5ff; color: #00e5ff; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; }

        /* RESULTS LAYOUT */
        .results-grid { display: grid; grid-template-columns: 2.4fr 1.2fr; gap: 28px; }
        .day-card { background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 22px; margin-bottom: 22px; transition: all 0.2s ease; }
        .day-card:hover { border-color: rgba(0, 229, 255, 0.5); transform: translateY(-2px); }
        .day-title { color: #FFD700; font-size: 1.25rem; font-weight: 700; text-transform: uppercase; border-bottom: 1px solid rgba(255, 215, 0, 0.3); padding-bottom: 8px; margin-bottom: 16px; }
        .day-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .col-box { background: rgba(0, 0, 0, 0.25); border-radius: 12px; padding: 16px 18px; border: 1px solid rgba(255, 255, 255, 0.05); }
        .col-header { color: #00e5ff; font-weight: 700; font-size: 0.95rem; margin-bottom: 12px; display: block; letter-spacing: 0.5px; border-bottom: 1px dashed rgba(0, 229, 255, 0.2); padding-bottom: 6px; }
        .markdown-content ul { list-style: none; padding-left: 0; }
        .markdown-content li { margin-bottom: 10px; font-size: 0.92rem; color: #e2e8f0; line-height: 1.6; }
        .markdown-content strong { color: #fff; }

        /* GROCERY CARD WITH SPACIOUS READABILITY */
        .grocery-card { background: rgba(0, 0, 0, 0.35); border: 1px solid #FFD700; border-radius: 16px; padding: 24px 22px; height: fit-content; position: sticky; top: 20px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); }
        .grocery-card h4 { color: #FFD700; border-bottom: 1px solid rgba(255, 215, 0, 0.35); padding-bottom: 8px; margin-top: 22px; margin-bottom: 14px; font-size: 1.1rem; font-weight: 700; }
        .grocery-card h4:first-child { margin-top: 0; }
        .grocery-card ul { list-style: none; padding-left: 0; margin-bottom: 14px; }
        .grocery-card li { margin-bottom: 12px; font-size: 0.93rem; color: #e2e8f0; line-height: 1.65; display: flex; align-items: flex-start; gap: 8px; }
        .grocery-card li::before { content: "•"; color: #00e5ff; font-weight: bold; font-size: 1.2rem; line-height: 1.2; }
        .grocery-card p { margin-bottom: 12px; line-height: 1.6; color: #cbd5e1; font-size: 0.93rem; }
        
        /* SPINNER & PLACEHOLDER */
        .spinner-container { display: none; text-align: center; padding: 60px; }
        .spinner { width: 50px; height: 50px; border: 4px solid rgba(255, 255, 255, 0.1); border-top-color: #00e5ff; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 15px auto; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .info-placeholder { background: rgba(255, 255, 255, 0.03); border: 1px dashed rgba(255, 255, 255, 0.2); border-radius: 16px; padding: 60px; text-align: center; color: #aaa; font-size: 1.1rem; }

        @media (max-width: 900px) {
            .container { flex-direction: column; }
            .sidebar { width: 100%; position: relative; max-height: none; }
            .results-grid { grid-template-columns: 1fr; }
            .day-columns { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- SIDEBAR -->
        <div class="sidebar">
            <h2>⚡ StudentFit Setup</h2>

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
                <label>Fitness Goal</label>
                <select id="goal">
                    <option value="Build Muscle" selected>Build Muscle</option>
                    <option value="Lose Weight">Lose Weight</option>
                    <option value="Get Shredded">Get Shredded</option>
                    <option value="Exam Stress Relief">Exam Stress Relief</option>
                </select>
            </div>

            <div class="form-group">
                <label>Available Gear</label>
                <select id="equipment">
                    <option value="Full Gym" selected>Full Gym</option>
                    <option value="Dumbbells Only">Dumbbells Only</option>
                    <option value="No Equipment (Dorm)">No Equipment (Dorm)</option>
                </select>
            </div>

            <h3>🥑 Kitchen & Budget</h3>
            <div class="form-group">
                <label>Cuisine</label>
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
                <label>Cooking Skill</label>
                <select id="cookingSkill">
                    <option value="Microwave Only">Microwave Only</option>
                    <option value="Basic Stove" selected>Basic Stove</option>
                    <option value="Full Chef">Full Chef</option>
                </select>
            </div>

            <button class="btn-generate" id="generateBtn" onclick="generatePlan()">🚀 GENERATE WEEKLY PLAN</button>
        </div>

        <!-- MAIN VIEW -->
        <div class="main-content">
            <div class="header">
                <div>
                    <h1>StudentFit AI ⚡</h1>
                    <p>Your Hyper-Personalized 7-Day Aligned Schedule</p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <div id="statusBadge" class="badge-status">Ready</div>
                    <button id="downloadBtn" class="action-btn" style="display: none;" onclick="downloadMarkdown()">📥 Save Plan</button>
                </div>
            </div>

            <div id="spinner" class="spinner-container">
                <div class="spinner"></div>
                <h3 style="color: #00e5ff; margin-bottom: 5px;">🗓️ Synchronizing your 7-day schedule with AI...</h3>
                <p style="color: #aaa;">Tailoring exercises, student meals, and localized grocery budgets...</p>
            </div>

            <div id="placeholder" class="info-placeholder">
                👈 Configure your bio-data, goals, and cuisine preferences in the sidebar, then click <strong>"GENERATE WEEKLY PLAN"</strong>.
            </div>

            <div id="resultsArea" class="results-grid" style="display: none;">
                <div id="daysContainer"></div>
                <div class="grocery-card" id="groceryCard"></div>
            </div>
        </div>
    </div>

    <script>
        let currentRawPlan = "";

        async function generatePlan() {
            const btn = document.getElementById('generateBtn');
            const spinner = document.getElementById('spinner');
            const placeholder = document.getElementById('placeholder');
            const resultsArea = document.getElementById('resultsArea');
            const statusBadge = document.getElementById('statusBadge');
            const daysContainer = document.getElementById('daysContainer');
            const groceryCard = document.getElementById('groceryCard');
            const downloadBtn = document.getElementById('downloadBtn');

            btn.disabled = true;
            placeholder.style.display = 'none';
            resultsArea.style.display = 'none';
            downloadBtn.style.display = 'none';
            spinner.style.display = 'block';
            statusBadge.innerText = 'Generating...';

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
                    statusBadge.innerText = 'Error';
                    placeholder.style.display = 'block';
                } else {
                    currentRawPlan = data.raw || "";
                    daysContainer.innerHTML = '';
                    
                    data.days.forEach(day => {
                        const card = document.createElement('div');
                        card.className = 'day-card';
                        card.innerHTML = `
                            <div class="day-title">🗓️ ${day.day}</div>
                            <div class="day-columns">
                                <div class="col-box">
                                    <span class="col-header">🏋️ WORKOUT ROUTINE</span>
                                    <div class="markdown-content">${marked.parse(day.workout)}</div>
                                </div>
                                <div class="col-box">
                                    <span class="col-header">🥗 SYNCHRONIZED MEALS</span>
                                    <div class="markdown-content">${marked.parse(day.meal)}</div>
                                </div>
                            </div>
                        `;
                        daysContainer.appendChild(card);
                    });

                    groceryCard.innerHTML = marked.parse(data.grocery);
                    resultsArea.style.display = 'grid';
                    downloadBtn.style.display = 'inline-block';
                    statusBadge.innerText = `Generated using ${data.source}`;
                }
            } catch (err) {
                alert('Connection error: ' + err.message);
                statusBadge.innerText = 'Failed';
                placeholder.style.display = 'block';
            } finally {
                spinner.style.display = 'none';
                btn.disabled = false;
            }
        }

        function downloadMarkdown() {
            if (!currentRawPlan) return;
            const blob = new Blob([currentRawPlan], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'StudentFit_Weekly_Schedule.md';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
