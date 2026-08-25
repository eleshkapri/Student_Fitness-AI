"""
Planner Package for StudentFit AI.
Exports LLM clients, prompt builders, parsers, and PDF generator.
"""

from .prompt_builder import build_prompt
from .llm_client import (
    CANDIDATE_MODELS,
    get_api_key,
    calculate_macros,
    parse_ai_response,
    generate_plan_mock,
    generate_plan_real,
    create_fitness_pdf
)

__all__ = [
    "build_prompt",
    "CANDIDATE_MODELS",
    "get_api_key",
    "calculate_macros",
    "parse_ai_response",
    "generate_plan_mock",
    "generate_plan_real",
    "create_fitness_pdf"
]
