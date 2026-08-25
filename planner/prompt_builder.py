"""
Prompt Engineering Engine for StudentFit AI.
Encapsulates structured LLM instructions, formatting delimiters, and constraint prompts.
"""

from typing import Union, Dict, Any
from planner.models import StudentProfile


class StudentPromptBuilder:
    """
    Object-oriented prompt builder constructing strictly delineated LLM completion requests.
    """

    @classmethod
    def build(cls, profile: Union[StudentProfile, Dict[str, Any]]) -> str:
        """
        Constructs the comprehensive 7-day fitness and synchronized nutrition prompt.
        """
        if isinstance(profile, dict):
            profile = StudentProfile.from_dict(profile)

        return f"""
Act as an elite fitness coach and student budget nutrition specialist.
Student Profile:
- Age: {profile.age} years old | Gender: {profile.gender}
- Weight: {profile.weight} {profile.weight_unit} | Height: {profile.height} {profile.height_unit}
- Goal: {profile.goal}
- Available Equipment: {profile.equipment}
- Cuisine Preference: {profile.cuisine} | Diet: {profile.diet_type}
- Weekly Budget Tier: {profile.budget} (Preferred Currency: {profile.currency})
- Cooking Facility / Setup: {profile.cooking_skill}

REQUIREMENTS:
1. Provide a comprehensive 7-DAY SCHEDULE (Monday through Sunday).
2. For EVERY day, output BOTH a tailored Workout Routine and Synchronized Meals matching the student's equipment and cooking skill.
3. At the end, output a complete Weekly Grocery Shopping List (1 Person) with realistic estimated costs in {profile.currency} and practical student meal-prep tips.
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
* **Proteins:** [Items with quantities and prices in {profile.currency}]
* **Grains & Carbs:** [Items with quantities and prices in {profile.currency}]
* **Produce & Veggies:** [Items with quantities and prices in {profile.currency}]
* **Healthy Fats & Dairy:** [Items with quantities and prices in {profile.currency}]
* **Estimated Weekly Total:** [Realistic student spending total in {profile.currency}]
#### 💡 Student Meal Prep & Budget Hacks
* [Batch cooking advice for dorm rooms / hostels]
* [Bulk buying savings tip for college budget]
### GROCERY_END
"""


def build_student_prompt(profile: Union[StudentProfile, Dict[str, Any]]) -> str:
    """Functional facade delegating to StudentPromptBuilder."""
    return StudentPromptBuilder.build(profile)


# Backwards compatibility alias
build_prompt = build_student_prompt
