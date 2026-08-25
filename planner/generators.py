"""
AI Generation Engine & Services for StudentFit AI.
Encapsulates polymorphism across Mock / Groq engines, fallback cascade resilience, and secrets resolution.
"""

from abc import ABC, abstractmethod
import os
import re
from typing import Tuple, Optional, Union, Dict, Any, List
from groq import Groq

from planner.models import StudentProfile, WeeklyFitnessPlan
from planner.prompt_builder import StudentPromptBuilder
from planner.parser import MarkdownPlanParser


CANDIDATE_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "groq/compound-mini",
    "groq/compound",
    "qwen/qwen3.6-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]


class SecretsManager:
    """Encapsulates secure API key resolution across parameters, environment, and secrets files."""

    @classmethod
    def resolve_groq_key(cls, provided_key: Optional[str] = None) -> Optional[str]:
        if provided_key and provided_key.strip():
            return provided_key.strip()

        env_key = os.environ.get("GROQ_API_KEY")
        if env_key and env_key.strip():
            return env_key.strip()

        # Try local .streamlit/secrets.toml
        try:
            import toml
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            secrets_path = os.path.join(base_dir, ".streamlit", "secrets.toml")
            if os.path.exists(secrets_path):
                secrets = toml.load(secrets_path)
                key = secrets.get("GROQ_API_KEY")
                if key and key.strip():
                    return key.strip()
        except Exception:
            pass

        return None


class BasePlanGenerator(ABC):
    """Abstract base class for all plan generation engines."""

    @abstractmethod
    def generate(self, profile: StudentProfile) -> Tuple[str, Optional[str]]:
        """
        Executes plan generation.
        Returns Tuple of (raw_schedule_text, model_name_or_identifier).
        """
        pass


class MockPlanGenerator(BasePlanGenerator):
    """
    Simulation engine generating instant realistic 7-day student fitness schedules
    for demonstration mode and offline resilience.
    """

    def generate(self, profile: StudentProfile) -> Tuple[str, Optional[str]]:
        sym = profile.currency.split(' ')[0]

        mock_content = f"""
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
        return mock_content.strip(), "StudentFit AI Neural Engine (Simulation)"


class GroqPlanGenerator(BasePlanGenerator):
    """
    Live AI inference engine interfacing with Groq Cloud with automated model fallback cascade.
    """

    def __init__(self, api_key: str, candidate_models: Optional[List[str]] = None, timeout: float = 35.0):
        self._api_key = api_key
        self._models = candidate_models or CANDIDATE_MODELS
        self._timeout = timeout
        self._client = Groq(api_key=self._api_key, timeout=self._timeout)

    def generate(self, profile: StudentProfile, preferred_model: str = "openai/gpt-oss-20b") -> Tuple[str, Optional[str]]:
        prompt = StudentPromptBuilder.build(profile)

        if preferred_model in self._models:
            models_to_try = [preferred_model] + [m for m in self._models if m != preferred_model]
        else:
            models_to_try = self._models

        last_error = None
        for model_name in models_to_try:
            try:
                response = self._client.chat.completions.create(
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


class FitnessPlannerService:
    """
    High-level facade orchestrating validation, generation, parsing, and reporting.
    """

    def __init__(self, parser: Optional[MarkdownPlanParser] = None):
        self._parser = parser or MarkdownPlanParser()

    def create_weekly_plan(
        self,
        profile_data: Union[StudentProfile, Dict[str, Any]],
        api_key: Optional[str] = None,
        preferred_model: str = "openai/gpt-oss-20b",
        force_demo: bool = False
    ) -> WeeklyFitnessPlan:
        if isinstance(profile_data, dict):
            profile = StudentProfile.from_dict(profile_data)
        else:
            profile = profile_data

        resolved_key = SecretsManager.resolve_groq_key(api_key)

        if force_demo or not resolved_key:
            generator: BasePlanGenerator = MockPlanGenerator()
            raw_text, used_model = generator.generate(profile)
        else:
            generator = GroqPlanGenerator(api_key=resolved_key)
            raw_text, used_model = generator.generate(profile, preferred_model=preferred_model)

        plan = self._parser.parse(raw_text)
        plan.model_used = used_model
        return plan


# Backward-compatible functional facades
def get_api_key(provided_key: Optional[str] = None) -> Optional[str]:
    """Resolves Groq API key."""
    return SecretsManager.resolve_groq_key(provided_key)


def generate_plan_mock(profile: Union[StudentProfile, Dict[str, Any]]) -> str:
    """Generates instant mock schedule."""
    if isinstance(profile, dict):
        profile = StudentProfile.from_dict(profile)
    gen = MockPlanGenerator()
    text, _ = gen.generate(profile)
    return text


def generate_plan_real(profile: Union[StudentProfile, Dict[str, Any]], api_key: str, chosen_model: str = "openai/gpt-oss-20b") -> Tuple[str, Optional[str]]:
    """Executes Groq API generation."""
    if isinstance(profile, dict):
        profile = StudentProfile.from_dict(profile)
    gen = GroqPlanGenerator(api_key=api_key)
    return gen.generate(profile, preferred_model=chosen_model)
