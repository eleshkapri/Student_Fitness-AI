"""
Response Parsing Services for StudentFit AI.
Encapsulates delimiter extraction and Markdown structure compilation into typed domain models.
Optimized with pre-compiled regular expressions and cached parser instances.
"""

from abc import ABC, abstractmethod
import re
from typing import Tuple, List
from planner.models import DailyPlan, WeeklyFitnessPlan


class BasePlanParser(ABC):
    """Abstract base parser interface."""

    @abstractmethod
    def parse(self, raw_text: str) -> WeeklyFitnessPlan:
        """Parses raw text into a WeeklyFitnessPlan structure."""
        pass


class MarkdownPlanParser(BasePlanParser):
    """
    High-performance parser converting delimiter-formatted plain text and markdown
    into strongly typed DailyPlan items and grocery lists.
    """

    DAY_DELIMITER_REGEX = re.compile(r'### DAY_START(.*?)### DAY_END', re.DOTALL)
    GROCERY_DELIMITER_REGEX = re.compile(r'### GROCERY_START(.*?)### GROCERY_END', re.DOTALL)
    DAY_NAME_REGEX = re.compile(r'Day:\s*(.*)')
    WORKOUT_REGEX = re.compile(r'Workout:\s*(.*?)(?=Meal:|$)', re.DOTALL)
    MEAL_REGEX = re.compile(r'Meal:\s*(.*)', re.DOTALL)

    def parse(self, raw_text: str) -> WeeklyFitnessPlan:
        if not raw_text:
            return WeeklyFitnessPlan()

        days: List[DailyPlan] = []
        day_blocks = self.DAY_DELIMITER_REGEX.findall(raw_text)

        for block in day_blocks:
            day_match = self.DAY_NAME_REGEX.search(block)
            day_name = day_match.group(1).strip() if day_match else "Schedule"

            workout_match = self.WORKOUT_REGEX.search(block)
            workout_text = workout_match.group(1).strip() if workout_match else "Rest & Active Recovery"

            meal_match = self.MEAL_REGEX.search(block)
            meal_text = meal_match.group(1).strip() if meal_match else "Balanced Student Nutrition"

            days.append(DailyPlan(
                day=day_name,
                workout=workout_text,
                meal=meal_text
            ))

        grocery_match = self.GROCERY_DELIMITER_REGEX.search(raw_text)
        grocery_text = grocery_match.group(1).strip() if grocery_match else ""

        if not grocery_text and "#### 🛒" in raw_text:
            idx = raw_text.find("#### 🛒")
            grocery_text = raw_text[idx:]

        return WeeklyFitnessPlan(
            days=days,
            grocery=grocery_text,
            raw_text=raw_text
        )


# Global singleton parser instance for high performance
_DEFAULT_PARSER = MarkdownPlanParser()


def parse_ai_response(raw_text: str) -> Tuple[List[dict], str]:
    """Functional facade returning (days_list_of_dicts, grocery_string)."""
    plan = _DEFAULT_PARSER.parse(raw_text)
    return [d.to_dict() for d in plan.days], plan.grocery
