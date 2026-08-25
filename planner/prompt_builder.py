"""
StudentFit AI — Prompt Builder
Constructs structured LLM prompts driving workout, nutrition, and budget grocery plans.
"""

def build_student_prompt(profile: dict) -> str:
    """Constructs a strictly structured prompt for 7-day student fitness & nutrition."""
    currency = profile.get('currency', 'INR (₹)')
    weight = profile.get('weight', 70)
    weight_unit = profile.get('weight_unit', 'kg')
    height = profile.get('height', 170)
    height_unit = profile.get('height_unit', 'cm')
    age = profile.get('age', 20)
    gender = profile.get('gender', 'Male')
    goal = profile.get('goal', 'Build Muscle')
    equipment = profile.get('equipment', 'Full Gym')
    cuisine = profile.get('cuisine', 'Indian')
    budget = profile.get('budget', 'Moderate ($$)')
    cooking_skill = profile.get('cooking_skill', 'Basic Stove')

    return f"""
Act as an elite fitness trainer and budget nutrition expert for university students.
Student Profile:
- Age: {age} years old, Gender: {gender}
- Weight: {weight} {weight_unit}, Height: {height} {height_unit}
- Primary Fitness Target: {goal}
- Available Equipment: {equipment}
- Cuisine Preference: {cuisine}, Diet: Standard
- Weekly Budget Tier: {budget}
- Preferred Currency for Budget Estimation: {currency}
- Cooking Skill / Setup: {cooking_skill}

TASK: Create a complete 7-Day Plan (Monday through Sunday) with aligned workouts and meals, followed by a clean, essential weekly grocery shopping list and budget breakdown.

CRITICAL FORMATTING RULES:
1. You MUST output all 7 days from Day: Monday to Day: Sunday.
2. For each day, use EXACTLY this format:
Day: [Day of Week, e.g. Monday]
Workout:
* [Target Muscle/Focus, e.g., Target: Chest & Triceps or Dorm Full Body]
* [Exercise 1 with sets and reps, e.g., Exercise 1: Push-ups - 4 sets x 12-15 reps]
* [Exercise 2 with sets and reps]
* [Exercise 3 with sets and reps]
* [Exercise 4 with sets and reps]
* [Exercise 5 with sets and reps]
* [Cardio/Core recommendation]
Meal:
* [Breakfast details with student ingredients]
* [Lunch details with student ingredients]
* [Snack details with student ingredients]
* [Dinner details with student ingredients]

3. At the end of Sunday, provide the weekly grocery and budget section using EXACTLY this header:
### WEEKLY GROCERY & BUDGET
#### 🛒 Weekly Student Grocery List (1 Person)
* **Proteins:** [List essential items with quantities]
* **Grains & Carbs:** [List essential items with quantities]
* **Vegetables & Produce:** [List essential items with quantities]
* **Pantry & Healthy Fats:** [List essential items with quantities]
#### 💡 Student Meal-Prep & Budget Tips
* [Tip 1 on bulk cooking or batch prep for dorm students]
* [Tip 2 on smart hydration and study energy]
#### 💰 Estimated Weekly Budget
* **Estimated Total:** [Realistic cost estimate in {currency}]
* **Savings Tip:** [Practical tip to save money in college]
"""
