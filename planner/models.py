"""
Domain Models for StudentFit AI.
Encapsulates student fitness data, validation rules, and schedule structures.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import html


@dataclass
class MacroResult:
    """Encapsulates calculated caloric and macronutrient targets."""
    bmr: int
    tdee: int
    target_calories: int
    protein_g: int
    carbs_g: int
    fats_g: int
    water_liters: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bmr": self.bmr,
            "tdee": self.tdee,
            "target_calories": self.target_calories,
            "protein_g": self.protein_g,
            "carbs_g": self.carbs_g,
            "fats_g": self.fats_g,
            "water_liters": self.water_liters,
        }


@dataclass
class DailyPlan:
    """Encapsulates a single day's workout and synchronized nutrition."""
    day: str
    workout: str
    meal: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "day": self.day,
            "workout": self.workout,
            "meal": self.meal
        }


@dataclass
class WeeklyFitnessPlan:
    """Encapsulates a complete 7-day schedule with grocery and raw text."""
    days: List[DailyPlan] = field(default_factory=list)
    grocery: str = ""
    raw_text: str = ""
    model_used: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "days": [d.to_dict() for d in self.days],
            "grocery": self.grocery,
            "raw": self.raw_text,
            "model": self.model_used
        }


class StudentProfile:
    """
    Encapsulated student bio-data and campus constraints with defensive validation.
    """
    VALID_GENDERS = {"Male", "Female", "Other"}
    VALID_WEIGHT_UNITS = {"kg", "lbs"}
    VALID_HEIGHT_UNITS = {"cm", "ft/in"}
    DEFAULT_CURRENCY = "INR (₹)"

    def __init__(
        self,
        gender: str = "Male",
        age: float = 20,
        weight: float = 70.0,
        weight_unit: str = "kg",
        height: float = 170.0,
        height_unit: str = "cm",
        goal: str = "Build Muscle",
        equipment: str = "Full Gym",
        cuisine: str = "Indian",
        budget: str = "Moderate ($$)",
        currency: str = "INR (₹)",
        cooking_skill: str = "Basic Stove",
        diet_type: str = "Standard"
    ):
        self.gender = gender
        self.age = age
        self.weight = weight
        self.weight_unit = weight_unit
        self.height = height
        self.height_unit = height_unit
        self.goal = goal
        self.equipment = equipment
        self.cuisine = cuisine
        self.budget = budget
        self.currency = currency
        self.cooking_skill = cooking_skill
        self.diet_type = diet_type

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, value: str):
        val = str(value or "Male").strip().title()
        self._gender = val if val in self.VALID_GENDERS else "Male"

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: Any):
        try:
            num = int(float(value))
            self._age = max(14, min(90, num))
        except (ValueError, TypeError):
            self._age = 20

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: Any):
        try:
            num = float(value)
            self._weight = max(25.0, min(350.0, num))
        except (ValueError, TypeError):
            self._weight = 70.0

    @property
    def weight_unit(self) -> str:
        return self._weight_unit

    @weight_unit.setter
    def weight_unit(self, value: str):
        val = str(value or "kg").strip().lower()
        self._weight_unit = "lbs" if val == "lbs" else "kg"

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: Any):
        try:
            num = float(value)
            self._height = max(50.0, min(260.0, num))
        except (ValueError, TypeError):
            self._height = 170.0

    @property
    def height_unit(self) -> str:
        return self._height_unit

    @height_unit.setter
    def height_unit(self, value: str):
        val = str(value or "cm").strip().lower()
        self._height_unit = "ft/in" if val in {"ft/in", "feet", "in"} else "cm"

    @property
    def goal(self) -> str:
        return self._goal

    @goal.setter
    def goal(self, value: str):
        cleaned = self._sanitize_text(value or "Build Muscle")
        self._goal = cleaned if cleaned else "Build Muscle"

    @property
    def equipment(self) -> str:
        return self._equipment

    @equipment.setter
    def equipment(self, value: str):
        self._equipment = self._sanitize_text(value or "Full Gym")

    @property
    def cuisine(self) -> str:
        return self._cuisine

    @cuisine.setter
    def cuisine(self, value: str):
        self._cuisine = self._sanitize_text(value or "Indian")

    @property
    def budget(self) -> str:
        return self._budget

    @budget.setter
    def budget(self, value: str):
        self._budget = self._sanitize_text(value or "Moderate ($$)")

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, value: str):
        self._currency = self._sanitize_text(value or self.DEFAULT_CURRENCY)

    @property
    def cooking_skill(self) -> str:
        return self._cooking_skill

    @cooking_skill.setter
    def cooking_skill(self, value: str):
        self._cooking_skill = self._sanitize_text(value or "Basic Stove")

    @property
    def diet_type(self) -> str:
        return self._diet_type

    @diet_type.setter
    def diet_type(self, value: str):
        self._diet_type = self._sanitize_text(value or "Standard")

    @property
    def weight_in_kg(self) -> float:
        """Returns normalized weight in kilograms."""
        if self._weight_unit == "lbs":
            return self._weight * 0.453592
        return self._weight

    @property
    def height_in_cm(self) -> float:
        """Returns normalized height in centimeters."""
        if self._height_unit == "ft/in":
            return self._height * 2.54
        return self._height

    @staticmethod
    def _sanitize_text(text: Any, max_len: int = 150) -> str:
        """Defensively sanitizes user inputs against prompt injection and control sequences."""
        if not text:
            return ""
        s = str(text).strip()
        s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
        s = html.escape(s)[:max_len]
        return s

    def to_dict(self) -> Dict[str, Any]:
        """Serializes domain model to dictionary."""
        return {
            "gender": self.gender,
            "age": self.age,
            "weight": self.weight,
            "weight_unit": self.weight_unit,
            "height": self.height,
            "height_unit": self.height_unit,
            "goal": self.goal,
            "equipment": self.equipment,
            "cuisine": self.cuisine,
            "budget": self.budget,
            "currency": self.currency,
            "cooking_skill": self.cooking_skill,
            "diet_type": self.diet_type
        }

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> 'StudentProfile':
        """Factory method constructing domain model from dictionary payload."""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            gender=data.get("gender", "Male"),
            age=data.get("age", 20),
            weight=data.get("weight", 70),
            weight_unit=data.get("weight_unit", data.get("weightUnit", "kg")),
            height=data.get("height", 170),
            height_unit=data.get("height_unit", data.get("heightUnit", "cm")),
            goal=data.get("goal", "Build Muscle"),
            equipment=data.get("equipment", "Full Gym"),
            cuisine=data.get("cuisine", "Indian"),
            budget=data.get("budget", "Moderate ($$)"),
            currency=data.get("currency", cls.DEFAULT_CURRENCY),
            cooking_skill=data.get("cooking_skill", data.get("cookingSkill", "Basic Stove")),
            diet_type=data.get("diet_type", "Standard")
        )
