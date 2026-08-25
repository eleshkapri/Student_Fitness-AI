"""
StudentFit AI — LLM Client & Utility Functions
Provides Groq model completions with failover cascade, simulation mock mode, response parser, and PDF generation.
"""

import os
import re
import time
from groq import Groq
from planner.prompt_builder import build_student_prompt

# Candidate models ordered by reliability & speed
CANDIDATE_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "groq/compound-mini",
    "groq/compound",
    "qwen/qwen3.6-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

def get_api_key(provided_key: str = None) -> str:
    """Resolves Groq API key from parameter, environment, or Streamlit secrets."""
    if provided_key and provided_key.strip():
        return provided_key.strip()
    
    env_key = os.environ.get("GROQ_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
    
    try:
        import toml
        secrets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".streamlit", "secrets.toml")
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            key = secrets.get("GROQ_API_KEY")
            if key and key.strip():
                return key.strip()
    except Exception:
        pass
        
    return None

def calculate_macros(age, gender, weight, weight_unit='kg', height=170, height_unit='cm', goal='Build Muscle') -> dict:
    """Calculates student BMR, TDEE, target calories, and daily macronutrient split."""
    try:
        age = float(age)
        w = float(weight)
        h = float(height)
        
        kg = w * 0.453592 if str(weight_unit).lower() == 'lbs' else w
        cm = h * 2.54 if str(height_unit).lower() == 'ft/in' else h
        
        if str(gender).lower() == 'female':
            bmr = (10 * kg) + (6.25 * cm) - (5 * age) - 161
        else:
            bmr = (10 * kg) + (6.25 * cm) - (5 * age) + 5
            
        tdee = bmr * 1.4
        goal_lower = str(goal).lower()
        if 'muscle' in goal_lower:
            target_calories = round(tdee + 350)
            protein_g = round(kg * 2.0)
        elif 'lose' in goal_lower or 'shredded' in goal_lower:
            target_calories = round(tdee - 400)
            protein_g = round(kg * 2.2)
        else:
            target_calories = round(tdee)
            protein_g = round(kg * 1.6)
            
        fats_g = round((target_calories * 0.25) / 9)
        carbs_g = max(round((target_calories - (protein_g * 4 + fats_g * 9)) / 4), 50)
        
        return {
            "bmr": round(bmr),
            "tdee": round(tdee),
            "target_calories": target_calories,
            "protein_g": protein_g,
            "carbs_g": carbs_g,
            "fats_g": fats_g,
            "water_liters": round(kg * 0.035, 1)
        }
    except Exception:
        return {
            "bmr": 1600,
            "tdee": 2200,
            "target_calories": 2400,
            "protein_g": 130,
            "carbs_g": 280,
            "fats_g": 65,
            "water_liters": 2.8
        }

def parse_ai_response(full_text: str):
    """Splits full AI output into 7 daily plans and grocery checklist."""
    if not full_text:
        return [], ""

    grocery_text = ""
    grocery_match = re.search(r'###\s*WEEKLY GROCERY & BUDGET.*', full_text, flags=re.DOTALL | re.IGNORECASE)
    if grocery_match:
        grocery_text = grocery_match.group(0)
        content_for_days = full_text[:grocery_match.start()]
    else:
        content_for_days = full_text

    day_blocks = re.split(r'(?=Day:\s*)', content_for_days)
    day_plans = []
    
    for block in day_blocks:
        if not block.strip():
            continue
        day_match = re.search(r'Day:\s*(.+)', block)
        if day_match:
            day_name = day_match.group(1).strip()
            
            workout_part = ""
            meal_part = ""
            
            w_idx = block.find("Workout:")
            m_idx = block.find("Meal:")
            
            if w_idx != -1 and m_idx != -1:
                if w_idx < m_idx:
                    workout_part = block[w_idx + len("Workout:"):m_idx].strip()
                    meal_part = block[m_idx + len("Meal:"):].strip()
                else:
                    meal_part = block[m_idx + len("Meal:"):w_idx].strip()
                    workout_part = block[w_idx + len("Workout:"):].strip()
            elif w_idx != -1:
                workout_part = block[w_idx + len("Workout:"):].strip()
            elif m_idx != -1:
                meal_part = block[m_idx + len("Meal:"):].strip()
                
            day_plans.append({
                "day": day_name,
                "workout": workout_part,
                "meal": meal_part
            })
            
    return day_plans, grocery_text

def generate_plan_mock(profile: dict) -> str:
    """Provides high-quality instant fallback response."""
    time.sleep(1.0)
    goal = profile.get("goal", "Build Muscle")
    cuisine = profile.get("cuisine", "Indian")
    gear = profile.get("equipment", "Full Gym")
    currency = profile.get("currency", "INR (₹)")
    
    return f"""Day: Monday
Workout:
* Target: Chest & Triceps ({gear} Edition)
* Exercise 1: Barbell Bench Press (or Weighted Push-ups) - 4 sets x 8-10 reps
* Exercise 2: Incline Dumbbell Press - 3 sets x 10-12 reps
* Exercise 3: Cable Chest Flyes - 3 sets x 12-15 reps
* Exercise 4: Parallel Bar Dips - 3 sets x 10-12 reps
* Exercise 5: Overhead Triceps Rope Extension - 3 sets x 12-15 reps
* Cardio/Core: 10 min HIIT Treadmill sprints (30s sprint / 30s walk)
Meal:
* Breakfast: Poha / Oatmeal with roasted peanuts, sliced banana, and 2 boiled eggs
* Lunch: Brown rice with high-protein spiced dal, sautéed spinach, and cucumber-tomato salad
* Snack: Roasted chickpeas (chana) with a glass of milk or soya milk
* Dinner: Grilled chicken breast (200g) or spiced Paneer (200g) with 2 whole wheat rotis and curd

Day: Tuesday
Workout:
* Target: Back & Biceps
* Exercise 1: Pull-ups / Lat Pulldown - 4 sets x 8-10 reps
* Exercise 2: Barbell Bent-Over Row - 4 sets x 8-10 reps
* Exercise 3: Seated Cable Row - 3 sets x 10-12 reps
* Exercise 4: Standing Barbell Biceps Curls - 3 sets x 10-12 reps
* Exercise 5: Incline Dumbbell Hammer Curls - 3 sets x 12-15 reps
* Cardio/Core: 3 sets of 45s Plank & Hanging Knee Raises
Meal:
* Breakfast: 3 whole scrambled eggs on whole wheat toast with sliced tomatoes
* Lunch: Lentil khichdi with mixed vegetables and 100g low-fat curd
* Snack: Whole apple with 2 tablespoons peanut butter
* Dinner: Soya chunk curry (70g dry) with 1 cup brown rice and green salad

Day: Wednesday
Workout:
* Target: Active Recovery & Exam Stress Relief
* Exercise 1: 30-minute brisk campus walk or light cycling
* Exercise 2: Full-body yoga flow for hip and spine mobility
* Exercise 3: Cat-Cow and Child's Pose - 3 rounds of 1 min
* Exercise 4: Foam rolling for thoracic spine and hamstrings
* Exercise 5: 10-minute box breathing meditation
* Cardio/Core: Low intensity steady state cardio
Meal:
* Breakfast: Overnight oats with chia seeds, banana, and a scoop of protein or Greek yogurt
* Lunch: Whole-wheat vegetable wrap with grilled paneer/tofu and mint chutney
* Snack: Handful of mixed almonds and walnuts with green tea
* Dinner: Light vegetable soup with 150g grilled chicken/fish or scrambled tofu & 2 rotis

Day: Thursday
Workout:
* Target: Legs & Glutes (Power & Stamina)
* Exercise 1: Barbell Back Squats (or Goblet Squats) - 4 sets x 8-10 reps
* Exercise 2: Romanian Deadlifts (RDLs) - 4 sets x 10-12 reps
* Exercise 3: Walking Lunges - 3 sets x 12 steps per leg
* Exercise 4: Leg Press / Bulgarian Split Squats - 3 sets x 10-12 reps
* Exercise 5: Standing Calf Raises - 4 sets x 15-20 reps
* Cardio/Core: 3 sets of 20 Abdominal Crunches & Russian Twists
Meal:
* Breakfast: Vegetable omelette (3 eggs) with 2 whole wheat toasts
* Lunch: Brown rice with rajma (kidney bean curry) and mixed greens
* Snack: 1 cup Greek yogurt topped with pumpkin seeds
* Dinner: Stir-fried tofu/paneer with bell peppers, broccoli, and steamed sweet potato

Day: Friday
Workout:
* Target: Shoulders & Abs (Hypertrophy)
* Exercise 1: Overhead Dumbbell Shoulder Press - 4 sets x 8-10 reps
* Exercise 2: Dumbbell Lateral Raises - 4 sets x 12-15 reps
* Exercise 3: Rear Delt Reverse Flyes - 3 sets x 15 reps
* Exercise 4: Barbell Shrugs - 3 sets x 12 reps
* Exercise 5: Cable Woodchoppers - 3 sets x 12 reps per side
* Cardio/Core: Hanging Leg Raises - 3 sets to failure
Meal:
* Breakfast: Peanut butter banana smoothie with 400ml milk and 40g oats
* Lunch: Chickpea (chole) curry with 1 cup brown rice and sliced cucumber
* Snack: 2 hard-boiled eggs with chaat masala and black coffee
* Dinner: Grilled chicken / paneer tikka with sautéed capsicum and 1 whole-wheat paratha

Day: Saturday
Workout:
* Target: Full Body Power & Conditioning
* Exercise 1: Trap Bar / Conventional Deadlifts - 4 sets x 6-8 reps
* Exercise 2: Dumbbell Incline Bench Press - 3 sets x 10 reps
* Exercise 3: Dumbbell Step-ups - 3 sets x 10 reps per leg
* Exercise 4: Push-up to Renegade Row - 3 sets x 10 reps
* Exercise 5: Face Pulls - 3 sets x 15 reps
* Cardio/Core: 12 min HIIT rowing machine or jump rope
Meal:
* Breakfast: Whole wheat pancakes topped with peanut butter and honey
* Lunch: Chicken or Soya biryani (cooked with minimal oil) with cucumber raita
* Snack: Sprouted moong bean salad with lemon, tomato, and onion
* Dinner: Spiced vegetable dal with 200g tofu/paneer and mixed steamed vegetables

Day: Sunday
Workout:
* Target: Rest, Mobility & Meal Prep Day
* Exercise 1: 20-minute gentle campus walk
* Exercise 2: Hamstring & Quad static stretching (10 mins)
* Exercise 3: Shoulder dislocates with resistance band (3 sets of 15)
* Exercise 4: 15 minutes mindfulness & deep breathing for semester mental clarity
Meal:
* Breakfast: Masala scrambled eggs or tofu scramble with toasted multigrain bread
* Lunch: Student meal-prep bowl (Brown rice, spiced chickpeas, spinach, curd)
* Snack: 1 glass sweet lassi / buttermilk or protein shake
* Dinner: Light vegetable khichdi or chicken clear soup with toasted pita bread

### WEEKLY GROCERY & BUDGET
#### 🛒 Weekly Student Grocery List (1 Person)
* **Proteins:** 1 Dozen Eggs (or 500g Tofu / Paneer / Chicken Breast)
* **Grains & Carbs:** 1 kg Brown Rice / Whole Wheat Flour, 500g Rolled Oats
* **Vegetables & Produce:** Onions, Tomatoes, Spinach, Cucumbers, Bananas, Apples
* **Pantry & Healthy Fats:** 1 Jar Peanut Butter, Chia seeds, Spices
#### 💡 Student Meal-Prep & Budget Tips
* **Cook Staples in Bulk:** Boil lentils and cook rice for 3 days at a time to save cooking time during class days.
* **Smart Hydration:** Carry a 1-liter reusable bottle; aim for 3 refills daily for peak brain function.
#### 💰 Estimated Weekly Budget
* **Estimated Total:** ₹800 – ₹1,200 INR (or approx. $12 – $18 USD)
* **Savings Tip:** Buying legumes, lentils, and oats in 1kg bulk bags reduces weekly costs by up to 30%.
"""

def generate_plan_real(profile: dict, api_key: str, chosen_model: str = "openai/gpt-oss-20b"):
    """Executes Groq API completion with model fallback cascade and timeout protection."""
    client = Groq(api_key=api_key, timeout=30.0)
    prompt = build_student_prompt(profile)
    
    if chosen_model in CANDIDATE_MODELS:
        models_to_try = [chosen_model] + [m for m in CANDIDATE_MODELS if m != chosen_model]
    else:
        models_to_try = CANDIDATE_MODELS
        
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
                temperature=0.4,
                max_tokens=4096,
            )
            content = response.choices[0].message.content
            if content and len(content.strip()) > 0:
                cleaned = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
                return cleaned, model_name
        except Exception as e:
            last_error = e
            continue
            
    return f"Error: {last_error}", None

def create_fitness_pdf(raw_text: str) -> bytes:
    """Generates a clean PDF binary for the fitness schedule."""
    try:
        from fpdf import FPDF
        
        class PDF(FPDF):
            def header(self):
                self.set_font('Helvetica', 'B', 14)
                self.set_text_color(255, 107, 84) # Coral
                self.cell(0, 10, 'StudentFit AI - Weekly Fitness & Nutrition Plan', align='C', new_x='LMARGIN', new_y='NEXT')
                self.ln(2)

            def footer(self):
                self.set_y(-15)
                self.set_font('Helvetica', 'I', 8)
                self.set_text_color(133, 130, 172)
                self.cell(0, 10, f'StudentFit AI | Page {self.page_no()}', align='C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        epw = pdf.epw
        
        replacements = {
            "₹": "Rs. ", "€": "EUR ", "£": "GBP ", "$": "USD ",
            "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", "**": ""
        }
        
        clean_text = raw_text or ""
        for key, val in replacements.items():
            clean_text = clean_text.replace(key, val)

        lines = clean_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                pdf.ln(2)
                continue
            
            safe_line = line.encode('latin-1', 'ignore').decode('latin-1')

            if safe_line.startswith('Day:') or safe_line.startswith('#'):
                pdf.ln(3)
                pdf.set_font("Helvetica", 'B', 12)
                pdf.set_text_color(255, 107, 84) # Coral
                pdf.cell(epw, 7, safe_line.replace('#', '').strip(), new_x="LMARGIN", new_y="NEXT")
            elif safe_line.startswith('Workout:') or safe_line.startswith('Meal:') or safe_line.startswith('GROCERY'):
                pdf.set_font("Helvetica", 'B', 10)
                pdf.set_text_color(156, 140, 255) # Lilac
                pdf.cell(epw, 6, safe_line, new_x="LMARGIN", new_y="NEXT")
            elif safe_line.startswith('*') or safe_line.startswith('-'):
                pdf.set_font("Helvetica", '', 9)
                pdf.set_text_color(40, 40, 40)
                pdf.multi_cell(epw, 5, "- " + safe_line[1:].strip(), new_x="LMARGIN", new_y="NEXT")
            else:
                pdf.set_font("Helvetica", '', 9)
                pdf.set_text_color(40, 40, 40)
                pdf.multi_cell(epw, 5, safe_line, new_x="LMARGIN", new_y="NEXT")
                
        return bytes(pdf.output())
    except Exception:
        return None
