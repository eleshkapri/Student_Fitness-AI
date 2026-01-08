import streamlit as st
from groq import Groq
import requests
from streamlit_lottie import st_lottie
import time
import re

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="StudentFit AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD ASSETS ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_fitness = load_lottieurl("https://lottie.host/5a8e0108-0118-4981-b54c-1296c0542368/jY8yHnN2Fm.json")

# --- CUSTOM CSS (NEON + ALIGNED CARDS) ---
st.markdown("""
    <style>
    /* Global Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #121212;
        border-right: 1px solid #333;
    }

    /* GLASSMORPHISM DAY CARD */
    .day-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .day-card:hover {
        border-color: rgba(0, 229, 255, 0.5);
        transform: translateY(-2px);
    }
    
    /* GROCERY CARD (Right Side) */
    .grocery-card {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid #FFD700;
        border-radius: 15px;
        padding: 20px;
        height: 100%;
        text-align: left;
    }

    /* Day Headers (Monday, Tuesday...) - GOLD COLOR */
    h3 {
        color: #FFD700 !important; /* Gold */
        font-size: 1.5rem !important;
        margin-top: 0px !important;
        margin-bottom: 15px !important;
        text-transform: uppercase;
        border-bottom: 1px solid rgba(255, 215, 0, 0.3);
        padding-bottom: 5px;
    }

    /* Column Headers (Workout/Diet) */
    .col-header {
        color: #00e5ff;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 10px;
        display: block;
    }

    /* List Items Styling */
    ul { list-style-type: none; padding-left: 0; }
    li { margin-bottom: 6px; font-size: 1rem; color: #e0e0e0; }
    strong { color: #fff; font-weight: 600; }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 18px;
        margin-top: 20px;
    }
    .stButton>button:hover {
        box-shadow: 0 0 20px rgba(255, 75, 43, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def parse_ai_response(text):
    """
    Parses the raw AI text into a structured dictionary.
    Expected format blocks: "Day: Monday... Workout: ... Meal: ..."
    """
    days = []
    grocery_section = "No grocery list generated."
    
    # Split by the separator we asked the AI to use
    blocks = text.split("|||")
    
    for block in blocks:
        block = block.strip()
        if block.startswith("Day:"):
            # Parse Day Block
            try:
                # Extract Day Name
                day_line = re.search(r"Day:\s*(.*)", block).group(1)
                
                # Extract Workout (between Workout: and Meal:)
                workout_match = re.search(r"Workout:\s*(.*?)(?=Meal:)", block, re.DOTALL)
                workout_text = workout_match.group(1).strip() if workout_match else "Rest"
                
                # Extract Meal (from Meal: to end)
                meal_match = re.search(r"Meal:\s*(.*)", block, re.DOTALL)
                meal_text = meal_match.group(1).strip() if meal_match else "Standard Diet"
                
                days.append({
                    "day": day_line,
                    "workout": workout_text,
                    "meal": meal_text
                })
            except:
                continue
                
        elif block.startswith("GROCERY"):
            grocery_section = block.replace("GROCERY", "").strip()
            
    return days, grocery_section

def generate_plan_mock(profile):
    time.sleep(1.5)
    # Mock data in the new split format
    return """
    Day: Monday
    Workout: * **Push:** Pushups (3x12)\n* **Core:** Plank (45s)
    Meal: * **Breakfast:** Oats\n* **Lunch:** Lentils
    |||
    Day: Tuesday
    Workout: * **Legs:** Squats (3x15)\n* **Cardio:** Jog (15m)
    Meal: * **Breakfast:** Eggs\n* **Lunch:** Rice
    |||
    GROCERY
    #### 🛒 Shopping List
    * 1 Dozen Eggs
    * 1kg Rice
    * 500g Oats
    #### 💰 Estimated Budget
    * Approx. ₹800 - ₹1200 INR (Indian Pricing)
    * Approx. $15 - $20 USD (Global Standard)
    """

def generate_plan_real(profile, api_key):
    try:
        client = Groq(api_key=api_key)
        
        # --- PROMPT DESIGNED FOR PARSING ---
        prompt = f"""
        Act as a fitness coach for a student.
        Profile: {profile['age']}y/o, {profile['gender']}, {profile['weight']}kg.
        Goal: {profile['goal']}. Equipment: {profile['equipment']}.
        Diet: {profile['diet_type']} ({profile['cuisine']}), Budget: {profile['budget']}.
        Cooking: {profile['cooking_skill']}.

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
        
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ StudentFit Setup")
    
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        st.success("✅ AI Connected")
        use_simulation = st.checkbox("Demo Mode", value=False)
    else:
        api_key = st.text_input("Groq API Key", type="password")
        use_simulation = st.checkbox("Demo Mode", value=True if not api_key else False)

    st.markdown("---")
    
    st.markdown("### 🏃‍♂️ Bio-Data")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", 40, 150, 70)
    with col_s2:
        age = st.number_input("Age", 16, 40, 20)
        height = st.number_input("Height (cm)", 140, 220, 170)

    st.markdown("### 🎯 Goals")
    goal = st.selectbox("Goal", ["Lose Weight", "Build Muscle", "Get Shredded", "Exam Stress Relief"])
    equipment = st.selectbox("Gear", ["No Equipment (Dorm)", "Dumbbells Only", "Full Gym"])
    
    st.markdown("### 🥑 Kitchen")
    cuisine = st.selectbox("Cuisine", ["Indian", "Global", "Mediterranean", "Asian", "Vegan"])
    budget = st.select_slider("Budget", options=["Cheap ($)", "Moderate ($$)", "Premium ($$$)"])
    cooking_skill = st.select_slider("Cooking Skill", options=["Microwave Only", "Basic Stove", "Full Chef"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("🚀 GENERATE WEEKLY PLAN")

# --- MAIN PAGE ---
col_header, col_anim = st.columns([2, 1])

with col_header:
    st.title("StudentFit AI ⚡")
    st.markdown("#### Your 7-Day Aligned Schedule")
    if not generate_btn:
        st.info("👈 Fill out the sidebar. We will generate a synchronized Workout & Meal plan.")

with col_anim:
    if lottie_fitness:
        st_lottie(lottie_fitness, height=150, key="anim_top")

st.markdown("---")

# --- RESULTS SECTION ---
if generate_btn:
    user_profile = {
        "age": age, "weight": weight, "height": height, "gender": gender, 
        "goal": goal, "equipment": equipment, "cuisine": cuisine, 
        "diet_type": "Standard", "budget": budget, "cooking_skill": cooking_skill
    }
    
    with st.spinner('🗓️ Synchronizing your week (Mon-Sun)...'):
        if use_simulation or not api_key:
            full_response = generate_plan_mock(user_profile)
            source = "Simulation"
        else:
            full_response = generate_plan_real(user_profile, api_key)
            source = "Llama 3 (Groq)"

    # PARSE THE RESPONSE
    day_plans, grocery_text = parse_ai_response(full_response)
    
    # LAYOUT: LEFT (Schedule) | RIGHT (Grocery)
    main_col, side_col = st.columns([2.5, 1])
    
    with main_col:
        # Loop through each day and create a row
        if not day_plans:
            st.error("AI output format error. Please try again.")
            # st.write(full_response) # Debug
        
        for plan in day_plans:
            # Create a Card Container for the day
            st.markdown(f"""
            <div class="day-card">
                <h3>🗓️ {plan['day']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Create 2 columns INSIDE the day row
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown('<span class="col-header">🏋️ WORKOUT</span>', unsafe_allow_html=True)
                st.markdown(plan['workout'])
                
            with c2:
                st.markdown('<span class="col-header">🥗 MEALS</span>', unsafe_allow_html=True)
                st.markdown(plan['meal'])
            
            st.markdown("---") # Visual separator between days

    with side_col:
        # --- FIX: FORMAT THE GROCERY LIST AS HTML ---
        # The AI gives Markdown (* Item), but inside a custom DIV, Markdown breaks.
        # We manually convert the text to HTML for perfect rendering.
        
        # 1. Convert Headers (#### Text -> html h4)
        formatted_grocery = re.sub(r'####\s*(.*)', r'<h4 style="color: #FFD700; border-bottom: 1px solid #FFD700; padding-bottom: 5px; margin-top: 15px;">\1</h4>', grocery_text)
        
        # 2. Convert Bold Text (**text** -> strong)
        formatted_grocery = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: white;">\1</strong>', formatted_grocery)
        
        # 3. Convert List Items (* Item -> div with dot)
        # We replace the newline+asterisk pattern with a styled div
        formatted_grocery = re.sub(r'\n\*\s*(.*)', r'<div style="margin-bottom: 5px; color: #e0e0e0;">• \1</div>', formatted_grocery)
        
        # 4. Handle first item if it doesn't have a newline before it
        formatted_grocery = re.sub(r'^\*\s*(.*)', r'<div style="margin-bottom: 5px; color: #e0e0e0;">• \1</div>', formatted_grocery)

        # 5. Clean up remaining newlines
        formatted_grocery = formatted_grocery.replace("\n", "")

        st.markdown(f"""
        <div class="grocery-card">
            {formatted_grocery}
        </div>
        """, unsafe_allow_html=True)

    st.success(f"Generated successfully using {source}")