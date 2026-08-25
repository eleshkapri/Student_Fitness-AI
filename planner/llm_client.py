"""
LLM Client and AI Execution Module for StudentFit AI.
Encapsulates generator delegation, backward-compatibility facades, and macro utilities.
"""

from planner.models import StudentProfile, MacroResult, DailyPlan, WeeklyFitnessPlan
from planner.calculator import MacroCalculator, calculate_macros
from planner.prompt_builder import StudentPromptBuilder, build_student_prompt
from planner.parser import BasePlanParser, MarkdownPlanParser, parse_ai_response
from planner.pdf_service import PDFReportGenerator, create_fitness_pdf
from planner.generators import (
    CANDIDATE_MODELS,
    SecretsManager,
    BasePlanGenerator,
    MockPlanGenerator,
    GroqPlanGenerator,
    FitnessPlannerService,
    get_api_key,
    generate_plan_mock,
    generate_plan_real
)

__all__ = [
    "CANDIDATE_MODELS",
    "StudentProfile",
    "MacroResult",
    "DailyPlan",
    "WeeklyFitnessPlan",
    "MacroCalculator",
    "StudentPromptBuilder",
    "BasePlanParser",
    "MarkdownPlanParser",
    "PDFReportGenerator",
    "SecretsManager",
    "BasePlanGenerator",
    "MockPlanGenerator",
    "GroqPlanGenerator",
    "FitnessPlannerService",
    "get_api_key",
    "calculate_macros",
    "build_student_prompt",
    "parse_ai_response",
    "generate_plan_mock",
    "generate_plan_real",
    "create_fitness_pdf"
]
