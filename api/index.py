import os
import re
import json
from flask import Flask, render_template_string, request, jsonify
from groq import Groq

app = Flask(__name__)

# --- HELPER FUNCTIONS ---
def parse_ai_response(text):
    days = []
    grocery_section = "No grocery list generated."
    
    # Split by the separator we asked the AI to use
    blocks = text.split("|||")
    
    for block in blocks:
        block = block.strip()
        if re.search(r"(?:Day|Day\s*\d+):", block, re.IGNORECASE):
            try:
                day_match = re.search(r"(?:Day|Day\s*\d+):\s*([^\n\r*#]+)", block, re.IGNORECASE)
                day_line = day_match.group(1).strip() if day_match else "Daily Routine"
                
                workout_match = re.search(r"(?:\*{0,2}Workout\*{0,2}):\s*(.*?)(?=(?:\*{0,2}Meal\*{0,2}):)", block, re.DOTALL | re.IGNORECASE)
                workout_text = workout_match.group(1).strip() if workout_match else "Rest day / Active recovery"
                
                meal_match = re.search(r"(?:\*{0,2}Meal\*{0,2}):\s*(.*)", block, re.DOTALL | re.IGNORECASE)
                meal_text = meal_match.group(1).strip() if meal_match else "Standard Student Diet"
                
                days.append({
                    "day": day_line,
                    "workout": workout_text,
                    "meal": meal_text
                })
            except Exception:
                continue
                
        elif "GROCERY" in block.upper():
            grocery_section = re.sub(r"^.*?GROCERY", "", block, flags=re.IGNORECASE | re.DOTALL).strip()
            
    return days, grocery_section

def generate_plan_mock(profile):
    return """
    Day: Monday
    Workout: * **Push:** Pushups (3x12)\n* **Core:** Plank (45s)
    Meal: * **Breakfast:** Oats\n* **Lunch:** Lentils & Rice
    |||
    Day: Tuesday
    Workout: * **Legs:** Squats (3x15)\n* **Cardio:** Jogging (15m)
    Meal: * **Breakfast:** Boiled Eggs\n* **Lunch:** Brown Rice & Veggies
    |||
    Day: Wednesday
    Workout: * **Pull:** Pull-ups/Rows (3x10)\n* **Core:** Leg Raises (3x15)
    Meal: * **Breakfast:** Peanut Butter Toast\n* **Lunch:** Chickpea Curry
    |||
    Day: Thursday
    Workout: * **Cardio:** HIIT / Jumping Jacks (20m)\n* **Mobility:** Stretching
    Meal: * **Breakfast:** Fruit Smoothie\n* **Lunch:** Paneer / Tofu Wrap
    |||
    Day: Friday
    Workout: * **Full Body:** Dumbbell Circuit (3x12)\n* **Core:** Side Plank
    Meal: * **Breakfast:** Oatmeal with Banana\n* **Lunch:** Mixed Dal & Roti
    |||
    Day: Saturday
    Workout: * **Active Recovery:** Long Walk / Light Jog\n* **Mobility:** Yoga
    Meal: * **Breakfast:** Scrambled Eggs / Besan Chilla\n* **Lunch:** Rice, Curd & Salad
    |||
    Day: Sunday
    Workout: * **Rest:** Complete Body Rest & Hydration
    Meal: * **Breakfast:** High Protein Pancakes\n* **Lunch:** Weekend Meal Prep
    |||
    GROCERY
    #### 🛒 Shopping List (1 Person)
    * 1 Dozen Eggs (or Tofu)
    * 1kg Brown Rice / Whole Wheat
    * 500g Oats
    * 500g Lentils / Dal
    * 1 Jar Peanut Butter
    * Seasonal Veggies & Fruits
    #### 💡 Tips
    * Cook in batches to save electricity and study time.
    #### 💰 Estimated Budget
    * Approx. ₹800 - ₹1200 INR (Indian Pricing)
    * Approx. $15 - $20 USD (Global Standard)
    """

def generate_plan_real(profile, api_key, chosen_model="openai/gpt-oss-20b"):
    client = Groq(api_key=api_key)
    
    prompt = f"""
    Act as an expert fitness and nutrition coach for a university student.
    Profile: {profile.get('age', 20)}y/o, {profile.get('gender', 'Male')}, {profile.get('weight', 70)}kg, height: {profile.get('height', 170)}cm.
    Goal: {profile.get('goal', 'Build Muscle')}. Equipment: {profile.get('equipment', 'Full Gym')}.
    Diet: {profile.get('diet_type', 'Standard')} ({profile.get('cuisine', 'Indian')}), Budget: {profile.get('budget', 'Moderate ($$)')}.
    Cooking: {profile.get('cooking_skill', 'Basic Stove')}.

    TASK: Create a 7-day plan (Monday-Sunday).
    
    STRICT OUTPUT FORMAT (Do not deviate):
    For each day, output a block separated by "|||".
    Inside each block, use "Day:", "Workout:", and "Meal:" labels exactly.
    
    Example format:
    Day: Monday
    Workout:
    * **Focus:** Chest
    * **Exercise:** Pushups (3x12)
    Meal:
    * **Breakfast:** Oats
    * **Lunch:** Rice
    |||
    Day: Tuesday
    ...
    |||
    GROCERY
    #### 🛒 Shopping List (1 Person)
    * [Quantity] [Item]
    #### 💡 Tips
    * [Tip]
    #### 💰 Estimated Budget
    * Estimate the weekly cost in the currency relevant to the Cuisine selected (e.g., INR for Indian, USD for Global/US, EUR for Mediterranean). 
    * Also provide a rough USD conversion.

    Begin immediately.
    """
    
    candidate_models = [
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b",
        "groq/compound-mini",
        "groq/compound",
        "qwen/qwen3.6-27b",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]
    
    if chosen_model in candidate_models:
        models_to_try = [chosen_model] + [m for m in candidate_models if m != chosen_model]
    else:
        models_to_try = candidate_models
        
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
                temperature=0.5,
                max_tokens=4096,
            )
            content = response.choices[0].message.content
            if content and len(content.strip()) > 0:
                content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
                return content, model_name
        except Exception as e:
            last_error = e
            continue
            
    return f"Error: {last_error}", None

# --- HTML TEMPLATE WITH NEON GLASSMORPHISM ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StudentFit AI ⚡ | 7-Day Aligned Schedule</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        body {
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            color: #ffffff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .container {
            display: flex;
            flex: 1;
            width: 100%;
        }

        /* SIDEBAR */
        .sidebar {
            width: 340px;
            background: rgba(18, 18, 18, 0.95);
            backdrop-filter: blur(15px);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px 20px;
            overflow-y: auto;
            max-height: 100vh;
            position: sticky;
            top: 0;
        }

        .sidebar h2 {
            font-size: 1.3rem;
            color: #ffffff;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .sidebar h3 {
            font-size: 1rem;
            color: #FFD700;
            margin: 18px 0 10px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .form-group {
            margin-bottom: 14px;
        }

        .form-row {
            display: flex;
            gap: 10px;
        }

        .form-row .form-group {
            flex: 1;
        }

        label {
            display: block;
            font-size: 0.85rem;
            color: #bbb;
            margin-bottom: 5px;
            font-weight: 500;
        }

        input, select {
            width: 100%;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 9px 12px;
            color: #fff;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus, select:focus {
            border-color: #00e5ff;
        }

        select option {
            background: #1a1a2e;
            color: #fff;
        }

        .btn-generate {
            width: 100%;
            background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
            color: white;
            border: none;
            padding: 14px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 15px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(255, 75, 43, 0.4);
        }

        .btn-generate:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 75, 43, 0.6);
        }

        .btn-generate:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* MAIN CONTENT */
        .main-content {
            flex: 1;
            padding: 35px 40px;
            overflow-y: auto;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .header h1 {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff, #00e5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            color: #aaa;
            font-size: 1rem;
            margin-top: 4px;
        }

        .badge-status {
            background: rgba(0, 229, 255, 0.15);
            border: 1px solid #00e5ff;
            color: #00e5ff;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }

        /* GRID LAYOUT FOR RESULTS */
        .results-grid {
            display: grid;
            grid-template-columns: 2.4fr 1.2fr;
            gap: 25px;
        }

        /* DAY CARDS */
        .day-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 20px;
            transition: all 0.2s ease;
        }

        .day-card:hover {
            border-color: rgba(0, 229, 255, 0.5);
            transform: translateY(-2px);
        }

        .day-title {
            color: #FFD700;
            font-size: 1.3rem;
            font-weight: 700;
            text-transform: uppercase;
            border-bottom: 1px solid rgba(255, 215, 0, 0.3);
            padding-bottom: 8px;
            margin-bottom: 15px;
        }

        .day-columns {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .col-workout, .col-meal {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 14px;
        }

        .col-header {
            color: #00e5ff;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 10px;
            display: block;
        }

        .markdown-content ul {
            list-style: none;
            padding-left: 0;
        }

        .markdown-content li {
            margin-bottom: 6px;
            font-size: 0.92rem;
            color: #e0e0e0;
            line-height: 1.4;
        }

        .markdown-content strong {
            color: #fff;
        }

        /* GROCERY CARD */
        .grocery-card {
            background: rgba(0, 0, 0, 0.35);
            border: 1px solid #FFD700;
            border-radius: 16px;
            padding: 22px;
            height: fit-content;
            position: sticky;
            top: 20px;
        }

        .grocery-card h4 {
            color: #FFD700;
            border-bottom: 1px solid #FFD700;
            padding-bottom: 6px;
            margin-top: 18px;
            margin-bottom: 10px;
            font-size: 1.1rem;
        }

        .grocery-card h4:first-child {
            margin-top: 0;
        }

        .grocery-item {
            margin-bottom: 6px;
            color: #e0e0e0;
            font-size: 0.9rem;
        }

        /* SPINNER */
        .spinner-container {
            display: none;
            text-align: center;
            padding: 60px;
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-top-color: #00e5ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px auto;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .info-placeholder {
            background: rgba(255, 255, 255, 0.03);
            border: 1px dashed rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            padding: 60px;
            text-align: center;
            color: #aaa;
            font-size: 1.1rem;
        }

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
            <h2>⚙️ StudentFit Setup</h2>
            
            <div class="form-group">
                <label>Groq API Key (Optional if preset)</label>
                <input type="password" id="apiKey" placeholder="gsk_..." value="">
            </div>

            <div class="form-group">
                <label>🤖 AI Model</label>
                <select id="modelOption">
                    <option value="openai/gpt-oss-20b" selected>openai/gpt-oss-20b (Fast & Free)</option>
                    <option value="openai/gpt-oss-120b">openai/gpt-oss-120b</option>
                    <option value="groq/compound-mini">groq/compound-mini</option>
                    <option value="groq/compound">groq/compound</option>
                    <option value="qwen/qwen3.6-27b">qwen/qwen3.6-27b</option>
                </select>
            </div>

            <div class="form-group">
                <label><input type="checkbox" id="demoMode" style="width: auto; margin-right: 5px;"> Demo Mode (Offline Simulation)</label>
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
                <div class="form-group">
                    <label>Weight (kg)</label>
                    <input type="number" id="weight" value="70" min="40" max="150">
                </div>
                <div class="form-group">
                    <label>Height (cm)</label>
                    <input type="number" id="height" value="170" min="140" max="220">
                </div>
            </div>

            <h3>🎯 Goals & Gear</h3>
            <div class="form-group">
                <label>Fitness Goal</label>
                <select id="goal">
                    <option value="Lose Weight">Lose Weight</option>
                    <option value="Build Muscle" selected>Build Muscle</option>
                    <option value="Get Shredded">Get Shredded</option>
                    <option value="Exam Stress Relief">Exam Stress Relief</option>
                </select>
            </div>

            <div class="form-group">
                <label>Available Gear</label>
                <select id="equipment">
                    <option value="No Equipment (Dorm)">No Equipment (Dorm)</option>
                    <option value="Dumbbells Only">Dumbbells Only</option>
                    <option value="Full Gym" selected>Full Gym</option>
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

            <div class="form-group">
                <label>Budget Tier</label>
                <select id="budget">
                    <option value="Cheap ($)">Cheap ($)</option>
                    <option value="Moderate ($$)" selected>Moderate ($$)</option>
                    <option value="Premium ($$$)">Premium ($$$)</option>
                </select>
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
                    <p>Your Hyper-Personalized 7-Day Synchronized Schedule</p>
                </div>
                <div id="statusBadge" class="badge-status">Ready</div>
            </div>

            <div id="spinner" class="spinner-container">
                <div class="spinner"></div>
                <h3 style="color: #00e5ff; margin-bottom: 5px;">🗓️ Synchronizing your week (Mon-Sun)...</h3>
                <p style="color: #aaa;">Generating customized workouts, meals, and budget groceries with AI...</p>
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
        async function generatePlan() {
            const btn = document.getElementById('generateBtn');
            const spinner = document.getElementById('spinner');
            const placeholder = document.getElementById('placeholder');
            const resultsArea = document.getElementById('resultsArea');
            const statusBadge = document.getElementById('statusBadge');
            const daysContainer = document.getElementById('daysContainer');
            const groceryCard = document.getElementById('groceryCard');

            btn.disabled = true;
            placeholder.style.display = 'none';
            resultsArea.style.display = 'none';
            spinner.style.display = 'block';
            statusBadge.innerText = 'Generating...';

            const payload = {
                apiKey: document.getElementById('apiKey').value,
                model: document.getElementById('modelOption').value,
                demoMode: document.getElementById('demoMode').checked,
                gender: document.getElementById('gender').value,
                age: document.getElementById('age').value,
                weight: document.getElementById('weight').value,
                height: document.getElementById('height').value,
                goal: document.getElementById('goal').value,
                equipment: document.getElementById('equipment').value,
                cuisine: document.getElementById('cuisine').value,
                budget: document.getElementById('budget').value,
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
                    alert(data.error || 'Failed to generate plan.');
                    statusBadge.innerText = 'Error';
                    placeholder.style.display = 'block';
                } else {
                    // Render Day Cards
                    daysContainer.innerHTML = '';
                    data.days.forEach(day => {
                        const card = document.createElement('div');
                        card.className = 'day-card';
                        card.innerHTML = `
                            <div class="day-title">🗓️ ${day.day}</div>
                            <div class="day-columns">
                                <div class="col-workout">
                                    <span class="col-header">🏋️ WORKOUT</span>
                                    <div class="markdown-content">${marked.parse(day.workout)}</div>
                                </div>
                                <div class="col-meal">
                                    <span class="col-header">🥗 MEALS</span>
                                    <div class="markdown-content">${marked.parse(day.meal)}</div>
                                </div>
                            </div>
                        `;
                        daysContainer.appendChild(card);
                    });

                    // Render Grocery Card
                    groceryCard.innerHTML = marked.parse(data.grocery);

                    resultsArea.style.display = 'grid';
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
    api_key = data.get("apiKey") or os.environ.get("GROQ_API_KEY")
    
    # Check secrets.toml as local fallback if available
    if not api_key:
        try:
            import toml
            if os.path.exists(".streamlit/secrets.toml"):
                secrets = toml.load(".streamlit/secrets.toml")
                api_key = secrets.get("GROQ_API_KEY")
        except Exception:
            pass

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
        return jsonify({"error": "Failed to parse AI output. Please retry."}), 500

    return jsonify({
        "days": days,
        "grocery": grocery,
        "source": source
    })

# For local development
if __name__ == "__main__":
    app.run(debug=True, port=5000)
