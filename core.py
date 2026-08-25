"""
StudentFit AI - Core Object-Oriented Facade
Provides unified exports for domain models, services, generators, and PDF reporting.
"""

from planner import (
    StudentProfile,
    MacroResult,
    DailyPlan,
    WeeklyFitnessPlan,
    MacroCalculator,
    StudentPromptBuilder,
    BasePlanParser,
    MarkdownPlanParser,
    PDFReportGenerator,
    SecretsManager,
    BasePlanGenerator,
    MockPlanGenerator,
    GroqPlanGenerator,
    FitnessPlannerService,
    CANDIDATE_MODELS,
    get_api_key,
    calculate_macros,
    build_student_prompt,
    build_prompt,
    parse_ai_response,
    generate_plan_mock,
    generate_plan_real,
    create_fitness_pdf
)

__all__ = [
    # Domain Models & Services
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
    # Facade Functions & Constants
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
