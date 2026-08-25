"""
Prompt Builder for StudentFit AI Weekly Planner.
Constructs strictly structured prompts honoring student constraints.
"""

def build_student_prompt(profile: dict) -> str:
    """Constructs the prompt for 7-day student fitness & nutrition plan."""
    currency = profile.get('currency', 'INR (₹)')
    weight = profile.get('weight', 70)
    weight_unit = profile.get('weight_unit', 'kg')
    height = profile.get('height', 170)
    height_unit = profile.get('height_unit', 'cm')
    gender = profile.get('gender', 'Male')
    age = profile.get('age', 20)
    goal = profile.get('goal', 'Build Muscle')
    equipment = profile.get('equipment', 'Full Gym')
    cuisine = profile.get('cuisine', 'Indian')
    diet_type = profile.get('diet_type', 'Standard')
    budget = profile.get('budget', 'Moderate ($$)')
    cooking_skill = profile.get('cooking_skill', 'Basic Stove')

    return f"""
Act as an elite fitness coach and student budget nutrition specialist.
Student Profile:
- Age: {age} years old | Gender: {gender}
- Weight: {weight} {weight_unit} | Height: {height} {height_unit}
- Goal: {goal}
- Available Equipment: {equipment}
- Cuisine Preference: {cuisine} | Diet: {diet_type}
- Weekly Budget Tier: {budget} (Preferred Currency: {currency})
- Cooking Facility / Setup: {cooking_skill}

REQUIREMENTS:
1. Provide a comprehensive 7-DAY SCHEDULE (Monday through Sunday).
2. For EVERY day, output BOTH a tailored Workout Routine and Synchronized Meals matching the student's equipment and cooking skill.
3. At the end, output a complete Weekly Grocery Shopping List (1 Person) with realistic estimated costs in {currency} and practical student meal-prep tips.
4. Follow this EXACT plain-text delimiter format:

### DAY_START
Day: Monday
Workout:
* Target: [Muscle group or Focus]
* Exercise 1: [Name] - [Sets x Reps]
* Exercise 2: [Name] - [Sets x Reps]
* Exercise 3: [Name] - [Sets x Reps]
* Cardio/Core: [Details]
Meal:
* Breakfast: [Meal description with estimated protein/calories]
* Lunch: [Meal description with estimated protein/calories]
* Snack: [Budget student snack]
* Dinner: [Meal description with estimated protein/calories]
### DAY_END

(Repeat ### DAY_START to ### DAY_END for Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)

### GROCERY_START
#### 🛒 Weekly Student Grocery List (1 Person)
* **Proteins:** [Items with quantities and prices in {currency}]
* **Grains & Carbs:** [Items with quantities and prices in {currency}]
* **Produce & Veggies:** [Items with quantities and prices in {currency}]
* **Healthy Fats & Extras:** [Items with quantities and prices in {currency}]
#### 💡 Student Meal-Prep & Budget Tips
* [Tip 1 on bulk batch cooking to save study hours]
* [Tip 2 on smart hydration / protein optimization]
#### 💰 Estimated Weekly Budget
* **Estimated Cost:** [Total weekly cost in {currency}]
* **Savings Tip:** [Tip on buying bulk or seasonal alternatives]
### GROCERY_END
"""
