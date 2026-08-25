import os
import re
import time
from groq import Groq

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

def get_api_key(provided_key=None):
    """Resolves Groq API key from parameter, environment, or Streamlit secrets."""
    if provided_key and provided_key.strip():
        return provided_key.strip()
    
    env_key = os.environ.get("GROQ_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()
    
    # Try .streamlit/secrets.toml
    try:
        import toml
        secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            key = secrets.get("GROQ_API_KEY")
            if key and key.strip():
                return key.strip()
    except Exception:
        pass
        
    return None

def build_prompt(profile):
    """Constructs a strictly structured prompt for 7-day student fitness & nutrition."""
    return f"""
Act as an elite fitness trainer and budget nutrition expert for university students.
Student Profile:
- Age: {profile.get('age', 20)} years old, Gender: {profile.get('gender', 'Male')}
- Weight: {profile.get('weight', 70)} kg, Height: {profile.get('height', 170)} cm
- Goal: {profile.get('goal', 'Build Muscle')}
- Available Equipment: {profile.get('equipment', 'Full Gym')}
- Cuisine: {profile.get('cuisine', 'Indian')}, Diet: {profile.get('diet_type', 'Standard')}
- Weekly Budget Tier: {profile.get('budget', 'Moderate ($$)')}
- Cooking Skill / Setup: {profile.get('cooking_skill', 'Basic Stove')}

TASK: Create a complete 7-Day Plan (Monday through Sunday) with aligned workouts and meals, followed by a smart grocery shopping list and budget breakdown.

STRICT DELIMITER FORMAT:
Separate each day block with "|||".
Inside each day block, strictly use the headers "Day:", "Workout:", and "Meal:".
After Sunday's block, add "|||" followed by "GROCERY".

Example:
Day: Monday
Workout:
* **Target:** Chest & Triceps
* **Exercise 1:** Dumbbell Bench Press (3 sets x 10 reps)
* **Exercise 2:** Pushups (3 sets x 15 reps)
* **Cardio/Core:** Plank (3 sets x 45s)
Meal:
* **Breakfast:** Oatmeal with sliced banana & peanut butter
* **Lunch:** Brown rice, spiced lentils (Dal), and cucumber salad
* **Snack:** Boiled eggs / Roasted chickpeas
* **Dinner:** Mixed vegetable curry with 2 whole wheat rotis
|||
Day: Tuesday
...
|||
GROCERY
#### 🛒 Weekly Student Shopping List
* 1 Dozen Eggs (or 500g Tofu)
* 1 kg Rice / Whole Wheat Flour
* 500g Rolled Oats
* 500g Lentils / Chickpeas
* 1 Jar Peanut Butter
* Assorted Seasonal Vegetables
#### 💡 Student Meal-Prep & Fitness Tips
* Prepare grains and boiled lentils in batches on Sunday evening.
* Stay hydrated with at least 2.5–3 liters of water daily.
#### 💰 Estimated Weekly Budget
* Cost: In regional currency corresponding to {profile.get('cuisine', 'selected')} cuisine (e.g. ₹800–₹1200 INR for Indian, $15–$25 USD for Global, €15–€25 EUR for Mediterranean).
* USD Equivalent: Approx. $15 – $25 USD per week.

Begin output immediately with 'Day: Monday'.
"""

def parse_ai_response(text):
    """
    Parses LLM output with regex resilience to variations in markdown,
    bolding, casing, and trailing tokens.
    """
    days = []
    grocery_section = "No grocery list generated."
    
    if not text:
        return days, grocery_section
        
    # Strip any reasoning or think tokens
    cleaned_text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    
    # Split by standard block delimiter
    blocks = cleaned_text.split("|||")
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Match day blocks
        if re.search(r"(?:Day|Day\s*\d+):", block, re.IGNORECASE):
            try:
                # Extract Day Title
                day_match = re.search(r"(?:Day|Day\s*\d+):\s*([^\n\r*#]+)", block, re.IGNORECASE)
                day_line = day_match.group(1).strip() if day_match else "Daily Schedule"
                
                # Extract Workout Section
                workout_match = re.search(
                    r"(?:\*{0,2}Workout\*{0,2}):\s*(.*?)(?=(?:\*{0,2}Meal\*{0,2}):|$)",
                    block,
                    re.DOTALL | re.IGNORECASE
                )
                workout_text = workout_match.group(1).strip() if workout_match else "Rest / Active Recovery"
                
                # Extract Meal Section
                meal_match = re.search(
                    r"(?:\*{0,2}Meal\*{0,2}):\s*(.*)",
                    block,
                    re.DOTALL | re.IGNORECASE
                )
                meal_text = meal_match.group(1).strip() if meal_match else "Standard Balanced Student Meals"
                
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
    """Realistic mock output for instant offline demo mode."""
    time.sleep(1.0)
    cuisine = profile.get('cuisine', 'Indian')
    goal = profile.get('goal', 'Fitness')
    
    return f"""
Day: Monday
Workout:
* **Focus:** Upper Body Strength (Push)
* **Exercise 1:** Standard Pushups (3 sets x 12 reps)
* **Exercise 2:** Incline Pike Pushups (3 sets x 10 reps)
* **Core:** High Plank Hold (3 sets x 45 sec)
Meal:
* **Breakfast:** Rolled oats porridge with banana, chia seeds & splash of milk
* **Lunch:** Warm spiced lentils (Dal), 1 cup steamed rice & fresh cucumber salad
* **Snack:** Handful of roasted peanuts / almonds
* **Dinner:** Grilled tofu/paneer with sautéed bell peppers & 2 whole-wheat flatbreads
|||
Day: Tuesday
Workout:
* **Focus:** Lower Body & Leg Power
* **Exercise 1:** Bodyweight Squats (4 sets x 15 reps)
* **Exercise 2:** Walking Lunges (3 sets x 12 reps per leg)
* **Cardio:** 15-minute brisk jog / stair climbing
Meal:
* **Breakfast:** 2 boiled eggs / Spiced besan chilla with mint chutney
* **Lunch:** Chickpea salad bowl with diced tomatoes, onions, lemon juice & olive oil
* **Snack:** 1 Fresh seasonal fruit (Apple / Orange)
* **Dinner:** Mixed vegetable & lentil stew with brown rice
|||
Day: Wednesday
Workout:
* **Focus:** Upper Body (Pull & Posture)
* **Exercise 1:** Doorframe Rows / Resistance Band Pulls (3 sets x 12 reps)
* **Exercise 2:** Superman Extensions (3 sets x 15 reps)
* **Core:** Bicycle Crunches (3 sets x 20 reps)
Meal:
* **Breakfast:** Peanut butter on 2 whole-wheat toast slices with sliced banana
* **Lunch:** Soybean / Chicken chunks cooked with onions, turmeric, served with rice
* **Snack:** Roasted chana / Green tea
* **Dinner:** Vegetable Khichdi / Quinoa bowl with homemade yogurt (curd)
|||
Day: Thursday
Workout:
* **Focus:** High-Intensity Cardio & Core Burn
* **Exercise 1:** Jumping Jacks (4 sets x 30 sec)
* **Exercise 2:** Mountain Climbers (3 sets x 20 reps)
* **Mobility:** 10 minutes deep hip & shoulder stretching
Meal:
* **Breakfast:** Fruit & yogurt bowl topped with oats & honey
* **Lunch:** Rajma (Kidney bean curry) with steamed brown rice
* **Snack:** Handful of roasted sunflower / pumpkin seeds
* **Dinner:** Stir-fried seasonal vegetables with tofu / scrambled eggs
|||
Day: Friday
Workout:
* **Focus:** Full Body Conditioning
* **Exercise 1:** Burpees / Step-back burpees (3 sets x 10 reps)
* **Exercise 2:** Glute Bridges (3 sets x 15 reps)
* **Core:** Side Planks (3 sets x 30 sec per side)
Meal:
* **Breakfast:** Scrambled eggs or Paneer bhurji with toasted bread
* **Lunch:** Lentil soup with roasted sweet potato & green salad
* **Snack:** Buttermilk / Protein shake
* **Dinner:** Whole-wheat wrap with spiced beans, shredded cabbage & salsa
|||
Day: Saturday
Workout:
* **Focus:** Active Recovery & Outdoor Movement
* **Activity:** 30–40 minute brisk nature walk / easy cycling
* **Flexibility:** Full body mobility routine (Hamstrings, Spine, Shoulders)
Meal:
* **Breakfast:** Homemade high-protein oats pancake with honey
* **Lunch:** Mediterranean / Indian lentil pilaf with fresh diced cucumber & lemon
* **Snack:** Roasted makhana (foxnuts) or boiled edamame
* **Dinner:** Light vegetable soup with garlic toast
|||
Day: Sunday
Workout:
* **Focus:** Complete Rest & Recharge
* **Recovery:** Deep breathing, hydration, foam rolling or gentle walking
Meal:
* **Breakfast:** Mashed avocado / peanut butter toast with boiled eggs
* **Lunch:** Weekend batch meal-prep bowl (Rice, Dal, Mixed Greens)
* **Snack:** Seasonal fruit smoothie
* **Dinner:** Light comforting soup / grilled sandwich
|||
GROCERY
#### 🛒 Weekly Student Grocery List (1 Person)
* **Proteins:** 1 Dozen Eggs (or 500g Tofu / Paneer / Chicken Breast)
* **Grains:** 1 kg Brown Rice / Whole Wheat Flour, 500g Rolled Oats
* **Legumes:** 500g Spiced Lentils (Dal), 500g Chickpeas / Kidney Beans
* **Healthy Fats:** 1 Jar Peanut Butter, Small pack Chia/Flax Seeds
* **Produce:** Onions, Tomatoes, Cucumbers, Spinach, Bananas, Apples
#### 💡 Student Meal-Prep & Budget Tips
* **Cook Staples in Bulk:** Boil lentils and cook rice for 3 days at a time to save electricity and study hours.
* **Smart Hydration:** Carry a 1-liter reusable bottle; aim for 3 refills daily.
#### 💰 Estimated Weekly Budget
* **Estimated Cost:** ₹800 – ₹1,200 INR (or approx. $15 – $20 USD)
* **Savings Tip:** Buying legumes and oats in 1kg bulk bags reduces weekly costs by up to 25%.
"""

def generate_plan_real(profile, api_key, chosen_model="openai/gpt-oss-20b"):
    """Executes Groq API completion with model fallback cascade and timeout protection."""
    client = Groq(api_key=api_key, timeout=30.0)
    prompt = build_prompt(profile)
    
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
