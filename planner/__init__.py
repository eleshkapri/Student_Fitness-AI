"""
Planner Package for StudentFit AI.
Exports Object-Oriented Domain Models, Services, Parsers, Generators, and Facades.
"""

from .models import (
    StudentProfile,
    MacroResult,
    DailyPlan,
    WeeklyFitnessPlan
)
from .calculator import (
    MacroCalculator,
    calculate_macros
)
from .prompt_builder import (
    StudentPromptBuilder,
    build_student_prompt,
    build_prompt
)
from .parser import (
    BasePlanParser,
    MarkdownPlanParser,
    parse_ai_response
)
from .pdf_service import (
    PDFReportGenerator,
    create_fitness_pdf
)
from .generators import (
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
    # Domain Models
    "StudentProfile",
    "MacroResult",
    "DailyPlan",
    "WeeklyFitnessPlan",
    # OOP Services
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
    # Constants & Facades
    "CANDIDATE_MODELS",
    "get_api_key",
    "calculate_macros",
    "build_student_prompt",
    "build_prompt",
    "parse_ai_response",
    "generate_plan_mock",
    "generate_plan_real",
    "create_fitness_pdf"
]
