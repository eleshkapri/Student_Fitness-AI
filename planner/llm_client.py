"""
LLM Client for StudentFit AI Weekly Planner.
Handles model execution with Groq, fallback cascades, parsing, and PDF creation.
"""

import os
import re
from groq import Groq
from planner.prompt_builder import build_student_prompt

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
    
    # Try .streamlit/secrets.toml
    try:
        import toml
        secrets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".streamlit", "secrets.toml")
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            key = secrets.get("GROQ_API_KEY")
            if key and key.strip():
                return key.strip()
    except Exception:
        pass
        
    return None

def parse_ai_response(raw_text: str):
    """Parses delimiters into daily schedule cards and grocery summary."""
    if not raw_text:
        return [], ""
        
    days = []
    day_blocks = re.findall(r'### DAY_START(.*?)### DAY_END', raw_text, re.DOTALL)
    
    for block in day_blocks:
        day_match = re.search(r'Day:\s*(.*)', block)
        day_name = day_match.group(1).strip() if day_match else "Schedule"
        
        workout_match = re.search(r'Workout:\s*(.*?)(?=Meal:|$)', block, re.DOTALL)
        workout_text = workout_match.group(1).strip() if workout_match else "Rest & Active Recovery"
        
        meal_match = re.search(r'Meal:\s*(.*)', block, re.DOTALL)
        meal_text = meal_match.group(1).strip() if meal_match else "Balanced Student Nutrition"
        
        days.append({
            "day": day_name,
            "workout": workout_text,
            "meal": meal_text
        })
        
    grocery_match = re.search(r'### GROCERY_START(.*?)### GROCERY_END', raw_text, re.DOTALL)
    grocery_text = grocery_match.group(1).strip() if grocery_match else ""
    
    if not grocery_text and "#### 🛒" in raw_text:
        grocery_text = raw_text[raw_text.find("#### 🛒"):]

    return days, grocery_text

def generate_plan_mock(profile: dict) -> str:
    """Generates instant mock schedule when in demo mode or without API key."""
    currency = profile.get('currency', 'INR (₹)')
    sym = currency.split(' ')[0]
    
    return f"""
### DAY_START
Day: Monday
Workout:
* Target: Chest & Triceps (Hypertrophy)
* Exercise 1: Barbell / Dumbbell Flat Press - 4 sets x 8-10 reps
* Exercise 2: Incline Dumbbell Press / Push-ups - 3 sets x 10-12 reps
* Exercise 3: Dips (Bench / Parallel Bars) - 3 sets x 12 reps
* Cardio/Core: 10 min High-Intensity Interval Sprint / Hanging Knee Raises
Meal:
* Breakfast: Oats porridge with peanut butter, banana & 2 boiled eggs (approx. 25g protein)
* Lunch: Brown rice with high-protein lentils (dal), roasted paneer/chicken & green salad
* Snack: Roasted chickpeas (chana) or fruit smoothie with nuts
* Dinner: 2 Whole-wheat rotis / flatbreads with stir-fried tofu/egg curry & steamed spinach
### DAY_END

### DAY_START
Day: Tuesday
Workout:
* Target: Back & Biceps (Pull Power)
* Exercise 1: Lat Pulldowns or Pull-ups - 4 sets x 8-10 reps
* Exercise 2: Bent-Over Dumbbell Rows - 3 sets x 10 reps
* Exercise 3: Standing Dumbbell Bicep Curls - 3 sets x 12 reps
* Cardio/Core: 15 min Campus brisk walk / 3 min Plank hold
Meal:
* Breakfast: Scrambled eggs or tofu bhurji with whole-wheat toast & sliced apples
* Lunch: Chickpea and kidney bean bowl with brown rice & lemon-cucumber relish
* Snack: Handful of almonds/peanuts and green tea for exam focus
* Dinner: Grilled chicken breast or soya chunk curry with steamed rice & curd
### DAY_END

### DAY_START
Day: Wednesday
Workout:
* Target: Legs & Core (Foundation)
* Exercise 1: Barbell / Goblet Squats - 4 sets x 10-12 reps
* Exercise 2: Romanian Dumbbell Deadlifts - 3 sets x 10 reps
* Exercise 3: Walking Lunges - 3 sets x 12 steps per leg
* Cardio/Core: Standing Calf Raises & Bicycle Crunches - 3 sets x 20 reps
Meal:
* Breakfast: Peanut butter banana oatmeal bowl with chia seeds
* Lunch: High-protein soya chunks pulao / chicken fried rice with salad
* Snack: Greek yogurt or cottage cheese with roasted pumpkin seeds
* Dinner: Lentil soup (dal tadka) with 2 rotis and sautéed mixed greens
### DAY_END

### DAY_START
Day: Thursday
Workout:
* Target: Shoulders & Upper Traps
* Exercise 1: Overhead Dumbbell Press - 4 sets x 8-10 reps
* Exercise 2: Dumbbell Lateral Raises - 4 sets x 12-15 reps (Strict form)
* Exercise 3: Face Pulls / Reverse Flyes - 3 sets x 15 reps
* Cardio/Core: 10 min skipping rope / Russian twists
Meal:
* Breakfast: 3 Egg omelet with spinach and mushrooms + 2 slices toast
* Lunch: Quinoa or brown rice with black beans, sweet corn & grilled protein
* Snack: Boiled egg or fruit chaat with toasted peanuts
* Dinner: Paneer / Chicken stir fry with bell peppers and 2 rotis
### DAY_END

### DAY_START
Day: Friday
Workout:
* Target: Arms & Conditioning (Biceps, Triceps, Core)
* Exercise 1: Close-Grip Push-ups / Skull Crushers - 3 sets x 12 reps
* Exercise 2: Hammer Curls - 3 sets x 12 reps
* Exercise 3: Cable Pushdowns / Diamond Push-ups - 3 sets x 15 reps
* Cardio/Core: Ab Rollers / Leg Raises - 3 sets x 15 reps
Meal:
* Breakfast: Overnight oats with milk/soy milk, chia seeds & sliced fruit
* Lunch: Mixed bean chili with rice and cucumber salad
* Snack: 1 glass sattu drink or protein shake with almonds
* Dinner: Egg or paneer wrap in whole-wheat roti with mint chutney
### DAY_END

### DAY_START
Day: Saturday
Workout:
* Target: Full Body Athletic Conditioning & Calisthenics
* Exercise 1: Bodyweight / Weighted Pull-ups - 3 sets to failure
* Exercise 2: Bodyweight Squats to Jump Squats - 3 sets x 15 reps
* Exercise 3: Push-up pyramid (10, 8, 6, 4, 2 reps)
* Cardio/Core: 20 min campus jog or swim
Meal:
* Breakfast: Sprouted moong dal salad with tomatoes, onions and lemon + 2 boiled eggs
* Lunch: Hearty vegetable biryani with curd (raita) and roasted chicken/soya
* Snack: Toasted whole grain bread with peanut butter
* Dinner: Baked sweet potato, sautéed greens & scrambled eggs / tofu
### DAY_END

### DAY_START
Day: Sunday
Workout:
* Target: Active Recovery, Mobility & Exam De-stress
* Exercise 1: Deep Hip and Shoulder Mobility Stretches (15 min)
* Exercise 2: Light campus walk or cycling (30 min)
* Cardio/Core: 10 min Box Breathing & Mindfulness Meditation
Meal:
* Breakfast: Healthy banana pancakes with honey & milk
* Lunch: Balanced weekend feast: Brown rice, yellow dal, roasted potatoes & paneer/chicken
* Snack: Fresh seasonal fruit (apple, orange, banana)
* Dinner: Light vegetable soup with 2 toasted whole-grain sandwiches
### DAY_END

### GROCERY_START
#### 🛒 Weekly Student Grocery List (1 Person)
* **Proteins:** 1 Dozen Eggs ({sym} 120-180), 500g Chicken Breast / Paneer / Tofu ({sym} 150-250), 500g Soya Chunks ({sym} 50)
* **Grains & Carbs:** 1 kg Brown Rice / Whole Wheat Flour ({sym} 70-100), 500g Rolled Oats ({sym} 90)
* **Legumes & Pulses:** 500g Yellow Moong Dal, 500g Chickpeas / Kala Chana ({sym} 110)
* **Healthy Fats:** 1 Jar Natural Peanut Butter ({sym} 150), Seeds / Cooking Oil ({sym} 80)
* **Produce & Greens:** 1kg Onions, 1kg Tomatoes, Spinach, Bananas, Apples ({sym} 160-220)
#### 💡 Student Meal-Prep & Budget Tips
* **Cook Staples in Bulk:** Boil lentils and cook rice for 3 days at a time to save cooking fuel and study hours.
* **Smart Hydration:** Carry a 1-liter reusable bottle; aim for 3 refills daily for cognitive retention.
#### 💰 Estimated Weekly Budget
* **Estimated Cost:** {sym} 850 – {sym} 1,200 (Approx. $12 – $18 USD)
* **Savings Tip:** Buying legumes, oats, and rice in 1kg bulk bags reduces weekly grocery costs by up to 25%.
### GROCERY_END
"""

def generate_plan_real(profile: dict, api_key: str, chosen_model: str = "openai/gpt-oss-20b"):
    """Executes Groq API completion with model fallback cascade."""
    client = Groq(api_key=api_key, timeout=35.0)
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

def create_fitness_pdf(raw_text: str):
    """Generates an A4 PDF binary for the weekly fitness schedule."""
    try:
        from fpdf import FPDF
        
        class PDF(FPDF):
            def header(self):
                self.set_font('Helvetica', 'B', 14)
                self.set_text_color(255, 107, 84) # Coral accent
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
                pdf.set_text_color(255, 107, 84)
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
